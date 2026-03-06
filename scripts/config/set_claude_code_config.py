import json
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python set_claude_code_config.py <model>")
    sys.exit(1)

model = sys.argv[1]

json_path = os.path.join(os.path.dirname(__file__), "claude_code_config.json")

try:
    with open(json_path, "r") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading config: {e}")
    sys.exit(1)

# Find openrouter provider
openrouter_provider = None
for provider in config["Providers"]:
    if provider["name"] == "openrouter":
        if model not in provider["models"]:
            print(f"Model '{model}' not found in openrouter models.")
            sys.exit(1)
        openrouter_provider = provider
        break

if openrouter_provider is None:
    print("Openrouter provider not found in config.")
    sys.exit(1)

# Update router
router = config["Router"]
router["default"] = f"openrouter,{model}"
router["background"] = f"openrouter,{model}"
router["think"] = f"openrouter,{model}"
router["longContext"] = f"openrouter,{model}"
router["webSearch"] = f"openrouter,{model}"
# longContextThreshold remains 30000

with open(json_path, "w") as f:
    json.dump(config, f, indent=2)

print(f"Successfully updated config to use model: {model}")
