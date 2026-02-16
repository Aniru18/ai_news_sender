# from crewai import Crew, Process
# from crewai.tools import tool

# from app.agents import (
#     get_news_agent,
#     get_writer_agent,
#     get_mail_agent
# )

# from app.tasks import (
#     get_fetch_task,
#     get_summary_task,
#     get_email_task
# )

# from mcp_servers.news_server.tools import get_filtered_news_logic
# from mcp_servers.mail_server.server import send_email_logic


# # 🔹 CrewAI-native tool wrappers
# @tool
# def news_tool(topic: str):
#     """Fetch latest news headlines for a topic."""
#     return get_filtered_news_logic(topic=topic)


# @tool
# def mail_tool(to: str, subject: str, body: str):
#     """Send email using Gmail."""
#     return send_email_logic(to=to, subject=subject, body=body)


# def build_crew(topic: str, recipient_email: str):

#     news_agent = get_news_agent(news_tool)
#     writer_agent = get_writer_agent()
#     mail_agent = get_mail_agent(mail_tool)

#     fetch_task = get_fetch_task(news_agent, topic)
#     summary_task = get_summary_task(writer_agent)
#     email_task = get_email_task(mail_agent, recipient_email)

#     crew = Crew(
#         agents=[news_agent, writer_agent, mail_agent],
#         tasks=[fetch_task, summary_task, email_task],
#         process=Process.sequential,
#         verbose=True
#     )

#     return crew
from crewai import Crew, Process
from app.tools import news_tool, mail_tool
from app.agents import (
    get_news_agent,
    get_writer_agent,
    get_mail_agent
)

from app.tasks import (
    get_fetch_task,
    get_summary_task,
    get_email_task
)



def build_crew(topic: str, recipient_email: str):

    news_agent = get_news_agent(news_tool)
    writer_agent = get_writer_agent()
    mail_agent = get_mail_agent(mail_tool)

    fetch_task = get_fetch_task(news_agent, topic)
    summary_task = get_summary_task(writer_agent)
    email_task = get_email_task(mail_agent, recipient_email)

    crew = Crew(
        agents=[news_agent, writer_agent, mail_agent],
        tasks=[fetch_task, summary_task, email_task],
        process=Process.sequential,
        verbose=True
    )

    return crew

