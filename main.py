import torch
from transformers import pipeline
import json
import re
import ai2thor.controller
import matplotlib.pyplot as plt

# -----------------------------
# Device setup
# -----------------------------
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Device set to use {device}")

# -----------------------------
# Load TinyLlama model
# -----------------------------
generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    dtype=torch.bfloat16 if device == "mps" else torch.float16,
    device_map="auto",
)
print("Model loaded successfully!\n")

# -----------------------------
# Launch AI2-THOR
# -----------------------------
controller = ai2thor.controller.Controller(scene="FloorPlan1")
print("AI2-THOR controller started.\n")

# -----------------------------
# Helper functions
# -----------------------------
def extract_json(text):
    """Extract the first JSON block from text."""
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)
    return None

def parse_command(command):
    """Parse natural language command into JSON actions."""
    prompt = f"""
You are a language-to-action parser for a household robot.

Convert this user's command into JSON. Replace <number> and <angle> with actual integers.
Output format:

{{
  "actions": [
    {{"action": "MoveAhead", "steps": 1}},
    {{"action": "RotateRight", "degrees": 90}}
  ]
}}

Command to parse:
"{command}"

Only output valid JSON — nothing else.
"""

    result = generator(prompt, max_new_tokens=200, do_sample=False)
    output = result[0]["generated_text"].strip()

    # Extract JSON block
    json_block = extract_json(output)
    if not json_block:
        print("⚠️ No JSON detected in model output.")
        return None

    try:
        return json.loads(json_block)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parsing error: {e}")
        print("Raw detected JSON block:\n", json_block)
        return None

def execute_actions(actions):
    """Execute JSON actions in AI2-THOR."""
    if not actions or "actions" not in actions:
        print("Invalid command or no actions found.")
        return

    for act in actions["actions"]:
        action_type = act.get("action")
        if action_type == "MoveAhead":
            steps = act.get("steps", 1)
            for _ in range(steps):
                controller.step(action="MoveAhead")
        elif action_type == "RotateRight":
            degrees = act.get("degrees", 90)
            controller.step(action="RotateRight", degrees=degrees)
        elif action_type == "PickupObject":
            obj = act.get("object")
            if obj:
                controller.step(action="PickupObject", objectId=obj)

        # Show current frame
        event = controller.step(action="Pass")
        plt.imshow(event.frame)
        plt.axis('off')
        plt.show()

# -----------------------------
# Main loop
# -----------------------------
if __name__ == "__main__":
    print("Enter natural language commands for the robot (type 'exit' to quit):\n")

    while True:
        command = input("Enter command (or 'exit'): ").strip()
        if command.lower() == "exit":
            print("Exiting program. 🛑")
            break

        actions_json = parse_command(command)
        execute_actions(actions_json)

    # Stop AI2-THOR
    controller.stop()