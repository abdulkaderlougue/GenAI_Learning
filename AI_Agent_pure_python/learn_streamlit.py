
import streamlit as st
from PIL import Image


st.set_page_config(page_title="Learning Streamlit", page_icon="🤖"
                   , layout="wide", initial_sidebar_state="expanded")
title = "AI Agent with Tools"
description = "An AI agent that can use tools to perform tasks."
st.title(title)
st.header("This is a header", anchor=None, help="This is a help text") 
st.subheader("This is a subheader")
st.text("This using st.text to display plain text")
st.write(description)

st.markdown("## This is a markdown")
st.markdown("You can use **Markdown** to format text.")

st.success("Success")

st.info("Information")

st.warning("Warning")

st.error("Error")

exp = ZeroDivisionError("Trying to divide by Zero")
st.exception(exp)

st.write("st.write() that can display text, numbers, data structures and even charts")
st.write(range(10),[1,2,3,4,5],{'raw': True, 'expanded': True})
st.code("print('Hello, Streamlit!')", language="python")
st.json({"name": "Streamlit", "type": "Library", "language": "Python"})

path = "C:/Users/user/Proline/pics/going-to-europe.jpg"
img = Image.open(path)
st.image(img, caption="Europe Players Image", width=500, use_column_width=None)
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
st.video("https://www.youtube.com/watch?v=JwSS70SZdyM")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")


# Widgets
st.header("Widgets")    
st.button("Click Me")

if st.button("Press Me"):
    st.write("Button Pressed!")

if st.checkbox("Show/Hide"):
    st.write("Checkbox is checked!")


st.slider("Select a range of values", 0, 100, (25, 75))
st.download_button("Download", data="Hello, Streamlit!", file_name="hello.txt", mime="text/plain")
st.checkbox("Check Me")
st.radio("Choose one", ("Option 1", "Option 2", "Option 3"))
st.selectbox("Select one", ("Option A", "Option B", "Option C"))

st.multiselect("Select multiple", ("Choice 1", "Choice 2", "Choice 3"))


st.text_input("Enter your name", max_chars=20, help="Your full name", placeholder="John Doe")
st.text_area("Enter your address", height=100, max_chars=200, help="Your full address", placeholder="123 Main St, City, Country")
st.number_input("Enter your age", min_value=0, max_value=120, value=20, step=1)
st.time_input("Select a time")
selected_date = st.date_input("Select a date")
st.info(f"You selected: {selected_date}")
st.color_picker("Pick a color", "#00f900")
# forms
with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider", 0, 100, 50)
    checkbox_val = st.checkbox("Form checkbox")
    st.text_input("First Name", max_chars=10, help="Enter your first name", placeholder="John", key="name", type="default",
                  label_visibility="visible", disabled=False)
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Form submitted!")
        st.write(f"Slider value: {slider_val}, Checkbox value: {checkbox_val}")

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')
right_column.button('Press me2!')

with st.sidebar:
    st.header("About Us")
    st.text("This is a sidebar")
    st.button("Sidebar Button")

import time

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'