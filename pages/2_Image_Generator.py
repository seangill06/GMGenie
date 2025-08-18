import streamlit as st
import openai
import os

# --- This sets the browser tab title, icon, and layout ---
st.set_page_config(
    page_title="GM Genie - AI-Powered Quest Generator",
    page_icon="🔮",  # You can use an emoji or a URL to an image file
    initial_sidebar_state="expanded"
)

# --- This is the new counter for images ---
if 'image_count' not in st.session_state:
    st.session_state.image_count = 0

IMAGE_FREE_LIMIT = 3 # You can adjust this number

# --- This section is for Stripe verification and business information ---
col1, col2 = st.columns([1, 4]) # Create two columns, with the second one being wider

with col1:
    st.image("images/logo.png", width=200) # Use the correct path to your image and adjust the width

with col2:
    st.header("Digital Anvil Designs")
    st.markdown("Your home for premium, AI-powered tools for tabletop role-playing games.")

st.markdown("---")

st.subheader("Unlock Unlimited AI Quests!")
st.markdown("Upgrade to a **GM Genie Pro** subscription to get unlimited quests, remove the free-tier limitations, and support future development.")
st.link_button("🚀 Subscribe Now!", "https://buy.stripe.com/dRm00ld9FdA2fgWc2kgjC02")

# Set your OpenAI API key from environment variables or Streamlit secrets
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key is missing. Please set it in Streamlit Secrets.")

# Initialize the OpenAI client with the key
client = openai.OpenAI(api_key=openai_api_key)

st.title("Image Generator")
st.markdown("Create a custom image for your quest!")

# --- Check if the user is at the image limit ---
if st.session_state.image_count < IMAGE_FREE_LIMIT or DEV_MODE:
    # The form and API call for image generation
    with st.form("image_form"):
        image_prompt = st.text_area("Image Prompt", "An adventurer standing on a cliff, looking at a dragon's lair")
        submit_image_button = st.form_submit_button("Generate Image")

    if submit_image_button:
            # The API call for image generation
            st.session_state.image_count += 1
            with st.spinner("Generating your image..."):            
                try:
                    image_response = client.images.generate(
                        model="dall-e-3",
                        prompt=image_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                image_url = image_response.data[0].url
                st.image(image_url, caption=image_prompt)
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.warning(f"You have reached the free limit of {IMAGE_FREE_LIMIT} images. Subscribe for unlimited image generation!")
    st.link_button("🚀 Subscribe Now!", "https://buy.stripe.com/dRm00ld9FdA2fgWc2kgjC02")