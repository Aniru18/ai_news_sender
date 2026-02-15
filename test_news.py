import json
from mcp_servers.news_server.tools import get_filtered_news_logic

result = get_filtered_news_logic(topic="agentic ai")

print(json.dumps(result, indent=2))
