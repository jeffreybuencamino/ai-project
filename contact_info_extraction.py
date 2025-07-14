import os, requests, asyncio
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from pydantic import BaseModel
from bs4 import BeautifulSoup

#--- this loads api key from .env file ----
load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPEN_API_KEY is not set int the environment variables")

#---- gets url for htttp request ----
@function_tool
def get_url_content(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        print("Request was successful!")
        print(response.status_code)
        print('\n\n')        
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.get_text(strip=True))
        print("\nPage Title:", soup.title.string if soup.title else "No title found")
        output = soup.get_text(strip=True) and soup.title.string if soup.title else "No title found"
        return soup.get_text(strip=True)
    else:
        raise ValueError(f"Request failed with status code: {response.status_code}")

#--- Basemodel for the recipe output ---
class Contact_info(BaseModel):
    phone: str
    email: str

#--- Agent for extracting contact info ---
extraction_agent = Agent(
    name="extraction_agent",
    instructions=(
        "You are an agent for extracting phone numbers and emails. You will be given a URL of a website to scrape information using the get_url_content tool you are given."
        "Your job is to use the information given from the get_url_content tool, and output the contact information in an organized manner."
        "## Notes: The tool will give you unstrctured text, so you will need to use your knowledge of phone numbers and emails to extract them."
    ),
    tools=[get_url_content],
    model="gpt-4o-mini",
    output_type=Contact_info
)
#--- Run the agent with the URL of the website to scrape ---
async def main():
    url_input = input("Enter the URL to scrape for contact information: ")
    global response
    response = await Runner.run(extraction_agent, url_input)

asyncio.run(main())
recipe = response.final_output
print(recipe)