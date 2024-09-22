# Terminator Trzsz Plugin


https://github.com/trzsz/trzsz-go  
with awesome [trzsz-go](https://trzsz.github.io/go), you can got `lrzsz` and `trzsz` support for [terminator](https://github.com/gnome-terminator/terminator)  


just run `trzsz -d bash`, then it will Take over your zmodem file transmit from stdio.  
you can use traditional `rz` `sz` cmd now (Or the more modern `trz` `tsz` cmd with Progress Bar)

BUT,  
terminator lack of dragfile support, so this plugin come..  
**It only add dragfile support for `trzsz --dragfile bash`**

## requirements

only tested with terminator 2.1.1+, on ubuntu 22 lts

## Install

1. Copy trzsz_dragfile.py to ~/.config/terminator/plugins/
2. Terminator Preferences > Plugins: enable `TrzszDrag`

## Usage

this only add dragfile support for Trzsz.

just dragfile to terminator
