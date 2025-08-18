import streamlit as st
import openai
import os

# Set your OpenAI API key from environment variables or Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

if not openai_api_key:
    st.error("OpenAI API key is missing. Please set it in Streamlit Secrets.")
    st.stop()

# Initialize the OpenAI client with the key
client = openai.OpenAI(api_key=openai_api_key)

st.title("GM Genie: AI-Powered Quest Generator")
st.write("Your creative co-pilot for legendary quests. Just give me a few details, and I'll whip up an adventure for your players!")

# Input fields for the GM to customize the quest
with st.form("quest_form"):
    quest_theme = st.text_input("Quest Theme", "A forgotten library, a mischievous spirit, and a missing artifact")
    player_levels = st.text_input("Player Levels", "3-5")
    quest_type = st.selectbox("Quest Type", ["Mystery", "Dungeon Crawl", "Social Intrigue", "Escort Quest"])
    
    submitted = st.form_submit_button("Conjure Quest!")

# When the button is clicked, generate the quest
if submitted:
    with st.spinner("The Genie is hard at work..."):
        try:
            # Our custom prompt, with user inputs
            prompt = f"""
            You are a master Dungeon Master's assistant, an expert at creating engaging and unique Dungeons & Dragons quests. Your task is to generate a detailed quest outline.

            Here are the specific requirements:
            - **Quest Title:**
            - **Quest Giver:**
            - **Quest Type:** {quest_type}
            - **Setting/Theme:** {quest_theme}
            - **Player Level:** {player_levels}
            - **Key NPCs:** (at least 2, a friendly one and a suspicious one)
            - **Primary Conflict:** (the main problem)
            - **Three-Act Structure:**
                * **Act 1: The Hook:** How do the players get involved?
                * **Act 2: The Rising Action:** What challenges do they face? Include a puzzle, a combat encounter, and a social challenge.
                * **Act 3: The Climax:** What is the final confrontation?
            - **Reward:** (e.g., gold, a magic item, a favor)
            - **Optional: Plot Twist:** A short, unexpected reveal that can surprise the players.

            Please generate a detailed and inspiring quest based on the requirements above. The output should be a well-formatted narrative clearly labeled with each section.
            """

            # Call the OpenAI API
            response = client.chat.completions.create(  
                model="gpt-4o-2024-11-20",  # Using the model we decided on
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Dungeon Masters."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )

            # Display the generated text
            st.markdown("---")
            st.subheader("Your Quest:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"An error occurred: {e}")