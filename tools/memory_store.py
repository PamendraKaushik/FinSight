import json
from pathlib import Path

MEMORY_FILE = Path("tools/memory_log.json")

def save_to_memory(question, answer, company):
    data = []
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    data.append({"question": question, "company": company, "answer": answer})
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_recent_memories(limit=5):
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            return data[-limit:]
    return []
