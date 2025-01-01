

import gradio as gr
import os
from together import Together
from helper import get_together_api_key,load_env
from dotenv import load_dotenv, find_dotenv


def load_env():
    _ = load_dotenv(find_dotenv())

def save_world(world, filename):
    with open(filename, 'w') as f:
        json.dump(world, f)

def load_world(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_together_api_key():
     load_env()
     together_api_key = os.getenv("TOGETHER_API_KEY")
     return together_api_key

system_prompt = f"""
Your job is to help create interesting fantasy worlds that \
players would love to play in.
Instructions:
- Only generate in plain text without formatting.
- Use simple clear language without being flowery.
- You must stay below 3-5 sentences for each description.
"""

world_prompt = f"""
Generate a creative description for a unique fantasy world with an
interesting concept around language monsters, language monstrosities, and language missions.

Output content in the form:
World Name: <WORLD NAME>
World Description: <WORLD DESCRIPTION>

World Name:"""

client = Together(api_key=get_together_api_key())

output = client.chat.completions.create(
    model="meta-llama/Llama-3-70b-chat-hf",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": world_prompt}
    ],
)

world_output =output.choices[0].message.content
print(world_output)

