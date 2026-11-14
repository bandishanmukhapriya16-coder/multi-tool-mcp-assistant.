from mcp.server.fastmcp import FastMCP
from pathlib import Path
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr
)

mcp = FastMCP("Document Search Server")

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
        raise FileNotFoundError(
            f"Sample document not found: {DOCUMENT_PATH}"
        )

    content = DOCUMENT_PATH.read_text(encoding="utf-8")

    results = [
        line for line in content.splitlines()
        if keyword.lower() in line.lower()
    ]

    if not results:
        return f"No results found for: {keyword}"

    return "\n".join(results)


if __name__ == "__main__":
    mcp.run(transport="stdio")