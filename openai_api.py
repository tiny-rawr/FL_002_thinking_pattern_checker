import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_distortions(journal_entry):
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

    return completion["choices"][0]["message"]


def categorise_distortions(quotes):
    return openai.ChatCompletion.create(
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
                                                 "Fortune telling", "Mind reading", "Blaming",
                                                 "Catastrophising",
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