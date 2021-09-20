
" The VimL/VimScript code is included in this sample plugin to demonstrate the
" two different approaches but it is not required you use VimL. Feel free to
" delete this code and proceed without it.

vmap <silent> <C-t> :exec DoItPython()

function DoItVimL()
    echo "hello from DoItVimL"
endfunction
