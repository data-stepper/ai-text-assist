import neovim

@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('DoItPython', range=True)
    def doItPython(self, args, r):
        self.vim.command('echo "Received {}"'.format(r))

