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


import neovim
import subprocess
import os
import pexpect


TEMPFILE = '/tmp/text_gen_tmp'


@neovim.plugin
class TextGenPlugin(object):


    def __init__(self, nvim):
        self.nvim = nvim

        self.token_length = 512
        self._spawn_daemon()


    def _spawn_daemon(self):

        self.daemon = pexpect.spawn(
            "/home/bent/miniconda3/envs/aitextgen/bin/python" +
            " /home/bent/git/ai-text-assist/daemon.py",
            encoding='utf-8',
            timeout=1200
        )


    def _kill_daemon(self):

        self.daemon.sendline('quit')


    def _restart_daemon(self):
        
        self._kill_daemon()
        self._spawn_daemon()


    def _read_from_tempfile(self):
        
        # Read from the temp file
        with open(TEMPFILE, "r") as f:
            self.source_text = f.read()


    def _write_to_tempfile(self, generated_text: str):
        try:
            # First delete the file
            assert os.system('rm {}'.format(TEMPFILE)) == 0, "Error occurred overwriting the tempfile"

        except:
            pass
        
        # This will fail if an error occurs here
        with open(TEMPFILE, "w") as f:
            bytes_written = f.write(generated_text)


    def _generate_text(self, source_text: str) -> str:

        # Write source text to tempfile
        self._write_to_tempfile(source_text)

        self.daemon.sendline('generate {}'.format(self.token_length))
        self.daemon.expect('done', timeout=1200)

        self._read_from_tempfile()

        return self.source_text


    def send_message(self, message: str):
        self.nvim.command(
            'echo "{}\n\n"'.format(message)
        )


    def extract_selected_text(self, r):

        """Given a selection range this method retrieves the selected text."""

        self.start, self.end = r
        self.start -= 1
    
        if self.start == self.end:
            # Nothing selected or just one line
            text = self.nvim.current.buffer[self.start]
            text += '\n'

        else:

            # Otherwise extract region
            lines_of_text = self.nvim.current.buffer[self.start:self.end]
            
            text = '\n'.join(lines_of_text)

        return text


    def insert_text_into_buffer(self, text: str, r):

        # Split text back into list of lines
        text_lines = text.split('\n')

        if self.start == self.end:

            # If there was no visual selection, just paste the text into the current line
            self.nvim.current.buffer[self.start:self.start] = text_lines

        else:

            # Paste the text lines into the selection area
            self.nvim.current.buffer[self.start:self.end] = text_lines


    @neovim.command("TextGenGenerate", nargs="*", range="")
    def testcommand(self, args, r):

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
        self.send_message('Daemon restarted')


    @neovim.command("TextGenQuit")
    def quit_plugin(self):
        self._kill_daemon()
        self.send_message('Killed daemon process')

    @neovim.command("TextGenChangeTokenLength", nargs=1)
    def change_token_length(self, token_length):

        token_length = int(token_length[-1])

        if not 0 < token_length <= 2048:
            self.send_message("Error: token length must be between 1 and 2048, given {}".format(token_length))

        else:
            self.token_length = token_length
