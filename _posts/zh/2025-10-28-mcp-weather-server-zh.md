---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 构建基础MCP气象服务器
translated: true
type: note
---

### 什么是模型上下文协议（MCP）？

模型上下文协议（MCP）是一个开放标准，定义了应用程序与人工智能系统（如大语言模型）之间如何交换上下文信息，包括工具、资源和提示。它实现了大语言模型（例如Claude）与外部服务的无缝集成，使得构建可扩展的AI智能体变得更加容易。本指南基于官方快速入门教程，重点介绍如何使用纯Python（不使用`uv`）设置一个基本的MCP服务器，该服务器连接至美国国家气象局API，提供简单的天气服务。该服务器暴露两个工具：`get_alerts`（用于获取州级天气警报）和`get_forecast`（用于获取位置天气预报）。

### 前提条件
- 基本熟悉Python和LLM（例如Claude）。
- 已安装Python 3.10或更高版本。
- 可访问终端（推荐macOS/Linux；Windows操作类似，但请使用PowerShell）。
- 用于测试：Claude桌面应用（适用于macOS/Windows；Linux不支持——如需使用，请使用自定义客户端）。
- 注意：MCP服务器通过stdio（标准输入/输出）上的JSON-RPC进行通信。为避免消息损坏，请勿在代码中向stdout打印内容；应改用stderr进行日志记录。

### 步骤1：设置环境
1. 创建新的项目目录：
   ```
   mkdir weather
   cd weather
   ```

2. 创建并激活虚拟环境：
   ```
   python -m venv .venv
   source .venv/bin/activate  # Windows系统：.venv\Scripts\activate
   ```

3. 升级pip（推荐以确保可靠性）：
   ```
   python -m pip install --upgrade pip
   ```

4. 安装依赖项（MCP SDK和HTTP客户端）：
   ```
   pip install "mcp[cli]" httpx
   ```

5. 创建服务器文件：
   ```
   touch weather.py  # 或使用编辑器创建
   ```

### 步骤2：构建MCP服务器
在编辑器中打开`weather.py`并添加以下代码。此代码使用MCP SDK中的`FastMCP`类，该类根据类型提示和文档字符串自动生成工具模式。

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化MCP服务器
mcp = FastMCP("weather")

# 美国国家气象局API常量
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """向NWS API发起请求并进行错误处理。"""
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
    """将警报要素格式化为可读字符串。"""
    props = feature["properties"]
    return f"""
事件: {props.get('event', 'Unknown')}
区域: {props.get('areaDesc', 'Unknown')}
严重程度: {props.get('severity', 'Unknown')}
描述: {props.get('description', 'No description available')}
指示: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取美国州的天气警报。

    参数:
        state: 两字母美国州代码（例如CA、NY）
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "无法获取警报或未找到警报。"

    if not data["features"]:
        return "该州暂无活跃警报。"

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """获取位置的天气预报。

    参数:
        latitude: 位置的纬度
        longitude: 位置的经度
    """
    # 首先获取预报网格端点
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "无法获取该位置的预报数据。"

    # 从points响应中获取预报URL
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "无法获取详细预报。"

    # 将时段格式化为可读预报
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # 仅显示接下来5个时段
        forecast = f"""
{period['name']}:
温度: {period['temperature']}°{period['temperatureUnit']}
风速: {period['windSpeed']} {period['windDirection']}
预报: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

def main():
    # 通过stdio运行服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
```

- **关键说明**：
  - 工具使用`@mcp.tool()`装饰器定义。LLM主机（例如Claude）将根据用户查询调用它们。
  - 此示例使用异步函数进行API调用。
  - 错误处理确保优雅失败（例如，无数据时返回用户友好消息）。
  - 对于生产环境，应添加日志记录（例如通过`logging`模块记录到stderr）和速率限制。

### 步骤3：本地测试服务器
运行服务器：
```
python weather.py
```
它应在stdio上开始监听而无输出（这很正常）。如需手动测试，您需要一个MCP客户端，但请继续下一步进行集成测试。

### 步骤4：连接到主机（例如Claude桌面版）
1. 从[claude.ai/download](https://claude.ai/download)下载并安装Claude桌面版。

2. 通过创建/编辑`~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或Windows上的等效路径（`%APPDATA%\Claude\claude_desktop_config.json`）来配置应用：
   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "python",
         "args": [
           "/ABSOLUTE/PATH/TO/weather/weather.py"  // 替换为您的项目路径（使用pwd查找）
         ],
         "cwd": "/ABSOLUTE/PATH/TO/weather"  // 可选：如有需要设置工作目录
       }
     }
   }
   ```
   - 使用绝对路径（例如macOS上的`/Users/yourname/weather/weather.py`）。
   - 在Windows上，使用正斜杠`/`或双反斜杠`\\`。
   - 在本地测试时确保虚拟环境已激活，但对于Claude，它运行系统Python可执行文件（确保venv的site-packages可访问，或如首选可全局安装——但推荐使用venv）。
   - 使用`which python`（macOS/Linux）或`where python`（Windows）查找Python路径。

3. 完全重启Claude桌面版（完全退出，例如在macOS上使用Cmd+Q）。

4. 在Claude中测试：
   - 打开Claude并点击“搜索和工具”图标（滑块图标）。
   - 您应看到列出的`get_alerts`和`get_forecast`。
   - 查询示例：
     - “加利福尼亚州有哪些活跃天气警报？”
     - “纬度37.77、经度-122.41的天气预报是什么？”（旧金山坐标）。
   - Claude将自动调用工具并将结果整合到其响应中。
   - 注意：此API仅支持美国位置。

### 故障排除
- **服务器未出现在Claude中**：验证JSON语法、绝对路径以及应用的完全重启。检查`~/Library/Logs/Claude/mcp*.log`的日志。
- **工具错误**：确保服务器在本地运行无错误。如需要，可为API速率限制添加延迟。
- **非美国查询**：NWS API仅限美国；如需全球支持，请扩展其他API。
- 对于高级功能（资源、提示、通知），请参阅完整的MCP文档。

这使用纯Python设置了一个功能正常的MCP服务器。对于TypeScript/Node.js替代方案或更多示例，请查看以下资源。

### 参考资料
- [构建MCP服务器（官方文档）](https://modelcontextprotocol.io/docs/develop/build-server)
- [MCP快速入门指南](https://modelcontextprotocol.info/docs/quickstart/quickstart/)
- [模型上下文协议指南与演示](https://www.datacamp.com/tutorial/mcp-model-context-protocol)
- [模型上下文协议工作原理](https://www.freecodecamp.org/news/how-the-model-context-protocol-works/)
- [MCP实用入门指南](https://medium.com/@davidlfliang/guide-a-practical-introduction-to-model-context-protocol-mcp-2f63b636f510)
