
import asyncio
import sys
from pathlib import Path
from contextlib import AsyncExitStack

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parent
MODEL = "qwen2.5:3b"

SERVERS = {
    "Calculator": BASE_DIR / "servers" / "calculator_server.py",
    "Documents": BASE_DIR / "servers" / "document_server.py",
    "Text Processing": BASE_DIR / "servers" / "text_server.py"
}


async def main():

    async with AsyncExitStack() as stack:

        sessions = {}
        tool_to_server = {}
        ollama_tools = []

        # Connect to all MCP servers
        for name, server_path in SERVERS.items():

            print(f"\nConnecting to {name}...")

            params = StdioServerParameters(
                command=sys.executable,
                args=[str(server_path)]
            )

            read_stream, write_stream = await stack.enter_async_context(
                stdio_client(params)
            )

            session = await stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )

            await session.initialize()
            sessions[name] = session

            print(f"{name} connected successfully!")

        # Discover tools from all servers
        for server_name, session in sessions.items():

            response = await session.list_tools()

            for tool in response.tools:

                tool_to_server[tool.name] = session

                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                })

        print("\n========== AVAILABLE AI TOOLS ==========")

        for tool in ollama_tools:
            print("-", tool["function"]["name"])

        # Get user request
        user_request = input("\nAsk your AI assistant: ")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful multi-tool AI assistant. "
                    "Use available tools whenever needed. "
                    "You can use calculator, document search "
                    "and text processing tools. "
                    "Explain the final result clearly."
                )
            },
            {
                "role": "user",
                "content": user_request
            }
        ]

        # AI tool execution loop
        for step in range(5):

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=ollama_tools
            )

            messages.append(response.message)

            tool_calls = response.message.tool_calls

            if not tool_calls:
                print("\nAI Assistant:", response.message.content)
                break

            for tool_call in tool_calls:

                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\nExecuting MCP tool: {tool_name}")

                session = tool_to_server.get(tool_name)

                if session is None:
                    tool_output = "Error: Unknown tool"
                else:
                    try:
                        result = await session.call_tool(
                            tool_name,
                            arguments=arguments
                        )

                        tool_output = "\n".join(
                            item.text
                            for item in result.content
                            if hasattr(item, "text")
                        )

                        if result.isError:
                            tool_output = "Tool error: " + tool_output

                    except Exception as error:
                        tool_output = f"Execution failed: {error}"

                messages.append({
                    "role": "tool",
                    "content": tool_output
                })

        else:
            print("Maximum tool execution steps reached.")


if __name__ == "__main__":
    asyncio.run(main())
