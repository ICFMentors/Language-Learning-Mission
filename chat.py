import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import os

openai.api_key  = os.getenv('OPENAI_API_KEY')

# Set your OpenAI API key
  # Replace with your actual API key
client = OpenAI(api_key=openAI_API)


# Step 1: Function to translate text
def translate_text(text, source_language="Arabic", target_language="English"):
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
        response = client.chat.completions.create(model="gpt-4o-mini",  # Use GPT-4 or another available model
        messages=[
            {"role": "system", "content": f"You are a professional translator from {source_language} to {target_language}"},
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
