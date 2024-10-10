import streamlit as st
from datasets import load_dataset
import os
import hmac
import toml


# Set the page layout to wide
st.set_page_config(layout="wide")

# Get the token from environment variables
token = os.getenv('HUGGINGFACE_TOKEN')

# Load dataset with token
dataset = load_dataset('rntc/first-annotations', split='train', token=token)

# Shuffle the dataset
shuffled_dataset = dataset.shuffle(seed=42)

# Convert to pandas DataFrame
df = shuffled_dataset.to_pandas()

# Rename the column 'educational_score' to 'Quality score'
df.rename(columns={'educational_score': 'quality_score'}, inplace=True)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here
st.title(st.secrets['app']['title'])
st.write(st.secrets['app']['description'])

# Display the current issues as a Markdown to-do list
st.markdown(st.secrets['todo']['list'])

# Display the table in fullscreen
st.dataframe(df, use_container_width=True)

# Display the provided block of Python code with syntax highlighting
st.subheader('Current version of the prompt template')
st.code(st.secrets['code']['block'], language='python')