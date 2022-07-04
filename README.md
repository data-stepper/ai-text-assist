# Text Gen Neovim Plugin

A neovim plugin that enables instant text generation inside neovim. 

## Installation

If you are using vim-plug, add the following to your vimrc:

```
Plug 'data-stepper/ai-text-gen'
```

## Requirements

You need the python module aitextgen in order for the plugin to work as it uses their language models.

## Usage

Select some text in visual mode, hit <C-g> and the plugin will feed the selected text to the text generation model to generate the rest of the text.

## TODO List

- [ ] Plugin only works when neovim is started in a directory that already downloaded the aitextgen models
- [ ] Should support variable text length when generating text, or a command to change text length.
- [x] Plugin should be able to generate text with variable length.
