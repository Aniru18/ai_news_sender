from crewai import Task


def get_fetch_task(news_agent, topic):
    return Task(
        description=f"""
        Fetch top news headlines for topic: {topic}.
        Return structured list of titles and sources.
        """,
        agent=news_agent,
        expected_output="List of news headlines with source"
    )


def get_summary_task(writer_agent):
    return Task(
        description="""
        Using the provided headlines, write a professional
        160-word news summary suitable for email newsletter.
        Keep it concise and clear.
        """,
        agent=writer_agent,
        expected_output="Formatted 160-word newsletter summary"
    )


def get_email_task(mail_agent, recipient_email):
    return Task(
        description=f"""
        Send the generated newsletter to {recipient_email}.
        Subject: Daily AI News Summary
        """,
        agent=mail_agent,
        expected_output="Email sent confirmation"
    )
