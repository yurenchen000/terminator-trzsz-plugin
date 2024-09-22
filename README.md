# Terminator Trzsz Plugin


## about trzsz
https://github.com/trzsz/trzsz-go  
with awesome [trzsz-go](https://trzsz.github.io/go), you can got `lrzsz` and `trzsz` support for [terminator](https://github.com/gnome-terminator/terminator)  


Just run `trzsz -d bash`, then it will Take over your zmodem file transmit from stdio.  
you can use traditional `rz` `sz` cmd now (Or the more modern `trz` `tsz` cmd with Progress Bar)

And you can set it as terminator default shell:  
Terminator Preferences > Profile > Command > Custom Command: `trzsz --dragfile bash`

## dragfile support
BUT,  
terminator lack of dragfile support, so this plugin come..  
**It only add dragfile support for `trzsz --dragfile bash`**

## requirements

only tested with terminator 2.1.1+, on ubuntu 22 lts

## Install

1. Copy `trzsz_dragfile.py` to ~/.config/terminator/plugins/
2. Terminator Preferences > Plugins: enable `TrzszDrag`

## Usage

this only add dragfile support for Trzsz.

just dragfile to terminator

<br>

## Dev Note
this plugin based on `TerminalHandler`, 
It is the third type of plugin that is implemented through heavy hacking

cause terminator offically only support [two type of plugins](https://gnome-terminator.readthedocs.io/en/latest/plugins.html#creating-your-own-plugins):
- plugin.URLHandle
- plugin.MenuItem
which makes plugin functionality very limited.

After some exploration, I implement this new plugin type,  
which improved the plugin capabilities.

<br>

Another plugin with `shortcut` support in terminator plugin  
(through hacking way, cause orignal plugin no such capbility)  
https://github.com/yurenchen000/terminator-hints-plugin


