import streamlit as st
import openai
import json
import os

def highlight_quotes(journal_entry, thinking_patterns):
    for pattern, details in thinking_patterns.items():
        for detail in details:
            quote = detail["quote"]
            explanation = detail["explanation"]
            highlighted = f'<span style="background-color: yellow;" title="{explanation}">{quote}</span>'
            journal_entry = journal_entry.replace(quote, highlighted)
    return journal_entry

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Thought Checker App")
st.write("This app will highlight different thinking patterns (cognitive distortions) present in your journal that can do with a bit of reframing. Hover over the highlighted text to find out more about the thinking pattern.")

journal_entry = st.text_area("Journal entry:", max_chars=2000, height=300)

# Submit button
if st.button("Check Thought Patterns"):
    if journal_entry:
        # Display the submitted entry
        st.write("Your journal entry:")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant who extracts examples of all of the cognitive distortions present in a journal entry. Use direct quotes."},
                {"role": "user", "content": journal_entry}
            ],
            functions=[{
                "name": "get_thinking_patterns",
                "description": "Get direct examples of thinking patterns that are present in a journal entry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Black or white thinking": {
                            "type": "array",
                            "description": "This thinking pattern involves viewing situations or events in extreme, polarized terms with no middle ground.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Overgeneralisation": {
                            "type": "array",
                            "description": "Making sweeping conclusions based on a single event or a limited set of experiences.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Mental filter": {
                            "type": "array",
                            "description": "This distortion involves selectively focusing on negative details while ignoring positive ones. It's like looking at life through a 'negative filter' that magnifies flaws and diminishes achievements or positive aspects of a situation.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Discounting the positives": {
                            "type": "array",
                            "description": "People with this distortion tend to downplay or dismiss positive experiences, believing that they don't 'count' or are insignificant. They might attribute positive outcomes to luck or external factors rather than their own abilities.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Mind reading": {
                            "type": "array",
                            "description": "Assuming you know what others are thinking and that they have negative thoughts or judgments about you.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Fortune telling": {
                            "type": "array",
                            "description": "Making negative predictions about future events without concrete evidence.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Catastrophising": {
                            "type": "array",
                            "description": "This distortion involves exaggerating the importance of negative events (magnification) or minimizing the significance of positive events (minimization).",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Emotional reasoning": {
                            "type": "array",
                            "description": "In this distortion, individuals believe that their emotions are accurate reflections of reality. For example, if they feel anxious about a situation, they assume it must be dangerous, even if there's no objective evidence to support that belief.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Should statements": {
                            "type": "array",
                            "description": "People who engage in should statements have rigid, unrealistic expectations for themselves and others. They often use words like 'should', 'must', or 'ought to', and when these expectations aren't met, they feel frustration, guilt, or anger.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Labelling": {
                            "type": "array",
                            "description": "Labeling involves attaching negative labels to oneself or others based on specific behaviors or mistakes. Mislabeling is a form of overgeneralization, where someone assigns a global, negative label to themselves or others based on a single incident.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                        "Blame": {
                            "type": "array",
                            "description": "Blame involves attributing the responsibility for negative events solely to others or external factors, while denying your own role or responsibility in the situation. This can lead to resentment and a lack of personal accountability.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "quote": {"type": "string"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "In 200 words, explain why the quote demonstrates the thinking pattern."
                                    }
                                },
                                "required": ["quote", "explanation"]
                            }
                        },
                    },
                    "required": ["Black or white thinking", "Overgeneralisation", "Mental filter",
                                 "Discounting the positives", "Mind reading", "Fortune telling", "Catastrophising",
                                 "Emotional reasoning", "Should statements", "Labelling", "Blame"]
                }
            }
            ],
            function_call={"name": "get_thinking_patterns"}
        )

        response_message = completion["choices"][0]["message"]
        if response_message.get("function_call"):
            thinking_patterns = json.loads(response_message["function_call"]["arguments"])

        highlighted_entry = highlight_quotes(journal_entry, thinking_patterns)
        st.markdown(highlighted_entry, unsafe_allow_html=True)
    else:
        st.warning("Please enter a journal entry before submitting.")