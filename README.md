# LLM JSON Parser 

## Overview 
`LLM JSON Parser` is a Python-based tool designed to read, parse, and reformat JSON data into a structured schema using language models. This project leverages OpenAI's GPT-4 model for natural language processing and various Python libraries for handling and formatting JSON data.
## Setup 

### Prerequisites 

- Python 3.11

- Poetry

### Installation 
 
1. **Clone the repository:** 

```bash
git clone https://github.com/thibaudbrg/llm-json-parser.git
cd llm-json-parser
```
 
2. **Install dependencies using Poetry:** 

```bash
poetry install
```
 
3. **Set up environment variables:** Create a `.env` file in the root directory or use the provided `.env.example` and update the necessary values:

```plaintext
cp .env.example .env
```
Update `.env` with your API keys:

```plaintext
# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=default
OPENAI_API_KEY=your_openai_api_key
```

## Usage 

### Part 1: Online Call to OpenAI 
 
1. **Place the input JSON file in the `inputs` directory:** 

```plaintext
llm_json_parser/inputs/bad_json.json
```
 
2. **Run the main script:** 

```bash
poetry run python llm_json_parser/main.py
```
This script will read the `bad_json.json` file, process it using OpenAI's GPT-4 model, and save the formatted JSON to `llm_json_parser/outputs/good_json.json`.

### Part 2: Offline Call to Ollama 
 
1. **Run the Ollama script:** 

```bash
poetry run python llm_json_parser/ollama.py
```
This script demonstrates the usage of the `instructor` library to interact with a local OpenAI model and retrieve structured data. Although the example uses a specific model, it can be adapted to work with any LLM that supports similar API interactions.