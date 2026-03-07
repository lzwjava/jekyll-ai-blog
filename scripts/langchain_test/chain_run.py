import os
import json
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 1. (Optionally) set your OpenRouter key in env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise Exception("OPENROUTER_API_KEY environment variable is not set or is empty")

os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
# and the base URL:
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# 2. Initialize the LLM to use OpenRouter
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    default_headers={"HTTP-Referer": "https://github.com/anthropics/claude-code"},
)

# 3. Create your prompt template
template = PromptTemplate(
    input_variables=["product"],
    template="Write a short marketing blurb for the product: {product}.",
)

# 4. Build and run the chain
chain = template | llm
result = chain.invoke({"product": "wireless noise-cancelling headphones"})

# Create test directory if it doesn't exist
os.makedirs("test", exist_ok=True)

# Format the result as a dictionary
output = {
    "content": result.content,
    "metadata": {
        "usage": result.response_metadata["token_usage"],
        "model": result.response_metadata["model_name"],
    },
}

# Save to file with nice formatting
with open("text_test/langchain_run.json", "w") as f:
    json.dump(output, f, indent=2)

print("Result saved to test/langchain_run.json")
