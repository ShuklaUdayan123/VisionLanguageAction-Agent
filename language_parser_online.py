import torch
from transformers import pipeline
import json, re

pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    dtype=torch.bfloat16,
    device_map="auto"
)

def parse_command(command):
    prompt = f"""
    Convert this command into JSON for AI2-THOR:
    Command: "{command}"
    """
    output = pipe(prompt, max_new_tokens=150, do_sample=False)[0]['generated_text']
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None