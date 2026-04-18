# Generative AI Full Course (Part 3)

This project contains practical examples for:
- LangChain tools
- Tool calling with an LLM
- Runnable composition (sequential, parallel, passthrough)
- A simple agent with human approval for tool execution
- News summarization with Tavily search + Mistral

All examples are written in Python and use `ChatMistralAI` (`mistral-small-2506`).

## Project Structure

- `owntool.py`: Creates a custom LangChain tool (`get_greeting`) and inspects its metadata.
- `toolcalling.py`: Demonstrates LLM tool-calling flow using a custom tool (`get_text_length`).
- `sequencerunnable.py`: Basic runnable sequence (`prompt -> model -> parser`).
- `parallelrunnable.py`: Runs multiple branches in parallel with `RunnableParallel`.
- `runnablepassthrough.py`: Generates code and explanation together using `RunnablePassthrough` + `RunnableParallel`.
- `newssummarizer.py`: Fetches latest AI news using Tavily and summarizes into bullet points with Mistral.
- `Agents.py`: City assistant agent with two tools:
  - `get_weather` (OpenWeather API)
  - `get_news` (Tavily API)
  Includes human approval middleware before each tool call.

## Prerequisites

- Python 3.10+
- API keys for:
  - Mistral
  - Tavily
  - OpenWeather

## Installation

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

If any import is missing in your environment, install these as well:

```bash
pip install requests rich tavily-python
```

## Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

## How to Run

Run any script directly:

```bash
python owntool.py
python toolcalling.py
python sequencerunnable.py
python parallelrunnable.py
python runnablepassthrough.py
python newssummarizer.py
python Agents.py
```

## Notes

- `Agents.py` currently queries weather using `city,IN` (India). If needed, update the API query logic for global locations.
- `toolcalling.py` and `Agents.py` are interactive scripts and wait for terminal input.
- The project is educational and focuses on understanding LangChain building blocks, not production hardening.
