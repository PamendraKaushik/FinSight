import ollama

def run_llm(model: str, prompt: str, temperature: float = 0.7) -> str:
    """
    Sends the prompt to the local Ollama model and returns the response text.
    """
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Ollama Error: {e}"