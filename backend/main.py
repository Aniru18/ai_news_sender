from fastapi import FastAPI
from pydantic import BaseModel
from app.crew import build_crew
from app.mcp_client import mail_client

app = FastAPI()


class GenerateRequest(BaseModel):
    topic: str


class MailRequest(BaseModel):
    topic: str
    email: str
    summary: str | None = None


# ----------------------------------
# Generate Summary Only
# ----------------------------------
@app.post("/generate")
def generate_summary(request: GenerateRequest):
    crew = build_crew(topic=request.topic)
    summary = crew.kickoff()
    summary_text = summary.tasks_output[1].raw
    return {"summary": summary_text}


# ----------------------------------
# Send Mail (Smart Logic)
# ----------------------------------
@app.post("/send-mail")
def send_mail(request: MailRequest):

    if not request.email:
        return {"message": "Email not provided"}

    # CASE 1: Summary already exists
    if request.summary:
        summary = request.summary
        mail_client.call(
            "send_email",
            {
                "to": request.email,
                "subject": f"Daily AI News Summary on {request.topic}",
                "body": summary
            }
        )

    # CASE 2: No summary → generate automatically
    else:
        crew = build_crew(topic=request.topic,
                          recipient_email=request.email,
                          send_email=True)
        summary = crew.kickoff()
