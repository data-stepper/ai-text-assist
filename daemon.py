# -*- coding: utf-8 -*-
"""
    ai-text-assist.daemon
    ~~~~~~~~~~~~~~~~~~~~~

    This is a simple daemon listening to commands from the main plugin.
    It will handle communication with the GPU to generate text with it.

    :copyright: (c) 2021 by Bent Mueller.
    :license: MIT, see LICENSE for more details.
"""

import sys
import os
import aitextgen


TEMPFILE = "/tmp/text_gen_tmp"


class Daemon:

    """Daemon class"""

    def __init__(self, model_name: str = "EleutherAI/gpt-neo-2.7B"):

        self.model_name = model_name
        self._load_model()
        self.token_length = 1024

    def _read_input_text(self):
        """Reads text from the tempfile and stores it in self.source_text."""

        # Read from the temp file
        try:
            with open(TEMPFILE, "r") as f:
                self.source_text = f.read()

        except:
            # Failed to read text
            self.source_text = ""

    def _write_generated_text(self, generated_text: str):
        """Deletes tempfile and writes text to the it."""

        # First delete the file
        assert (
            os.system("rm {}".format(TEMPFILE)) == 0
        ), "Error occurred overwriting the tempfile"

        # This will fail if an error occurs here
        with open(TEMPFILE, "w") as f:
            bytes_written = f.write(generated_text)

    def generate_text(self):
        """Handles entire text generation process."""

        self._read_input_text()

        self.generated_text = self.ai.generate_one(
            prompt=self.source_text,
            max_length=self.token_length,
            no_repeat_ngram_size=4,
            do_sample=False,
            early_stopping=True,
        )

        self._write_generated_text(self.generated_text)

    def listen_to_input(self):
        """Listens on stdin for input so it knows when to generate new text."""

        for line in sys.stdin:

            if line.startswith("generate"):
                # Find how many tokens to generate
                n = str.replace(line, "generate ", "")

                if n[-1] in "\n\r":
                    n = n[:-1]

                # Now parse the number of tokens
                try:
                    self.token_length = int(n)

                except:
                    pass

                # Generate some text
                self.generate_text()

                # After generating text respond on stdout
                print("done")

            elif line.startswith("quit"):
                # Quit the daemon

                del self.ai
                exit(0)

    def _load_model(self):
        """Loads the model from file."""

        self.ai = aitextgen.aitextgen(model=self.model_name)

        # The bigger model needs to be in fp16 because of GPU memory capacities
        self.ai.to_fp16()

        # Load the model onto gpu for speed up
        self.ai.to_gpu()


def main():
    """Main function in daemon."""

    d = Daemon()
    d.listen_to_input()


if __name__ == "__main__":
    main()
