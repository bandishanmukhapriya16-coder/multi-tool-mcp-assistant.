
from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("Document Search Server")

# Locate the sample document
DOCUMENT_PATH = (
    Path(__file__).resolve().parent.parent
    / "documents"
    / "sample.txt"
)


@mcp.tool()
def search_docs(keyword: str) -> str:
    """Search the sample document for a keyword."""

    if not keyword.strip():
        raise ValueError("Keyword cannot be empty")

    if not DOCUMENT_PATH.exists():
        raise FileNotFoundError("Sample document not found")

    content = DOCUMENT_PATH.read_text(encoding="utf-8")

    results = [
        line for line in content.splitlines()
        if keyword.lower() in line.lower()
    ]

    if not results:
        return f"No results found for: {keyword}"

    return "\n".join(results)


if __name__ == "__main__":
    mcp.run()
