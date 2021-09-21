import neovim
import subprocess
import os

TMPFILE_PATH = '/tmp/text_gen_tmp'

@neovim.plugin
class TestPlugin(object):


    def __init__(self, nvim):
        self.nvim = nvim

        self._spawn_daemon()


    def _spawn_daemon(self):
        
        self.daemon = subprocess.Popen(
            "~/miniconda3/envs/aitextgen/bin/python" +
            " /home/bent/git/ai-text-assist/daemon.py",
            shell=True,
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )


    def _kill_daemon(self):
        
        out, _ = self.daemon.communicate('quit')
        self.daemon.kill()


    def _restart_daemon(self):
        
        self._kill_daemon()
        self._spawn_daemon()


    def _read_input_text(self):
        
        # Read from the temp file
        with open(TMPFILE_PATH, "r") as f:
            self.source_text = f.read()


    def _write_generated_text(self, generated_text: str):

        # First delete the file
        assert os.system('rm {}'.format(TMPFILE_PATH)) == 0, "Error occurred overwriting the tempfile"
        
        # This will fail if an error occurs here
        with open(TMPFILE_PATH, "w") as f:
            bytes_written = f.write(generated_text)



    def _generate_text(self, source_text: str) -> str:

        # Write source text to tempfile
        self._write_generated_text(source_text)

        out, _ = self.daemon.communicate('generate\n')

        assert out.endswith('done\n'), "Error occurred communicating with daemon"

        self._read_input_text()

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


    @neovim.command("TextGen", nargs="*", range="")
    def testcommand(self, args, r):

        # Extract the visually selected text first
        selected_text = self.extract_selected_text(r)

        # Emulate call to model for now
        selected_text = self._generate_text(selected_text)

        # Prepared some text
        # Now paste it back in the buffer where it came from

        self.insert_text_into_buffer(selected_text, r)


