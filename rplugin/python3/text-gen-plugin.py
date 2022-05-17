# -*- coding: utf-8 -*-
"""
    bent.text-gen-plugin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Neovim remote plugin python part.
    Handles communication with the daemon, gathers text
    from neovim and pushes generated text to the source buffer.

    :copyright: (c) 2021 by Bent Mueller.
    :license: MIT, see LICENSE for more details.
"""


import json
import logging
import os
from os.path import expanduser
from pprint import pformat
import subprocess
from pathlib import Path

import neovim
import openai
import pexpect


# Load the API key
API_KEY: str = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

DATA_DIR: Path = Path.home() / ".text_gen_plugin"
DATA_DIR.mkdir(exist_ok=True)

TEMPFILE = DATA_DIR / "tmpfile"
LOGFILE = DATA_DIR / "logfile.log"
STATE_FILE = DATA_DIR / "statefile.json"

logging.basicConfig(level=logging.DEBUG, filename=LOGFILE)


model_ids: dict = {
    "1": "text-davinci-002",
    "2": "text-curie-001",
    "3": "text-babbage-001",
    "4": "text-ada-001",
    "5": "code-davinci-002",  # And the codex models
    "6": "code-cushman-001",
}

# Prepare a choices string here
models_choice_str = ""
for k, v in model_ids.items():
    models_choice_str += "{} --> {}\n".format(k, v)


# Pricing is calculated per 1k tokens in USD
models_pricing = {
    "text-davinci-002": 0.06,
    "text-curie-001": 0.006,
    "text-babbage-001": 0.0012,
    "text-ada-001": 0.0008,
    "code-davinci-002": 0.06,  # Not sure whether these pricings are right
    "code-cushman-001": 0.006,
}


@neovim.plugin
class TextGenPlugin(object):

    """Plugin to communicate with OpenAI's GPT-3 API."""

    def __init__(self, nvim):
        self.nvim = nvim

        self.constant_kwargs = {
            "echo": True,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        }

        self._load_state_file()

    def _save_state_to_file(self):
        """Save the state to the state file."""

        with open(STATE_FILE, "w") as fp:

            json.dump(self.state, fp)

    def _load_state_file(self):
        """Load the state from the state file."""

        try:

            with open(STATE_FILE, "r") as fp:

                self.state = json.load(fp)

        except:

            # Create state file if it doesn't exist
            self.state = {
                "total_tokens_requested": {name: 0 for name in model_ids.values()},
                "max_tokens": 256,
                "temperature": 0.0,
                "engine_id": "code-cushman-001",
                "total_spending_usd": 0.0,
            }

            # And then save the state to the file
            self._save_state_to_file()

    def _send_api_request(self, prompt_text: str) -> str:
        """Send an API request to OpenAI's GPT-3 API.

        Automatically logs API usage information and displays
        it to the user.
        """

        if not API_KEY:

            self.send_message_to_user("Error: could not find API key")
            return prompt_text

        assert self.state is not None, "State was none, cannot send API request"

        try:

            # Before really sending the API request, ask
            # the user if he really wants to send the request
            # and calculate an expected price for the request

            # According to OpenAI ~750 tokens make up 1000 words
            estimated_number_of_tokens = str.count(prompt_text, " ") / 750
            estimated_cost_in_usd = (
                estimated_number_of_tokens * models_pricing[self.state["engine_id"]]
            )

            user_response = self.nvim.input(
                "You are about to send a request for {} tokens (estimated)"
                " using the generation model '{}'.\n\nEstimated cost:"
                " ${:.2f}\n\nAre you sure you want to send this request?"
                " [y/n] ".format(
                    estimated_number_of_tokens,
                    self.state["engine_id"],
                    estimated_cost_in_usd,
                )
            )

            if user_response.lower() != "y":

                self.send_message_to_user("Request cancelled")
                return prompt_text

            # Otherwise send the request
            response = openai.Completion.create(
                engine=self.state["engine_id"],
                prompt=prompt_text,
                temperature=self.state["temperature"],
                max_tokens=self.state["max_tokens"],
                **self.constant_kwargs,
            )

            # Only return the text and write the raw response to the logfile
            logging.debug(
                "Received response from OpenAI API: \n{}".format(pformat(response))
            )

            return response["choices"][0]["text"]

        except Exception as ex:

            self.send_message_to_user(
                "Error occurred sending api request: {}".format(ex)
            )

            return prompt_text

    def _generate_text(self, source_text: str) -> str:

        # Ask the user first if he really wants to send the request

        # Send the api request
        response_text = self._send_api_request(source_text)

        return response_text

    def send_message_to_user(self, message: str):
        self.nvim.command('echo "{}\n\n"'.format(message))

    def extract_selected_text(self, r):

        """Given a selection range this method retrieves the selected text."""

        self.start, self.end = r
        self.start -= 1

        if self.start == self.end:
            # Nothing selected or just one line
            text = self.nvim.current.buffer[self.start]
            text += "\n"

        else:

            # Otherwise extract region
            lines_of_text = self.nvim.current.buffer[self.start : self.end]

            text = "\n".join(lines_of_text)

        return text

    def insert_text_into_buffer(self, text: str, r):

        # Split text back into list of lines
        text_lines = text.split("\n")

        if self.start == self.end:

            # If there was no visual selection, just paste the text into the current line
            self.nvim.current.buffer[self.start : self.start] = text_lines

        else:

            # Paste the text lines into the selection area
            self.nvim.current.buffer[self.start : self.end] = text_lines

    @neovim.command("TextGenGenerate", nargs="*", range="")
    def command_generate_text(self, args, r):

        # Extract the visually selected text first
        selected_text = self.extract_selected_text(r)

        # Emulate call to model for now
        generated_text = self._generate_text(selected_text)

        # Prepared some text
        # Now paste it back in the buffer where it came from

        self.insert_text_into_buffer(generated_text, r)

    @neovim.command("TextGenRestart")
    def restart_plugin(self):
        self._restart_daemon()
        self.send_message_to_user("Daemon restarted")

    @neovim.command("TextGenQuit")
    def quit_plugin(self):
        self._kill_daemon()
        self.send_message_to_user("Killed daemon process")

    @neovim.command("TextGenChangeTokenLength", nargs=1)
    def change_token_length(self, token_length):

        token_length = int(token_length[-1])

        if not 0 < token_length <= 4096:
            self.send_message_to_user(
                "Error: token length must be between 1 and 4096, given {}".format(
                    token_length
                )
            )

        else:

            self.max_tokens = token_length
            self._save_state_to_file()

    @neovim.command("TextGenChangeModel", nargs=1)
    def change_engine(self, token_length):
        """Change the generation model engine."""

        self.send_message_to_user(
            "Changing text generation model to \n{}".format(models_choice_str)
        )

        r = self.nvim.input(
            "Changing text generation model to \n{}".format(models_choice_str)
        )

        if r in model_ids.keys():
            new_engine_id = model_ids[r]
            self.send_message_to_user(
                "Changing generation model to {}".format(new_engine_id)
            )

            self.state["engine_id"] = new_engine_id
            self._save_state_to_file()

        token_length = int(token_length[-1])

        if not 0 < token_length <= 4096:
            self.send_message_to_user(
                "Error: token length must be between 1 and 4096, given {}".format(
                    token_length
                )
            )

        else:

            self.max_tokens = token_length
            self._save_state_to_file()
