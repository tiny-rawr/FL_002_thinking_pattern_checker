import streamlit as st


st.title("Thought Checker App")
st.write("This app will highlight different thinking patterns (cognitive distortions) present in your journal that can do with a bit of reframing. Hover over the highlighted text to find out more about the thinking pattern.")

journal_entry = st.text_area("Journal entry:", max_chars=2000, height=300)

# Submit button
if st.button("Check Thought Patterns"):
    if journal_entry:
        # Display the submitted entry
        st.write("Your journal entry:")
        st.write(journal_entry)
    else:
        st.warning("Please enter a journal entry before submitting.")