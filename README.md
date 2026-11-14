# Build a Multi-Tool AI Assistant Using MCP

## Introduction
This project demonstrates a Multi-Tool AI Assistant
using Model Context Protocol (MCP), Python and Ollama.

## Technologies Used
- Python
- Model Context Protocol (MCP)
- Ollama
- Qwen 2.5 3B
- Visual Studio Code

## Project Modules

### 1. Calculator Server
- Addition
- Subtraction
- Multiplication
- Division

### 2. Document Search Server
- Searches documents using keywords.

### 3. Text Processing Server
- Word counting
- Uppercase conversion
- Text reversal

## Architecture
User -> Python MCP Client -> Ollama AI
-> Calculator / Document Search / Text Processing

## Installation

Install dependencies:

pip install -r requirements.txt

Download the AI model:

ollama pull qwen2.5:3b

## Run the Project

python client.py

## Features
- Multiple MCP servers
- Automatic tool discovery
- AI-based tool selection
- Multi-tool execution
- Error handling

## Conclusion
This project demonstrates how MCP connects
AI applications with multiple external tools.