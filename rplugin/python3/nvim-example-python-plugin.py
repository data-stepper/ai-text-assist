import neovim
import subprocess


@neovim.plugin
class TestPlugin(object):


    def __init__(self, nvim):
        self.nvim = nvim


    def _generate_text(self, source_text: str) -> str:

        # cmd = [
        #     "~/miniconda3/envs/aitextgen/bin/aitextgen",
        #     "generate",
        #     "--prompt",
        #     "\"{}\"".format(source_text),
        #     "--to_file",
        #     "False",
        #     "--n",
        #     "1",
        #     "--temperature","0.01","--max_length","50"
        # ]

        cmd = ("~/miniconda3/envs/aitextgen/bin/aitextgen generate" +
                " --prompt \"{}\"".format(source_text) +
                " --to_file False --n 1 --temperature 0.01 --max_length 100 |" +
                "sed -r \"s/\\x1B\[[0-9;]*[a-zA-Z]//g\"")

        # self.nvim.current.buffer[:] = cmd
        # quit()

        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.returncode == 0:
            # Everything went fine
            produced_text = p.stdout
            produced_text = bytes.decode(produced_text)
            return produced_text

        else:
            # Some error occurred
            err_message = bytes.decode(p.stderr)
            self.send_message("An Error occurred trying to generate text:\n\n{}".format(err_message))

            return source_text


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


