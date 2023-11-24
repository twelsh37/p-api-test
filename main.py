from dotenv import load_dotenv
import os
import requests
import pprint

load_dotenv()


def load_api_key():
    return os.getenv('API_KEY')


def model_selection(model):

    # Print keys and values
    output = ""
    for key, value in model.items():
        output += f"{key + 1}: {value}\n"
    print(output)

    # Get user selection
    selected_key = int(input("Enter the key of the model you want to select: "))
    while selected_key not in model:
        print("Invalid key. Please try again.")
        selected_key = int(input("Enter the key of the model you want to select: "))
    selected_model = model[selected_key]

    return selected_model


def user_question():
    return input('What is your question? ')


def main():

    load_api_key()

    # The URL to the API service
    url = "https://api.perplexity.ai/chat/completions"

    # our models
    model = {0: 'codellama-34b-instruct', 1: 'llama-2-70b-chat', 2: 'mistral-7b-instruct', 3: 'openhermes-2-mistral-7b',
             4: 'openhermes-2.5-mistral-7b', 5: 'pplx-7b-chat-alpha', 6: 'pplx-70b-chat-alpha'}

    payload = {
        #"model": "mistral-7b-instruct",
        "model": model_selection(model),
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": user_question()
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer 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"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Get the content as a JSON object
    json_data = response.json()

    answer = json_data['choices'][0]['message']['content']

    # Now you can access specific parts of the response
    print(f'Answer: {answer}')



if __name__ == '__main__':
    main()
