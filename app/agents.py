from crewai import Agent
from app.llm import get_llm

def get_news_agent(news_tool):
    return Agent(
        role="News Research Analyst",
        goal="Fetch the latest news headlines for a given topic.",
        backstory="You are responsible for gathering relevant news.",
        tools=[news_tool],
        llm=get_llm(),
        verbose=True
    )


def get_writer_agent():
    return Agent(
        role="Newsletter Writer",
        goal="Write a professional 160-word news summary.",
        backstory="You are an expert news editor creating concise newsletters.",
        llm=get_llm(),
        verbose=True
    )


def get_mail_agent(mail_tool):
    return Agent(
        role="Email Dispatcher",
        goal="Send formatted newsletter via Gmail.",
        backstory="You are responsible for sending final newsletters.",
        tools=[mail_tool],
        llm=get_llm(),
        verbose=True
    )
