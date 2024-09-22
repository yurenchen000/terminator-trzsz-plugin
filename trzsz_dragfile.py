
'''
Terminator plugin to implement 
   Kitty Hints-like feature for Terminator

 Author: yurenchen@yeah.net
License: GPLv2
   Site: https://github.com/yurenchen000/terminator-hints-plugin
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from gi.repository import Vte

AVAILABLE = ['TrzszDrag']

import terminatorlib.plugin as plugin


## disable log
print = lambda *a:None

'''
TerminalHandler to handle each terminal
   self-construct the third type plugin for Terminator
   by play tricks on a fake URLHandler
   heavy reliance on terminator internal implementation
'''
class TerminalHandler(plugin.URLHandler):
    ''' a fake URLHandler, register to each terminal for hints '''
    capabilities = ['url_handler']
    _handler_name = 'full_uri' ## HACK: use built-in name to avoid actual cost, it will not registered to matches

    @property
    def handler_name(self):    ## HACK: use getter got opportunity to call function
        """Handle init for each term"""
        term = self.get_terminal()
        self.attach_terminal(term)
        return self._handler_name

    def unload(self):
        """Handle deinit for disable"""
        self.disable()

    def __init__(self):
        """Handle init for load or enable"""
        self.terminator = plugin.Terminator()
        terminal = self.get_terminal()
        if terminal: # is load
            self.enable(terminal)
        else:
            self.enable(None)

    # hack from https://github.com/mchelem/terminator-editor-plugin
    def get_terminal(self):    # HACK: use the inspect module to climb up the stack to the Terminal object
        import inspect
        for frameinfo in inspect.stack():
            frameobj = frameinfo[0].f_locals.get('self')
            if frameobj and frameobj.__class__.__name__ == 'Terminal':
                return frameobj

    def enable(self, terminal=None):
        ''' Callback to enable plugin
        if terminal:
            do_load_things()
            return
        for terminal in self.terminator.terminals:
            print('terminal:', terminal)
            do_init_for_terminal(terminal)
        '''
        raise NotImplementedError

    def disable(self):
        ''' Callback to disable plugin
        for terminal in self.terminator.terminals:
            print('terminal:', terminal)
            de_init_for_terminal(terminal)
        '''
        raise NotImplementedError

    def attach_terminal(self, terminal):
        ''' Callback to init for each terminal
        print('terminal:', terminal)
        do_init_for_terminal(terminal)
        '''
        raise NotImplementedError

def hex_id(term):
    return hex(id(term))
    # return x.uuid

class TrzszDrag(TerminalHandler):
    ''' a fake URLHandler, register to each terminal for hints '''
    def attach_terminal(self, terminal):    ## register for each terminal once
        print('\n==TrzszDrag init_term:', hex_id(terminal))
        TrzszDragImpl.setup_for_term(terminal)

    def disable(self):
        print('\n==disable_trzszDrag..')
        for terminal in self.terminator.terminals:
            # print('term:', terminal)
            TrzszDragImpl.teardown_for_term(terminal)

    def enable(self, terminal=None):
        if terminal:
            print('\n==load_trzszDrag:', hex_id(terminal))
            return

        print('\n==enable_trzszDrag..')
        for terminal in self.terminator.terminals:
            # print('term:', terminal)
            TrzszDragImpl.setup_for_term(terminal)


'''
 trzsz dragfile support for Terminator
'''
class TrzszDragImpl:
    def __init__(self, term):
        if hasattr(term, 'trzsz_drag'): # already init
            return

    @staticmethod
    def setup_for_term(term):
        if hasattr(term, 'trzsz_drag'): # already init
            return term.trzsz_drag
        else:
            ## NOTE: only text (avoid conflict with builtin drag function)
            term.trzsz_drag = term.vte.connect("drag-data-received", TrzszDragImpl.on_drag_data_received)

            print('== do init dragfile:', hex_id(term), term.trzsz_drag)

    @staticmethod
    def teardown_for_term(term):
        if not hasattr(term, 'trzsz_drag'): # already destroy
            return 
        else:
            print('== de-init dragfile:', hex_id(term), term.trzsz_drag)
            term.vte.disconnect(term.trzsz_drag)
            del term.trzsz_drag


    @staticmethod
    def on_drag_data_received(widget, drag_context, x, y, data, info, time):
        print('== on drag:', data.get_uris(), data.get_text())
        
        files = []
        # uris = data.get_uris()
        uris = data.get_text().splitlines()
        if not Gtk.targets_include_uri(drag_context.list_targets()):
            return
        for uri in uris:
            file_path = GLib.filename_from_uri(uri)[0]
            print(f" - drag file: {file_path}")
            files.append(file_path)

        ## encode and send to vte child
        if files:
            # files = [ f"'{f}'" if ' ' in f else f for f in files]  # quote if has space
            # wrapped_files = '\x1b[200~' + ' '.join(files) + ' \x1b[201~'
            import shlex
            shstr = shlex.join(files)
            wrapped_files = '\x1b[200~' + shstr + ' \x1b[201~'
            print('=== feed:', wrapped_files)
            vte = widget
            vte.feed_child(wrapped_files.encode('utf-8'))

