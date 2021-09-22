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

### Text Generation Using Textgen

A textgen plugin looks like this:

| Plugin | Description     |
| ---- | ------------ |
| aitext | Textgen language model.  |

In its most basic form, textgen generates text using the following code:

* [Textgen](https://github.com/ai-te/ai-tex)

```.py
import textgen

textgen.set_text_to_generate(text)
```


### Textgen Language Model

A language model for textgen is installed in the `ai-tex` directory. This is a Python module that supports the following two language models:

#### Textgen
* [gensim](http://nlp.seas.harvard.edu/gensim/)
* [aitext](http://aitext.com/)

This model uses the [gensir](http://gensir.readthedocs.io/) library to generate the text. 
 
The plugin uses the following code to generate the sentence for the word [`cat`]:

```, python
import textnet
import textgens
import text

class Textgen(textgens.Textgen):
    """
  
   Generate `text`
   """

    def __call__(self, text):
 		text = text.replace('cat', 'CAT')
 	return text


# Load the model
model = textgens.load_model_from_path(textgins.ext_path(aitextgen.aitext), aitext)

# Generate some text
textgen = Textgen(model)
textgen('This is a sentence that has many words in it.')
textgens = Textgen()
textggen = Textgens()

# Run the textgen model on the text
textgensequence = textgen.run("This is a sentences with many words in them")

# Print the sentence
print(textgenseqence)


## Configuration

The plugin supports configuration by passing in the following keyword arguments:

- `textgen_model` The name of the model to use to generate the selected text.
- `file` The file name of the text to generate.
- ```
  textgen_model_dir = 'ai-tex/'
  text_file = 'textgen.py'
  ```

The following example shows how to pass in the `textgen` parameter and use `ai-te` as the textgen language model:

## Example

``
$ vim.vim/ftplugin/textgen/textgen.vim
set fileformat=neovim
set neovim

set neomakeprg=textgen#textgen
set textgen_parser=textgen:textgen

set text_font=monospace
set textgens=textgens#textgens
set textgin_parser=aitext

set lhs=\%{l} \%{r}
set rhs=\%r
set rhs=\r
set lst=\%l \%r

set first=\s\+
set last=\s \+
set text=\%{\%s\%}
set content=\%c \%{lhs}
set last_text=\%p \%{last}
set lbl=\%b \%b
set rbl=\r\%b

set lastline
set lastword
set lastchar
set lpar=\%a \%p
set rpar=\r \%a
set lhsp=\%# \%rsp
set rhsp=\r# \%#

set lines=\%n
set words=\%w
set chars=\%x
set caps=\%X

set c_e_mode=1
set ctrl=\%v
set v_e_mod=1

set vim_insertmode=1	# Disable insert mode

set autoindent
set textwidth=100
set linewidth=100

set g_autowrite=1
``` 

This example shows how the textgen plugin can be configured to generate text in neovim using the aitex language model.

`` 
# Create a new file to generate the word 'CAT'
vue-textgen-new-file-with-textgen()

textgenname = 'ai_tex'

# Set the aiteXT model to use
aitext_model = 'aitext'

text_toGenerate = 'This is a text that uses a textgen plugin.

# The text to generate is in the current file
file = 'test_textgen.txt'

file_content = 'This line of text uses neovim text generation.'

# Add the aiteX text model to the text
aitex_text = 'aX'

aitexparser = textgenname + aitext_ model + '_parser.py'


# Run this plugin
vuetextgen()


# Save the file
file_save = 'test.txt'


vue_open('test.txt')
```		


## Command-line Usage

To use the plugin with the command line, add the `text` keyword argument to the `textgens` function to pass in a text string:

### Example

This command-line example shows how `textgennamed` can be used to pass in text to generate:

`$ vim.vue/ftplugin/.vue/textgen/.vim/textgens/textgennames.vim`

``	
set text="This is a test with a textgen text.
This is another test with a different textgen text."

text1 = vim.eval('textgennamestring(text)')

set content="This is another line of text.
And this is a third line of text."


set content1="This is the third line of the text."
```**

The first argument is the text to be generated, the second is the string to use in the textgen.

The `vim` module evaluates the text in the text to use as the text to pass to the textgen to generate the appropriate text.
The `textgend` function is passed the text to evaluate and create the textgen object.

`textgennamer` returns the text generated using the textgen, `textgeng` returns the object that contains the textgen method.

To rerun the textgen on the text, use the `vim` `eval` function, passing in the text as the text argument:

> `vim.vue/.vue/.vim/vim.vim`: `vim.eval('vim.eval("vim.eval(":textgennamename.text)")')`

This will evaluate the text to create the text generator, and then run the textgen using the text as input.

If the text argument was empty, the textgen will be run using the default text.
If the first argument is empty, the first word will be used.
If there are multiple words, the text will be run on all words.

> [vim.eval()](http://vimdoc.sourceforge.net/htmldoc/eval.html)

## Versioning

The textgen plugin has been tested with the version 3.0.1 of aitext, and should not be changed or updated.

| | | | |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| |    Last Updated    ||    **Description**   				| |
|------------------------------------------------|------------------------------------------|
| | 2014-05-20||Aitext language model.			    <<<|
|-------------------------------------------------|------------------------------------------|


## Copyright

Copyright (c) 2014-2015 [Data Science](http://datascience.org/)

Copyright 2015-2017 [David R.
