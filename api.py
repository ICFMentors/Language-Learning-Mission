from openai import OpenAI


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

# Step 2: Function to simulate NPC interaction
def npc_interaction(player_input):
    """
    Generate an NPC response using OpenAI GPT API with ChatCompletion.
    
    Args:
        player_input (str): The player's input or dialogue.
    
    Returns:
        str: NPC's response.
    """
    try:
        # Use the ChatCompletion API
        response = client.chat.completions.create(model="gpt-4o-mini",  # Use GPT-4 or another available model
        messages=[
            {"role": "system", "content": "You are a medieval NPC in an adventure game. Respond to the player's input in a role-playing manner."},
            {"role": "user", "content": f"Player: {player_input}\nNPC:"}
        ],
        temperature=0.7)  # Slightly higher temperature for creative responses)

        # Extract and return the NPC's response
        npc_response = response.choices[0].message.content.strip()
        return npc_response
    except Exception as e:
        return f"Error during NPC interaction: {e}"

# Step 3: Example usage in a game loop
if __name__ == "__main__":
    print("Welcome to the Adventure Language Game!")

    # while True:
        # Ask the player for input
    player_input = input("You (in Arabic or English): ")

    # Exit condition
    if player_input.lower() in ["exit", "quit"]:
        print("Thank you for playing!")
        #break

    # Option 1: Translate the player's input
    translation = translate_text(player_input, source_language="Arabic", target_language="English")
    print(f"Translated to English: {translation}")

    # Option 2: NPC responds based on the translated input
    npc_response = npc_interaction(translation)
    print(f"NPC: {npc_response}")