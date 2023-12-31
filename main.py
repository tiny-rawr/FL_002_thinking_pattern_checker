import streamlit as st
import json
from collections import Counter
from config import pattern_color_map, tooltip_style
from openai_api import get_distortions, categorise_distortions

def display_app_info():
    st.title("Thought Checker")
    st.markdown("This thought checker will spot unhelpful thinking patterns ([cognitive distortions](https://in.nau.edu/wp-content/uploads/sites/202/Cog.-Distortions.pdf)) in your journal entries for you, so you can focus on the most helpful step: reframing 😭 ➡️ 💪🥰")
    st.markdown("To learn how to leverage genAI to build use-cases like this, sign up to the [fairylights newsletter](https://fairylightsai.substack.com) 💌 & connect on [LinkedIn](https://www.linkedin.com/in/becca9941/) 🥰")

def get_user_journal_entry():
    return st.text_area("Journal entry:", max_chars=2000, height=300)

def highlight_quotes(entry_text, pattern_information):
    processed_entry = entry_text  # Copy of the original entry text
    for pattern_info in pattern_information:
        quote = pattern_info['quote']
        thinking_pattern = pattern_info['thinking pattern']
        explanation = pattern_info['explanation']
        highlight_color = pattern_color_map.get(thinking_pattern, 'yellow')
        tooltip_html = f'<span class="tooltip"><span style="background-color:{highlight_color};">{quote}</span><span class="tooltiptext"><strong>{thinking_pattern}</strong>: {explanation}</span></span>'
        processed_entry = processed_entry.replace(quote, tooltip_html)
    return processed_entry

def generate_highlighted_table(pattern_counter):
    table_html = '<table style="width:100%"><thead><tr><th>Pattern</th><th>Count</th></tr></thead><tbody>'
    table_html += ''.join(
        f'<tr><td style="background-color:{pattern_color_map.get(pattern, "#FFF")}">{pattern}</td><td>{count}</td></tr>'
        for pattern, count in pattern_counter.items())
    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)

def analyze_journal_entry(journal_entry):
    response_message = get_distortions(journal_entry)
    data = json.loads(response_message["function_call"]["arguments"]) if response_message.get("function_call") else {}

    quotes = data.get('quotes', [])
    if not quotes:
        st.success("No cognitive distortions present in the journal entry.")
        return

    # Second API call
    completion = categorise_distortions(quotes)
    response_message = completion["choices"][0]["message"]
    data = json.loads(response_message["function_call"]["arguments"]) if response_message.get("function_call") else {}

    thinking_patterns = data['thinking patterns']
    pattern_counter = Counter([pattern_info['thinking pattern'] for pattern_info in thinking_patterns])
    generate_highlighted_table(pattern_counter)

    entry_with_highlights = highlight_quotes(journal_entry, thinking_patterns)
    st.markdown(tooltip_style, unsafe_allow_html=True)
    st.markdown(entry_with_highlights, unsafe_allow_html=True)

def display_thought_analysis(journal_entry):
    if st.button("Check Thought Patterns"):
        if journal_entry:
            st.info("Journal analysis started. This may take 60-120 seconds to complete.")
            analyze_journal_entry(journal_entry)
        else:
            st.warning("Please enter a journal entry before submitting.")

# Main app logic
display_app_info()
journal_entry = get_user_journal_entry()
display_thought_analysis(journal_entry)