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


import logging
import os
from os.path import expanduser
import subprocess

import json
import neovim
import openai
import pexpect


# Load the API key
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

TEMPFILE = "/tmp/text_gen_tmp"
LOGFILE = "/log/text_generation.log"
STATE_FILE = "/log/text_generation_plugin_state_file.json"
logging.basicConfig(level=logging.DEBUG, filename=LOGFILE)


model_ids = {
    "1": "text-davinci-002",
    "2": "text-curie-001",
    "3": "text-babbage-001",
    "4": "text-ada-001",
}


# Pricing is calculated per 1k tokens in USD
models_pricing = {
    "text-davinci-002": 0.06,
    "text-curie-001": 0.006,
    "text-babbage-001": 0.0012,
    "text-ada-001": 0.0008,
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

    def _load_state_file(self):

        try:

            with open(STATE_FILE, "rw") as fp:

                self.state = json.load(fp)

        except:

            # Create state file if it doesn't exist
            self.state = {
                "total_tokens_requested": {
                    "text-davinci-002": 0,
                    "text-curie-001": 0,
                    "text-babbage-001": 0,
                    "text-ada-001": 0,
                },
                "max_tokens": 256,
                "temperature": 0.0,
                "engine_id": "text-curie-001",
                "total_spending_usd": 0.0,
            }

            # And then save the state to the file

    def _send_api_request(self, prompt_text: str) -> str:
        pass

    def _generate_text(self, source_text: str) -> str:

        self.daemon.sendline("generate {}".format(self.max_tokens))
        self.daemon.expect("done", timeout=1200)

        self._read_from_tempfile()

        return self.source_text

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
        selected_text = self._generate_text(selected_text)

        # Prepared some text
        # Now paste it back in the buffer where it came from

        self.insert_text_into_buffer(selected_text, r)

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
                "Error: token length must be between 1 and 4096, given {}"
                .format(token_length)
            )

        else:
            self.max_tokens = token_length
