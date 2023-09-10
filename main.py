import streamlit as st
import openai
import json
import os
from collections import Counter


pattern_color_map = {
    "Black or white thinking": "#FFD1DC",  # Pastel Pink
    "Overgeneralisation": "#FFD1A1",  # Pastel Orange
    "Mental filter": "#FFFFA1",  # Pastel Yellow
    "Discounting the positives": "#A1FFA1",  # Pastel Green
    "Mind reading": "#A1FFFF",  # Pastel Blue
    "Fortune telling": "#D1A1FF",  # Pastel Purple
    "Catastrophising": "#D3D3D3",  # Pastel Grey
    "Emotional reasoning": "#A1FFD1",  # Pastel Cyan
    "Should statements": "#FFA1FF",  # Pastel Magenta
    "Labelling": "#D2B48C",  # Pastel Brown
    "Blaming": "#C0FF3E"  # Pastel Lime
}


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


tooltip_style = '''
<style>
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 300px;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 125%; /* Position the tooltip above the text */
  left: 50%;
  margin-left: -150px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
'''

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Thought Checker")
st.markdown("This thought checker will spot unhelpful thinking patterns ([cognitive distortions](https://in.nau.edu/wp-content/uploads/sites/202/Cog.-Distortions.pdf)) in your journal entries for you, so you can focus on the most helpful step: reframing 😭 ➡️ 💪🥰")
st.markdown("To learn how to leverage genAI to build use-cases like this, sign up to the [fairylights newsletter](https://fairylightsai.substack.com) 💌 & connect on [LinkedIn](https://www.linkedin.com/in/becca9941/) 🥰")
journal_entry = st.text_area("Journal entry:", max_chars=2000, height=300)


# Submit button
if st.button("Check Thought Patterns"):
    if journal_entry:
        start_time = time.time()
        st.info("Journal analysis started. This may take 60-120 seconds to complete.")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant who goes through each sentence and extracts every single example of cognitive distortions present in a journal entry. Use direct quotes."},
                {"role": "user", "content": journal_entry}
            ],
            functions=[{
                "name": "identify_cognitive_distortions",
                "description": "Identifies all cognitive distortion present in a journal entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "quotes": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A direct quote from the journal entry that represents a cognitive distortion"
                            }
                        }
                    },
                    "required": ["quotes"]
                }
            }]
        )

        response_message = completion["choices"][0]["message"]
        if response_message.get("function_call"):
            data = json.loads(response_message["function_call"]["arguments"])

        quotes = data['quotes']

        # Step 2: Categorize quotes by cognitive distortions and explain why each quote is an example of that thinking pattern
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant who categorizes cognitive distortions and explains why they are an example of that cognitive distortion"},
                {"role": "user", "content": str(quotes)}
            ],
            functions=[
                {
                    "name": "identify_cognitive_distortions",
                    "description": "Categorizes quotes by cognitive distortions and explains why each quote is an example of that thinking pattern.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "thinking patterns": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "quote": {
                                            "type": "string",
                                            "description": "A direct quote from the journal entry that most represents this thinking pattern"
                                        },
                                        "thinking pattern": {
                                            "type": "string",
                                            "enum": ["Black or white thinking", "Overgeneralisation", "Labelling",
                                                     "Fortune telling", "Mind reading", "Blaming", "Catastrophising",
                                                     "Discounting the positives", "Emotional reasoning"]
                                        },
                                        "explanation": {
                                            "type": "string",
                                            "description": "Explain why this is an example of the thinking pattern."
                                        }
                                    },
                                    "required": ["quote", "thinking pattern", "explanation"]
                                }
                            }
                        },
                        "required": ["thinking patterns"]
                    }
                }
            ]
        )

        response_message = completion["choices"][0]["message"]
        if response_message.get("function_call"):
            data = json.loads(response_message["function_call"]["arguments"])

        thinking_patterns = data['thinking patterns']

        pattern_counter = Counter([pattern_info['thinking pattern'] for pattern_info in thinking_patterns])

        # Generate and display the table with colored cells
        table_html = '<table style="width:100%"><thead><tr><th>Pattern</th><th>Count</th></tr></thead><tbody>'
        table_html += ''.join(
            f'<tr><td style="background-color:{pattern_color_map.get(pattern, "#FFF")}">{pattern}</td><td>{count}</td></tr>'
            for pattern, count in pattern_counter.items())
        table_html += '</tbody></table>'
        st.markdown(table_html, unsafe_allow_html=True)

        entry_with_highlights = highlight_quotes(journal_entry, thinking_patterns)
        st.markdown(tooltip_style, unsafe_allow_html=True)  # Add the tooltip style
        st.markdown(entry_with_highlights, unsafe_allow_html=True)

    else:
        st.warning("Please enter a journal entry before submitting.")
