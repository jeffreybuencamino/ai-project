import streamlit as st
import pandas as pd
import os, requests, asyncio
from bs4 import BeautifulSoup
from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

st.set_page_config(
    page_title='Contact Info Extraction',
    layout='wide',    
)

st.title('Contact Info Extraction from Web Page')
st.write("This app extracts contact information (phone and email) from a given web page URL.")

with st.sidebar:
    st.header("Configuration")
    agent_name = st.text_input("Agent Name", "ContactInfoExtractor")
    agent_instructions = st.text_area("Agent Instructions",
        "You are an agent for extracting phone numbers and emails. You will be given a URL of a website to scrape information using the get_url_content tool you are given. "
        "Your job is to use the information given from the get_url_content tool, and output the contact information in an organized manner. "
        "## Notes: The tool will give you unstructured text, so you will need to use your knowledge of phone numbers and emails to extract them."
    )
    model_options = [
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-3.5-turbo"
    ]

    selected_model = st.selectbox("Select Model", model_options, index=0)

    demo_options = [
        "https://www.exotictreatment.net/contact/",
        "https://www.premier-soccertraining.com/contact-us/",
        "https://www.chewy.press/"
    ]

    demo_prompt = st.selectbox("Select Demo URL", demo_options, index=1)

    st.markdown("Gangsta Mode")

user_input = st.text_input("Enter the URL to scrape for contact information:", value=demo_prompt)
send_button = st.button("Extract Contact Info")

response_container = st.container()

async def stream_response(extraction_agent: Agent, user_input: str):
    response_parts = ''
    message_placeholder = st.empty()
    try:
        result = Runner.run_streamed(extraction_agent, input=user_input)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta)
                response_parts += event.data.delta
                # Update the UI with a trailing cursor symbol for a live effect
                message_placeholder.markdown(response_parts + "▌")
        message_placeholder.markdown(response_parts)
    except Exception as e:
        st.error(f"An error occurred: {e}")




if send_button and user_input and selected_model:
    # Indented block starts here

    class ContactInfo(BaseModel):
        phone: str
        email: str

    @function_tool
    def get_url_content(url: str) -> str:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Request was successful! {response.status_code}")
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text(strip=True)
        else:
            raise ValueError(f"Request failed with status code: {response.status_code}")

    extraction_agent = Agent(
        name=agent_name,
        instructions=agent_instructions,
        tools=[get_url_content],
        model=selected_model,
        output_type=ContactInfo
    )

    with response_container:
        st.write("Thinking...")
        asyncio.run(stream_response(extraction_agent, user_input))

        #---Add clear button ----
        if st.button("Clear"):
            st.empty()