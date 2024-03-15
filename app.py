###############################################################################
#   This program  allows a user to select an AI model and query against it    #
#    Copyright (C) 2024  Tom Welsh twelsh37@gmail.com                         #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.   #
###############################################################################

###############################################################################
# DESCRIPTION                                                                 #
# 1. A user selects an AI model from the dropdown list ID=model-dropdown      #
# 2. The user enters their question into the input area. ID = question-input  #
# 3. The user  clicks on the submit button and the question-input is queried  #
#    against the selection from the mode-dropdown.                            #
# 4. The users query is returned and displayed in the ID=answer-output        #
#    section.                                                                 #
#                                                                             #
###############################################################################

# Standard Libraries
import logging
import os


# Third Party / Related Imports
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Define the logging configuration for the application
logging.basicConfig(
    # Specify the log file's name. The logging module will write logs to 'app.log'.
    # Update the filename if you need logs written to a different file
    filename="app.log",
    # Set how the log file is opened. 'a' means the file is opened in 'append' mode.
    # The file is appended to each time the program runs.
    # Change to 'w' for 'write' mode to write a new logfile each application run.
    filemode="a",
    # Set the format for log messages.
    # '%(asctime)s' adds a timestamp to each log entry.
    # '%(name)s' denotes the logger's name, '%(levelname)s' inserts the message level (debug, info, etc.),
    # and '%(message)s' inserts the log message.
    # Update the format string to modify the information added to each log message.
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Define the date and time format that will be appended to each log message as dictated by '%(asctime)s'.
    # Currently set to 'Month/Day/Year Hour (24-hour format):Minute:Second'.
    # Change this string to modify timestamp format.
    datefmt="%m/%d/%Y %H:%M:%S",  # Adjusted to 24-hour clock
    # Denote the lowest level of logs that will be recorded.
    # Levels are: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL in ascending order.
    # 'DEBUG' is the lowest possible level -> all messages will be logged.
    # Raise this level to record only higher-level log messages.
    level=logging.WARNING,
)


# load our environment variabled
load_dotenv()

url = 'https://docs.perplexity.ai/docs/model-cards'


# API key Load funktion
def load_api_key() -> str:
    """
    Load the API key from the .env file.

    Returns:
        str: The API key.
    """
    return os.getenv("API_KEY")


def fetch_url_content(uri: str) -> bytes | str:
    """
        Fetches the HTML content of a webpage given a URL.

    Args:
        uri (str): The webpage URL.

    Returns:
        str: The HTML content of the webpage.
    """
    try:
        response = requests.get(uri)
        response.raise_for_status()
        return response.content
    # Deal with HTTP error
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        return ''
    # Deal with request failure
    except requests.exceptions.RequestException as err:
        print("Request Failed:", err)
        return ''


def fetch_models(uri: str) -> list:
    """
    Scrapes a webpage for a table of models.

    Args:
        uri (str): The URL of the webpage to scrape.

    Returns:
        list: The list of model names found in the webpage.
    """
    content = fetch_url_content(uri)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('div', {'class': 'rdmd-table-inner'})

        # Extract model names
        models = [
            cell.find('code', {'tabindex': '0'}).text
            for row in table.find_all('tr')
            if (cell := row.find('td')) is not None
            and cell.find('code', {'tabindex': '0'}) is not None
        ]
        return models
    else:
        print("No content retrieved from URL.")
        return []


# load our API key
api_key = load_api_key()

# Create a new Dash application
app = dash.Dash(
    # __name__ is a special Python variable whose value is set to the name of the current module
    # Here it's used to help Dash determine the location of static files
    __name__,
    # External CSS stylesheets, in this case, a Bootstrap theme is used
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # The prevent_initial_callbacks parameter is set to "initial_duplicate".
    # This is used to prevent callbacks from firing when the Dash app starts. It will not trigger
    # the callbacks with the initial values of the input components, but only with the later ones.
    prevent_initial_callbacks="initial_duplicate",
)

