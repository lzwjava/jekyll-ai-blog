---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Building a Basic MCP Weather Server
translated: false
type: note
---

### What is the Model Context Protocol (MCP)?

The Model Context Protocol (MCP) is an open standard that defines how applications and AI systems (like large language models) exchange context, such as tools, resources, and prompts. It enables seamless integration between LLMs (e.g., Claude) and external services, making it easier to build extensible AI agents. This guide focuses on setting up a basic MCP server using plain Python (no `uv`), based on the official quickstart tutorial for a simple weather server that connects to the National Weather Service API. This server exposes two tools: `get_alerts` (for state weather alerts) and `get_forecast` (for location forecasts).

### Prerequisites
- Basic familiarity with Python and LLMs (e.g., Claude).
- Python 3.10 or higher installed.
- Access to a terminal (macOS/Linux recommended; Windows instructions similar but use PowerShell).
- For testing: Claude for Desktop app (available for macOS/Windows; not Linux—use a custom client if needed).
- Note: MCP servers communicate via JSON-RPC over stdio (stdin/stdout). Avoid printing to stdout in your code to prevent message corruption; use logging to stderr instead.

### Step 1: Set Up Your Environment
1. Create a new project directory:
   ```
   mkdir weather
   cd weather
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Upgrade pip (recommended for reliability):
   ```
   python -m pip install --upgrade pip
   ```

4. Install dependencies (MCP SDK and HTTP client):
   ```
   pip install "mcp[cli]" httpx
   ```

5. Create the server file:
   ```
   touch weather.py  # Or use your editor to create it
   ```

### Step 2: Build the MCP Server
Open `weather.py` in your editor and add the following code. This uses the `FastMCP` class from the MCP SDK, which auto-generates tool schemas from type hints and docstrings.

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("weather")

# Constants for the National Weather Service API
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

def main():
    # Run the server over stdio
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
```

- **Key Notes**:
  - Tools are defined with `@mcp.tool()` decorators. The LLM host (e.g., Claude) will call them based on user queries.
  - This example uses async functions for API calls.
  - Error handling ensures graceful failures (e.g., no data returns a user-friendly message).
  - For production, add logging (e.g., via `logging` module to stderr) and rate limiting.

### Step 3: Test the Server Locally
Run the server:
```
python weather.py
```
It should start listening on stdio without output (that's normal). To test manually, you'd need an MCP client, but proceed to integration for full testing.

### Step 4: Connect to a Host (e.g., Claude for Desktop)
1. Download and install Claude for Desktop from [claude.ai/download](https://claude.ai/download).

2. Configure the app by creating/editing `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the equivalent on Windows (`%APPDATA%\Claude\claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "python",
         "args": [
           "/ABSOLUTE/PATH/TO/weather/weather.py"  # Replace with your project path (use pwd to find it)
         ],
         "cwd": "/ABSOLUTE/PATH/TO/weather"  # Optional: Set working directory if needed
       }
     }
   }
   ```
   - Use absolute paths (e.g., `/Users/yourname/weather/weather.py` on macOS).
   - On Windows, use forward slashes `/` or double backslashes `\\`.
   - Ensure your virtual environment is activated when testing locally, but for Claude, it runs the Python executable from your system (make sure the venv's site-packages are accessible or install globally if preferred—though venv is recommended).
   - Find Python path with `which python` (macOS/Linux) or `where python` (Windows).

3. Fully restart Claude for Desktop (quit completely, e.g., Cmd+Q on macOS).

4. Test in Claude:
   - Open Claude and click the "Search and tools" icon (slider icon).
   - You should see `get_alerts` and `get_forecast` listed.
   - Query examples:
     - "What are the active weather alerts in California?"
     - "What's the weather forecast for latitude 37.77, longitude -122.41?" (San Francisco coords).
   - Claude will invoke the tools automatically and incorporate results into its response.
   - Note: This API only supports US locations.

### Troubleshooting
- **Server not appearing in Claude**: Verify JSON syntax, absolute paths, and full restart of the app. Check logs at `~/Library/Logs/Claude/mcp*.log`.
- **Tool errors**: Ensure the server runs error-free locally. Add delays for API rate limits if needed.
- **Non-US queries**: The NWS API is US-only; extend with other APIs for global support.
- For advanced features (resources, prompts, notifications), see the full MCP docs.

This sets up a functional MCP server using plain Python. For TypeScript/Node.js alternatives or more examples, check the resources below.

### References
- [Build an MCP Server (Official Docs)](https://modelcontextprotocol.io/docs/develop/build-server)
- [MCP Quickstart Guide](https://modelcontextprotocol.info/docs/quickstart/quickstart/)
- [Model Context Protocol Guide with Demo](https://www.datacamp.com/tutorial/mcp-model-context-protocol)
- [How the Model Context Protocol Works](https://www.freecodecamp.org/news/how-the-model-context-protocol-works/)
- [Practical Introduction to MCP](https://medium.com/@davidlfliang/guide-a-practical-introduction-to-model-context-protocol-mcp-2f63b636f510)
