" I like vim defaults a lot, especially on Arch Linux
unlet! skip_defaults_vim
source $VIMRUNTIME/defaults.vim

fun RStripWhitespace()
	" Don't strip markdown files.
	" Trailing whitespace actually has meaning for that.
	if &ft !~ 'md'
		%s/\s*$//
		execute "normal \<C-O>"
	endif
endfun


" Common sense default settings
set nu relativenumber

" Delegate whitespace stripping to separate function
autocmd BufWritePre * call RStripWhitespace()

" Use <C-k> as a catch-all for my personal key mappings

" Special mappings to single-line (un)comment.
" Especially useful for Zig which has removed multiline comments.
map <C-K><C-C> :s/^\(\s*\)/\1\/\// <CR>
map <C-K><C-U> :s/^\(\s*\)\/\/*/\1/ <CR>

" Mapping to move code blocks or lines
" above or each other.
map <C-K><C-K> :m'<-2 <CR>
map <C-K><C-J> :m'>+ <CR>

