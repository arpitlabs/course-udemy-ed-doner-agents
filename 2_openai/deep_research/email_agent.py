import os
from typing import Dict
from sys import path
from pathlib import Path

import sendgrid
#from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool
path.insert(0, str(Path(__file__).parent.parent))
from azure_client import get_AzureOpenAIChatCompletionsModel

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body """
    #sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = "ed@edwarddonner.com" # Change this to your verified email
    to_email = "ed.donner@gmail.com" # Change this to your email
    content = html_body
    mail = (from_email, to_email, subject, content)
    print(mail)
    #sg.client.mail.send.post(request_body=mail)
    return "success"


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=get_AzureOpenAIChatCompletionsModel(),
)
