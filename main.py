import os
import requests
import json
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

# Set up a list to store the conversation context
context: List[Dict[str, str]] = []


def load_context_from_file() -> None:
    """
    Load the conversation context from a .plx file if it exists.
    """
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.plx')]
    if files:
        print("Available .plx files:")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file}")
        while True:
            try:
                selected_key = int(input("Enter the key of the file you want to load (or 0 to skip): ")) - 1
                if selected_key == -1:
                    break
                with open(files[selected_key], 'r') as f:
                    global context
                    context = json.load(f)
                break
            except (ValueError, KeyError, IndexError):
                print("Invalid key. Please try again.")


def save_context_to_file() -> None:
    """
    Save the conversation context to a .plx file.
    """
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.plx')]
    if files:
        print("Available .plx files:")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file}")
        while True:
            try:
                selected_key = int(
                    input("Enter the key of the file you want to save to (or 0 to save to a new file): ")) - 1
                if selected_key == -1:
                    filename = input("Enter a new filename for the .plx file (without the extension): ")
                else:
                    filename = files[selected_key].rsplit('.', 1)[0]
                break
            except (ValueError, KeyError, IndexError):
                print("Invalid key. Please try again.")
    else:
        filename = input("Enter a new filename for the .plx file (without the extension): ")
    with open(f"{filename}.plx", 'w') as f:
        json.dump(context, f)


def load_api_key() -> str:
    """
    Load the API key from the .env file.

    Returns:
        str: The API key.
    """
    return os.getenv('API_KEY')


def model_selection(model: Dict[int, str]) -> str:
    """
    Print the available models and get the user's selection.

    Args:
        model (dict): A dictionary of available models.

    Returns:
        str: The selected model.
    """
    # Print keys and values
    for key, value in model.items():
        print(f"{key + 1}: {value}")

    # Get user selection
    while True:
        try:
            selected_key = int(input("Enter the key of the model you want to select: ")) - 1
            selected_model = model[selected_key]
            return selected_model
        except (ValueError, KeyError):
            print("Invalid key. Please try again.")


def user_question() -> str:
    """
    Get the user's question.

    Returns:
        str: The user's question.
    """
    return input('What is your question? ')


def query_perplexity(selected_model: str) -> requests.models.Response:
    """
    Make a query to Perplexity AI.

    Args:
        selected_model (str): The selected model.

    Returns:
        response (requests.models.Response): The response from the API.
    """
    api_key = load_api_key()
    url = "https://api.perplexity.ai/chat/completions"

    response = ''

    # Set up the payload for the API request
    payload = {
        "model": selected_model,
        "messages": context
    }

    # Set up the headers for the API request
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}",
    }

    # Make the API request and handle any exceptions
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong", err)

    return response


def send_answer(response: requests.models.Response) -> str:
    """
    Extract the answer from the response and add it to the context.

    Args:
        response (requests.models.Response): The response from the API.

    Returns:
        str: The answer.
    """
    try:
        json_data = response.json()
        answer = json_data['choices'][0]['message']['content']
        context.append({"role": "assistant", "content": answer})
        return answer
    except (KeyError, IndexError):
        print("Error in response data")


def main() -> None:
    """
    The main function of the program. It gets the user's question, makes the API request, and prints the answer.
    """
    load_context_from_file()
    model = model_selection({0: 'codellama-34b-instruct', 1: 'llama-2-70b-chat', 2: 'mistral-7b-instruct',
                             3: 'pplx-7b-chat', 4: 'pplx-70b-chat-alpha'})
    while True:
        question = user_question()
        if question.lower() == '/q':
            print('Quitting...')
            save_context_to_file()  # Prompt the user to save the conversation context
            break
        context.append({"role": "user", "content": question})
        response = query_perplexity(model)
        answer = send_answer(response)
        print(f'Answer:\n{answer}')


if __name__ == '__main__':
    main()
