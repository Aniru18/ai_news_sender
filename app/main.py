from app.crew import build_crew
from mcp_servers.news_server.tools import get_filtered_news_logic


if __name__ == "__main__":

    topic = "agentic ai"
    recipient_email = "shitaniruddha92@gmail.com"

    print("\n========== FETCHING NEWS ==========\n")

    # 🔹 Step 1: Fetch news directly and print
    news_data = get_filtered_news_logic(topic=topic)

    for i, article in enumerate(news_data, 1):
        print(f"{i}. {article['title']} ({article['source']})")

    print("\n========== GENERATING & SENDING NEWSLETTER ==========\n")

    # 🔹 Step 2: Run CrewAI
    crew = build_crew(topic, recipient_email)
    result = crew.kickoff()

    print("\n========== FINAL NEWSLETTER ==========\n")
    print(result)
