import requests
import json

url = "https://api.openai.com/v1/chat/completions"

# Your OpenAI API key
api_key = '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'

# Create or open buffer.txt for reading and writing conversation history
buffer_file = open("buffer.txt", "a+")
buffer_file.seek(0)
conversation_history = buffer_file.read()

# Set the number of iterations
num_iterations = 10

for _ in range(num_iterations):
    # Get user input from the terminal
    user_input = input("User: ")

    # Append the user message to the conversation history
    conversation_history += f"User: {user_input}\n"

    # Make API request with the entire conversation history
    payload = json.dumps({
        "model": "gpt-3.5-turbo-1106",
        "messages": [{"role": "system", "content": "You are an assistant that provides chess moves."}] +
                    [{"role": "user", "content": msg} for msg in conversation_history.split("\n") if msg.strip()]
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post(url, headers=headers, data=payload)
    response_json = response.json()

    # Extract and print the assistant's reply
    assistant_reply = response_json["choices"][0]["message"]["content"]
    print("Assistant:", assistant_reply)

    # Append the assistant's reply to the conversation history
    conversation_history += f"Assistant: {assistant_reply}\n"

# Update the buffer file with the updated conversation history
buffer_file.seek(0)
buffer_file.write(conversation_history)
buffer_file.truncate()
buffer_file.close()



