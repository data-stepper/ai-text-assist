
" The VimL/VimScript code is included in this sample plugin to demonstrate the
" two different approaches but it is not required you use VimL. Feel free to
" delete this code and proceed without it.

" Map C-g to generate text
noremap <C-g> :TextGenGenerate<CR>
vnoremap <C-g> :TextGenGenerate<CR>
