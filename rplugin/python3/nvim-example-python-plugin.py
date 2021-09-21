import neovim


@neovim.plugin
class TestPlugin(object):


    def __init__(self, nvim):
        self.nvim = nvim


    def _call_to_model(self, source_text: str) -> str:
        pass


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
        text_len = len(selected_text)

        last_line = "This is the last line, your text contains {} characters, range {}".format(text_len, r)

        selected_text += '\n' + last_line

        # Prepared some text
        # Now paste it back in the buffer where it came from

        self.insert_text_into_buffer(selected_text, r)


