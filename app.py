import streamlit as st
import openai
import os

# --- This sets the browser tab title, icon, and layout ---
st.set_page_config(
    page_title="GM Genie - AI-Powered Quest Generator",
    page_icon="🔮",  # You can use an emoji or a URL to an image file
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- This section is for Stripe verification and business information ---
st.header("Digital Anvil Designs")
st.markdown("Your home for premium, AI-powered tools for tabletop role-playing games.")
st.markdown("---")

# Initialize session state for the quest counter
if 'quest_count' not in st.session_state:
    st.session_state.quest_count = 0

FREE_LIMIT = 3 # You can adjust this number
DEV_MODE = os.getenv("IS_DEV_MODE") == "True"

# --- The button to subscribe to your service ---
st.link_button("🚀 Get Unlimited Quests!", "https://buy.stripe.com/fZu28td9FgMe1q63vOgjC00")

# Set your OpenAI API key from environment variables or Streamlit secrets
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key is missing. Please set it in Streamlit Secrets.")
    st.stop()

# Initialize the OpenAI client with the key
client = openai.OpenAI(api_key=openai_api_key)

st.title("GM Genie: AI-Powered Quest Generator")
st.write("Your creative co-pilot for legendary quests. Just give me a few details, and I'll whip up an adventure for your players!")

# Check if the user is a subscriber (for now, we'll check the quest count)
if st.session_state.quest_count < FREE_LIMIT or DEV_MODE:
    # --- This is where the quest generation form starts ---
    with st.form("quest_form"):
        # The form content (all of your inputs)
        ... (your existing input code goes here) ...
        # The generate button is a form submit button
        submit_button = st.form_submit_button("Generate Quest")

    if submit_button:
        st.session_state.quest_count += 1
        with st.spinner("Generating your quest..."):
            try:
                # The code that generates the quest
                ... (your existing API call code goes here) ...
                # The code that displays the quest
                ... (your existing display code goes here) ...
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    # --- This is the paywall message ---
    st.warning(f"You have reached the free limit of {FREE_LIMIT} quests. Please subscribe for unlimited access!")

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