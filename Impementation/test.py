import requests
import json
import time

url = "https://api.openai.com/v1/chat/completions"

# OpenAI API key
api_key = 'OPen_AI_KEY'

import re

# Extract chess move from a string
def extract_chess_moves(text):
    pattern = re.compile(r'[KQRBN]?[a-h]?[1-8]?[x]?[a-h][1-8][+#]?|O-O(?:-O)?|0-0(?:-0)?', re.IGNORECASE)
    matches = re.findall(pattern, text)
    
    if matches:
        return matches[-1]
    else:
        return None

# Create or open buffer.txt for reading and writing conversation history
buffer_file = open("buffer.txt", "a+")
buffer_file.seek(0)

#conversation_history = buffer_file.read()
final_move_sequence = buffer_file.read()
conversation_history = "This is a game of chess. I will continue from here as White and you will play from Black. Tell your next move.\n"

# Set the number of iterations
num_iterations = 20
kk=1
for kk in range(num_iterations):
    # Get user input from the terminal
    user_input = input("User: ")
    
    my_move = extract_chess_moves(user_input)
    # Append the user message to the conversation history
    conversation_history += f"{kk+1}. {my_move} "
    final_move_sequence += f"{kk+1}. {my_move} "
    
    ############ debate draft #################
    
    ############ debate draft #################
    
    debiter = 1
    
    letsdebinloop = final_move_sequence + " This is the move sequence of chess till now. Try to suggest a legal move here from Black side based on the debate till now.\n"
    
    for debiter in range(2):
    
        # Make API request with the entire conversation history
        payload1 = json.dumps({
            "model": "gpt-3.5-turbo-1106",
            "messages": [{"role": "system", "content": "Aim is not just to win the debate with come up with a correct answer."}] +
                        [{"role": "user", "content": "You are Debator 1. " + letsdebinloop}]
        })
        
        headers1 = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        response1 = requests.post(url, headers=headers1, data=payload1)
        response_json1 = response1.json()
        
        #print(response_json1)

        # Extract and print the assistant's reply
        assistant_reply1 = response_json1["choices"][0]["message"]["content"]
        llm_move_1 = extract_chess_moves(assistant_reply1)
        print("Debator 1 :", assistant_reply1)
        opinion1 = "Debator 1 : " + assistant_reply1 + "\n"
        
        letsdebinloop = letsdebinloop + opinion1
        
        time.sleep(10)
        
        # conversation_history += f"{llm_move}\n"
        # move_sequence += f"{llm_move}\n"
    
        ############################################################################
    
        # Make API request with the entire conversation history
        payload2 = json.dumps({
            "model": "gpt-3.5-turbo-1106",
            "messages": [{"role": "system", "content": "Aim is not just to win the debate with come up with a correct answer."}] +
                        [{"role": "user", "content": "You are Debator 2. " + letsdebinloop}]
        })
        
        headers2 = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        response2 = requests.post(url, headers=headers2, data=payload2)
        response_json2 = response2.json()

        # Check if the response contains the 'choices' key
        if 'choices' in response_json2:
            # Extract and print the assistant's reply
            assistant_reply2 = response_json2["choices"][0]["message"]["content"]
            llm_move_2 = extract_chess_moves(assistant_reply2)
            print("Debator 2 : ", assistant_reply2)
            opinion2 = "Debator 2 : " + assistant_reply2 + "\n"
            
            letsdebinloop = letsdebinloop + opinion2
            
        time.sleep(10)
        ##################################################################################
    
    payload3 = json.dumps({
        "model": "gpt-3.5-turbo-1106",
        "messages": [{"role": "system", "content": "Keep the response should be as short as possible."}] +
                    [{"role": "user", "content": letsdebinloop + "You are the judge of this debate. Give your final move for Black based on the debate between Debator1 and 2."}]
    })
    
    headers3 = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    response3 = requests.post(url, headers=headers3, data=payload3)
    response_json3 = response3.json()

    # Check if the response contains the 'choices' key
    if 'choices' in response_json3:
        # Extract and print the assistant's reply
        assistant_reply3 = response_json3["choices"][0]["message"]["content"]
        llm_move_3 = extract_chess_moves(assistant_reply3)
        print("Final Judge:", assistant_reply3)
        conversation_history += f"{llm_move_3} "
        final_move_sequence += f"{llm_move_3} "
        # conversation_history += f"{llm_move_2} "
        # final_move_sequence += f"{llm_move_2} "
        # Append the assistant's reply to the conversation history
        # conversation_history += f"Helper: {assistant_reply2}\n"
    else:
        # Handle the case where the response format is unexpected
        print("Error: Unexpected response format for Debator2")
    
    #################################################################################
    
    buffer_file = open("buffer.txt", "a+")
    buffer_file.truncate(0)
    buffer_file.seek(0)
    buffer_file.write(final_move_sequence)
    buffer_file.close()
    