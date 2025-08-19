import streamlit as st

# --- This sets the browser tab title, icon, and layout ---
st.set_page_config(
    page_title="GM Genie - AI-Powered Quest Generator",
    page_icon="🔮",  # You can use an emoji or a URL to an image file
    initial_sidebar_state="expanded"
)

# --- This section is for Stripe verification and business information ---
col1, col2 = st.columns([1, 4]) # Create two columns, with the second one being wider

with col1:
    st.image("images/logo.png", width=400) # Use the correct path to your image and adjust the width

with col2:
    st.header("Digital Anvil Designs")
    st.markdown("Your home for premium, AI-powered tools for tabletop role-playing games.")
    st.write("Choose tool from left sidebar to get started")

st.markdown("---")

st.subheader("Unlock Unlimited AI Quests!")
st.markdown("Upgrade to a **GM Genie Pro** subscription to get unlimited quests, remove the free-tier limitations, and support future development.")
st.link_button("🚀 Subscribe Now!", "https://buy.stripe.com/dRm00ld9FdA2fgWc2kgjC02")
