from dotenv import load_dotenv, dotenv_values
import os
from agents import Agent
from openai import OpenAI
from pydantic import BaseModel

dotenv_path = "/Users/jeffreybuencamino/ai-project/.env"
load_dotenv()


# API_KEY = os.getenv("OPENAI_API_KEY")
# print("API_KEY from getenv:", API_KEY)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "Write a limerick about the Python programming language.",
        },
    ],
)

response = completion.choices[0].message.content
print(response)



# --------------------------------------------------------------
# Step 1: Define the response format in a Pydantic model
# --------------------------------------------------------------


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


# --------------------------------------------------------------
# Step 2: Call the model
# --------------------------------------------------------------

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    response_format=CalendarEvent,
)

# --------------------------------------------------------------
# Step 3: Parse the response
# --------------------------------------------------------------

event = completion.choices[0].message.parsed
if event is not None:
    print(f"Event name: {event.name}")
    print(f"Event date: {event.date}")
    print(f"Event participants: {event.participants}")
else:
    print("Failed to parse event information")