# Begins creating the layout for the dash application
app.layout = dbc.Container(
    [  # Array of all the elements to add to the container
        # Define a row in the container
        dbc.Row(
            [
                # Creates a level 4 heading with the text "Select Your Model"
                html.H4("Select Your Model", style={"color": "white"}),
                # Dropdown menu with the id 'model-dropdown'
                dcc.Dropdown(
                    id="model-dropdown",
                    # Options for the dropdown, each defined as a dictionary
                    options=[{'label': model, 'value': model} for model in fetch_models(url)],

                    # Default selected option
                    value="codellama-34b-instruct",
                ),
            ],
            style={"align-items": "left"},
        ),
        dbc.Row(
            [
                html.H4(
                    "Ask your question", style={"color": "white", "margin-top": "5px"}
                ),
                # Textbox for taking user's input with the id 'question-input'
                dbc.Textarea(
                    id="question-input",
                    placeholder="Enter a question...",  # Placeholder text
                    style={"borderRadius": "5px", "height": "30vh", "color": "black"},
                ),
            ],
            style={"align-items": "left", "marginBottom": "1vh"},
        ),
        dbc.Row(
            [
                html.H4("Your Question Answered", style={"color": "white"}),
                # Textbox for showing the answer to the user's question with id 'answer-output'
                dbc.Textarea(
                    id="answer-output",
                    placeholder="Answer will be displayed here...",
                    style={"borderRadius": "5px", "height": "30vh", "color": "black"},
                    className="mb-10",
                ),
            ],
            style={"align-items": "left", "marginBottom": "1vh"},
        ),
        dbc.Row(
            [
                # "Submit" button with id 'submit-button'
                dbc.Button(
                    "Submit",
                    id="submit-button",
                    n_clicks=0,
                    style={
                        "borderRadius": "5px",
                        "maxWidth": "150px",
                        "margin-top": "10px",
                    },
                ),
                # "Reset" button with id 'reset-button'
                dbc.Button(
                    "Reset",
                    id="reset-button",
                    n_clicks=0,
                    style={
                        "borderRadius": "5px",
                        "maxWidth": "150px",
                        "margin-top": "10px",
                        "margin-left": "20px",
                    },
                ),
            ],
            justify="left",
        ),
    ],
    style={"padding": "30px", "backgroundColor": "#006635", "height": "100vh"},
    fluid=True,  # Container spans the width of the screen
)


def get_api_response(uri, payload, headers):
    """
    Send a request to the given url with provided payload and headers.
    Return the response upon success or log an error upon failure.
    """
    try:
        response = requests.post(uri, json=payload, headers=headers)
        response.raise_for_status()

    except requests.exceptions.RequestException as err:
        logging.error(f"RequestException: {err}")
        raise PreventUpdate(f"Something went wrong: {err}")

    else:
        return response.json()


@app.callback(
    Output("answer-output", "value"),
    Input("submit-button", "n_clicks"),
    [
        State("model-dropdown", "value"),
        State("question-input", "value"),
    ],
)
def update_output(n_clicks, model_value, question_value):
    """
    Update the value of the 'answer-output' component based on inputs and states.
    There is a callback to this function when 'submit-button' is clicked.
    """
    logging.info(
        f"Number of clicks: {n_clicks}, Model value: {model_value}, Question value: {question_value}"
    )

    if not (n_clicks > 0 and question_value and model_value):
        raise PreventUpdate

    api_key1 = load_api_key()
    ura = "https://api.perplexity.ai/chat/completions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key1}",
    }
    payload = {
        "model": model_value,
        "messages": [{"role": "user", "content": question_value, "temperature":2.2}],
    }
    response = get_api_response(ura, payload, headers)
    logging.info(f"Response from API: {response}")
    return response["choices"][0]["message"]["content"]


@app.callback(
    [
        Output("model-dropdown", "value", allow_duplicate=True),
        Output("question-input", "value", allow_duplicate=True),
        Output("answer-output", "value", allow_duplicate=True),
    ],
    Input("reset-button", "n_clicks"),
)
def reset_values(n: int):
    """
    Resets the values of the dropdown, question input, and answer output fields
    whenever the reset button is clicked.

    Args:
        n (int): Number of times reset button is clicked

    Returns:
        Tuple[str, str, str]: Tuple containing default values for the dropdown,
        question input and answer output fields respectively.
    """
    try:
        if n > 0:
            # Reset text input fields to empty strings and the dropdown to its default value
            return "codellama-34b-instruct", "", ""
        else:
            raise PreventUpdate()
    except Exception as e:
        logging.error(f"Error while resetting values: {e}")
        raise e


if __name__ == "__main__":
    app.run_server(port=8000)
