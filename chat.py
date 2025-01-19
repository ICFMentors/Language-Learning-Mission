import gradio as gr
#from openai import OpenAI
import openai
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv()) # read local .env file
#openAI_api_key = os.environ('OPENAI_API_KEY')
openai.api_key = os.environ['OPENAI_API_KEY']

# Set your OpenAI API key
  # Replace with your actual API key
client = openai #OpenAI(api_key=openAI_api_key)


# Step 1: Function to translate text
def translate_text(text, source_language="English", target_language="Arabic", age=12):
    """
    Translate text using OpenAI ChatCompletion API.
    
    Args:
        text (str): The text to translate.
        source_language (str): Source language of the text.
        target_language (str): Target language for translation.
    
    Returns:
        str: The translated text.
    """
    print(f"Translate the following from {source_language} to {target_language}: {text}")
    
    try:
        # API call using ChatCompletion
        response = client.ChatCompletion.create(model="gpt-4o-mini",  # Use GPT-4 or another available model
        messages=[
            {"role": "system", "content": f"You are an NPC in a language learning game who translates from {source_language} to {target_language}. talk to the user in their source language and talk to them as if they are {age} years old. give the player advice on their grammar."},
            {"role": "assistant", "content": f"Hello traveller! How can I help you?"},
            {"role": "user", "content": f"Translate the following from {source_language} to {target_language}: {text}"}
            #{"role": "user", "content": f"Translate the following English text to Spanish: Hi, I would like to order a blender"}
        ],  # Closing the list of messages
        temperature=0.3)  # Lower temperature for accurate translation)  # Properly closing the function call

        # Extract the translated text
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error during translation: {e}"

demo = gr.Interface(fn=translate_text, inputs="textbox", outputs="textbox")

if __name__ == "__main__":
    demo.launch()
