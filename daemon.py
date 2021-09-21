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

TMPFILE_PATH = '/tmp/text_gen_tmp'


class Daemon:

    def __init__(self, model_name: str = "EleutherAI/gpt-neo-2.7B"):

        self.model_name = model_name
        self._load_model()


    def _read_input_text(self):
        
        # Read from the temp file
        try:
            with open(TMPFILE_PATH, "r") as f:
                self.source_text = f.read()

        except:
            # Failed to read text
            self.source_text = ""


    def _write_generated_text(self, generated_text: str):

        # First delete the file
        assert os.system('rm {}'.format(TMPFILE_PATH)) == 0, "Error occurred overwriting the tempfile"
        
        # This will fail if an error occurs here
        with open(TMPFILE_PATH, "w") as f:
            bytes_written = f.write(generated_text)


    def generate_text(self):
        
        self._read_input_text()

        self.generated_text = self.ai.generate_one(prompt=self.source_text, max_length=512, no_repeat_ngram_size=4)

        self._write_generated_text(self.generated_text)

    
    def listen_to_input(self):

        for line in sys.stdin:
            
            if line.startswith('generate'):
                # Generate some text
                self.generate_text()

                # After generating text respond on stdout
                print("done")

            elif line.startswith('quit'):
                # Quit the daemon

                del self.ai
                exit(0)


    def _load_model(self):

        self.ai = aitextgen.aitextgen(model=self.model_name)

        # The bigger model needs to be in fp16 because of GPU memory capacities
        self.ai.to_fp16()

        # Load the model onto gpu for speed up
        self.ai.to_gpu()


def main():
    
    d = Daemon()
    d.listen_to_input()


if __name__ == "__main__":
    main()


