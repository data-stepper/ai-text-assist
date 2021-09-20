import neovim

@neovim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    def _call_to_model(self, source_text: str) -> str:
        pass

    @neovim.command('AiTextGen', nargs='*', range='')
    def testcommand(self, args, r):
        
        if r == [1, 1]:
            self.nvim.command('echo "You need to visually select some text to use for text generation."')
