from mcp_servers.news_server.tools import mcp

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

if __name__ == "__main__":
    mcp.run()

