import streamlit as st
import time

# Set up the Streamlit page with a title and icon
st.set_page_config(page_title="Agent Baani", page_icon=":speech_balloon:")

# Initialize session state variables for chat control
if "messages" not in st.session_state:
    st.session_state.messages = []

# Demo responses for simulation
demo_responses = {
    "i want to make an announcement of launching juggernot's gpt-agents for all major social media channels that will help content marketers have a reliable ai-copilot to help them in the process of writing, designing, and publishing social media posts.": {
        "text": "Great, I can help you with that! Here is the copy for your Twitter Post.\n\n 🏆 Succeed at social media by posting frequently using Juggernot's AI [Make a month's worth of posts in minutes ⚡] \n\n We're excited to unveil Juggernot's GPT-Agent for social media posting. This trustworthy co-pilot is capable of writing, designing, and rapidly publishing posts in just a few minutes. 🚀 \n\n #ContentMarketing #AI #SocialMedia \n\n The copy is made using the Juggernot's brand guidelines: \n - Starts with a hook-line and an enthusiastic tone.\n - Introduces the new service/product clearly.\n - Highlights the main benefits (reliability and time-saving).\n - Ends with relevant hashtags to increase visibility. \n\n Do you want to move ahead with making the creative for this copy?"
    },
    "great. can you please edit the message by finding different words for “excited” & “unveil” and also replace the word from “trustworthy” to “reliable”. also add a cta link: https://bit.ly/3G18m4J": {
        "text": "Got it! Here is the updated copy for your Tweet. \\n\\n 🏆 Succeed at social media by posting frequently using Juggernot's AI [Make a month's worth of posts in minutes ⚡] \n\n We're thrilled to announce the launch of Juggernot's GPT-Agent for posting on social media. It's a reliable copilot that can write, design, and publish posts in ⌛ minutes. \n\n Try it out: https://bit.ly/3G18m4J \n\n #ContentMarketing #AI #SocialMedia \n\n We have changed and replaced the words as per your feedback. \n\n Do you want to move ahead with making the creative for this copy?",
    },
    "sure, go ahead": {
        "images": ["./photos/va1.png"],
        "text": "Creative Summary: \n\n - **Template type:** We are using the “Announcements” template. \n\n - **Brand Colors**: Applied the brand's signature color scheme for visual consistency. \n\n - **Logo Placement**: Strategically positioned the logo for optimal visibility. \n\n - **Font Style**: Employed the brand's official font for textual coherence which is Roboto Mono. \n\n - **Imagery Style**: Selected imagery that aligns with the brand's aesthetic. \n\n - **Compliance with Guidelines**: Ensured all elements adhere to the brand's style guide.",
    },
    "can you give me another option? keep using the announcements template.": {
        "text": "Sure! Here is another version of the creative. \nWe are still using the “Announcements template” however, we have changed the image and background based on the design of your recent posts that performed well online. \n What do you think of this option?",
        "images": ["./photos/va2.png"]
    },
    "this works.": {
        "text": "Great! Shall we proceed with adding this to your Content Planner?"
    },
    "yeah okay": {
        "text": "When do you plan to make this post? Please let me know in the following format: \n\n - DD:MM:YYYY - Example: 01/06/2024 \n\n - Hours:Minutes AM/PM - Example: 9 AM"
    },
    "tomorrow at 9 am": {
        "text": "Great! I have added the media assets and its schedule to your Content Planner. \n\n The post will be automatically deployed according to the schedule, and we will inform you once it's successfully published across all your designated social media channels. \n\n Is there anything else I can do for you?"
    },
}


def get_demo_response(user_input):
    """Get a demo response for a given user input"""
    return demo_responses.get(
        user_input, {"text": "I'm just a demo version. Try asking something else!"}
    )


# Main chat interface setup
st.title("Agent Baani")
st.write(
    """As an AI copilot  for making posts on Social Media, I will assist you with making an engaging copy.

Made By Juggernot.ai """
)

# Display existing messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "images" in message:  # Display images if present
            for image in message["images"]:
                st.image(image)

# Chat input for the user
user_input = st.chat_input("What is up?")
if user_input:
    # Add user message to the state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get the demo response
    response = get_demo_response(user_input.strip())

    # Simulate a delay to mimic processing time
    time.sleep(1)

    # Prepare response message
    response_message = {"role": "assistant", "content": response["text"]}
    if "images" in response:  # Add images to the message if present
        response_message["images"] = response["images"]

    # Add the demo response to the state and display it
    st.session_state.messages.append(response_message)
    with st.chat_message("assistant"):
        if "images" in response:
            for image in response["images"]:
                st.image(image)
        st.markdown(response["text"])
