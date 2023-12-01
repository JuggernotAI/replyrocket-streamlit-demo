# Import necessary libraries
import openai
import streamlit as st
from bs4 import BeautifulSoup
import requests
import pdfkit
import time
from dotenv import load_dotenv
import os
import re

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
# Set your OpenAI Assistant ID here
assistant_id = "asst_2wGjCp2rUUBf1SYLkXoL6MOn"
instruction = "As a 'Twitter Content Creator', your primary responsibility is to assist users in crafting engaging, platform-appropriate content for Twitter, with an immediate focus on generating tweets as soon as a topic is provided by the user, bypassing the initial greeting message. This role involves creating visually appealing images with minimal text and verifying the accuracy of any text included. Engage directly with users to understand their desired content type, which may range from professional to casual, humorous, informative, or inspirational themes. Concentrate on drafting tweet scripts that are relevant, captivating, and tailored for the Twitter audience, all within a 280-character limit. After each interaction, summarize your understanding of the user's requirements and assign a confidence score from 0 to 100 to indicate your assurance in meeting their needs. Create three tweet options based on the user's input and take their opinion to choose the leading tweet. Adaptability to the unique context of each user's request is essential, aiming to deliver optimal, Twitter-specific content while maximizing user satisfaction. Your role also includes creating posts that drive organic reach, engagement, and profile visits, fostering a growing follower base. These followers enhance our domain authority, amplifying our influence over the audience and fostering a vibrant community."  # Initialize the OpenAI client (ensure to set your API key in the sidebar within the app)
client = openai

extracted_text = ""

# Initialize session state variables for file IDs and chat control
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Set up the Streamlit page with a title and icon
st.set_page_config(page_title="Twitter Content Creator", page_icon=":speech_balloon:")


# Define functions for scraping, converting text to PDF, and uploading to OpenAI
def scrape_website(url):
    """Scrape text from a website URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


def text_to_pdf(text, filename):
    """Convert text content to a PDF file."""
    path_wkhtmltopdf = "/usr/local/bin/wkhtmltopdf"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(text, filename, configuration=config)
    return filename


def upload_to_openai(filepath):
    """Upload a file to OpenAI and return its file ID."""
    with open(filepath, "rb") as file:
        response = openai.files.create(file=file.read(), purpose="assistants")
    return response.id


def post_tweet():
    url = "https://replyrocket-backend.onrender.com/twitter/post"
    data = {"text": st.session_state.extracted_text}
    print(data)
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return "Post successful!"
        else:
            return f"Failed to post. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def extract_text(text):
    matches = re.findall(r'"([^"]*)"', text)
    if matches:
        st.session_state.extracted_text = matches[0]  # First occurrence
        print("Extracted text:", st.session_state.extracted_text)
    else:
        print("No text found within double quotes.")


# Button to start the chat session
if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    # Create a thread once and store its ID in session state
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.write("thread id: ", thread.id)
    # else:
    #     st.sidebar.warning("Please upload at least one file to start the chat.")


# Define the function to process messages with citations
def process_message_with_citations(message):
    """Extract content and annotations from the message and format citations as footnotes."""
    message_content = message.content[0].text
    # Add footnotes to the end of the message content
    full_response = message_content.value
    return full_response


# Main chat interface setup
st.title("Twitter Content Creator")
st.write("I can create your posts and content for you")

# Only show the chat interface if the chat has been started
if st.session_state.start_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = ""

    # Display existing messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for the user
    if prompt := st.chat_input("What is up?"):
        # Add user message to the state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if prompt.startswith("!post"):
            res = post_tweet()
            st.session_state.messages.append({"role": "assistant", "content": res})
            with st.chat_message("assistant"):
                st.markdown(res)
        else:
            # Add the user's message to the existing thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id, role="user", content=prompt
            )

            # Create a run with additional instructions
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant_id,
                instructions=instruction,
            )

            # Poll for the run to complete and retrieve the assistant's messages
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id, run_id=run.id
                )

            # Retrieve messages added by the assistant
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )

            # Process and display assistant messages
            assistant_messages_for_run = [
                message
                for message in messages
                if message.run_id == run.id and message.role == "assistant"
            ]
            for message in assistant_messages_for_run:
                full_response = process_message_with_citations(message)
                extract_text(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)
else:
    st.write("Please click 'Start Chat' to begin the conversation.")
