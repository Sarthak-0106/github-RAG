import os
from git import Repo
from langchain_core.documents import Document
from tree_sitter_languages import get_language, get_parser

# ---------------- CONFIG ---------------- #

IGNORED_DIRS = [
    ".git",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    ".venv"
]

# ---------------- LANGUAGE DETECTION ---------------- #

def detect_language(file):
    if file.endswith(".py"):
        return "python"
    elif file.endswith(".java"):
        return "java"
    elif file.endswith(".js") or file.endswith(".ts"):
        return "javascript"
    elif file.endswith(".go"):
        return "go"
    elif file.endswith(".cpp"):
        return "cpp"
    else:
        return None

# ---------------- TREE-SITTER SPLITTER ---------------- #

def split_code_tree_sitter(content, file_path, language):
    try:
        parser = get_parser(language)
        tree = parser.parse(bytes(content, "utf8"))

        root = tree.root_node
        chunks = []

        TARGET_NODES = [
            "function_definition",
            "function_declaration",
            "method_definition",
            "method_declaration",
            "class_definition",
            "class_declaration",
            "constructor_declaration"
        ]

        def extract_nodes(node):
            if node.type in TARGET_NODES:

                code = content[node.start_byte:node.end_byte]

                # Extract name (VERY IMPORTANT)
                name = None
                for child in node.children:
                    if child.type == "identifier":
                        name = content[child.start_byte:child.end_byte]
                        break

                # Avoid tiny useless chunks
                if len(code.strip()) > 20:
                    chunks.append(
                        Document(
                            page_content=code,
                            metadata={
                                "source": file_path,
                                "type": node.type,
                                "language": language,
                                "name": name
                            }
                        )
                    )

            for child in node.children:
                extract_nodes(child)

        extract_nodes(root)

        # Debug (optional)
        # print(f"{file_path} → {len(chunks)} chunks")

        return chunks

    except Exception as e:
        print(f"Tree-sitter failed for {file_path}: {e}")
        return []

# ---------------- CLONE ---------------- #

def clone_repo(repo_url, base_path="repos"):
    repo_name = repo_url.split("/")[-1]
    local_path = os.path.join(base_path, repo_name)

    if not os.path.exists(local_path):
        Repo.clone_from(repo_url, local_path)

    return local_path

# ---------------- LOADER ---------------- #

def create_repo_summary(documents):
    files = set(doc.metadata["source"] for doc in documents)

    structure = "Project Structure:\n\n"
    for f in sorted(files):
        structure += f"- {f}\n"

    return Document(
        page_content=structure,
        metadata={
            "source": "repo_summary",
            "type": "repo_summary",
            "priority": 9
        }
    )

def load_repo_files(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                relative_path = os.path.relpath(file_path, repo_path)
                if file.lower() == "readme.md":
                    documents.append(
                        Document(
                            page_content=content,
                            metadata={
                                "source": "README",
                                "type": "readme",
                                "priority": 10
                            }
                        )
                    )
                    continue

                language = detect_language(file)

                # AST-based splitting
                if language:
                    chunks = split_code_tree_sitter(content, relative_path, language)

                    if chunks:
                        documents.extend(chunks)
                        continue

                # fallback (full file)
                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": relative_path,
                            "language": language or "text",
                            "type": "file",
                            "name": file
                        }
                    )
                )

            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    documents.append(create_repo_summary(documents))
    return documents