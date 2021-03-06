
'''
this module provides an app class to use in python tk gui applications
'''

from tkapp.factories import WidgetFactory


class TkBaseWindow(object):
    '''
    this class represents a tk window - extended by TkApp and TkDialog
    '''

    def __init__(self):
        '''
        constructor
        '''
        self._layout = None
        self._materialized = False

        self._bound_events = []
        self._widget_index = dict()

        self._factory = WidgetFactory(self)
        self._root = None

    def __getitem__(self, key):
        '''
        produce the widget of the given name
        '''
        return self._widget_index[key]

    def __setitem__(self, key, value):
        '''
        store the given widget under the given name
        '''
        self._widget_index[key] = value

    def bind(self, event, callback):
        '''
        register a bind event and pass to materialized root widget
        '''
        self._bound_events.append((event, callback))
        if self._materialized:
            self._root.bind(event, callback)

    def set_layout(self, layout):
        '''
        set the layout from an xml file
        '''
        self._layout = layout

    def materialize(self):
        '''
        materialize the specified layout and menu to a window
        '''
        self._root = self._factory.from_file(self._layout)
        self._materialized = True

        for (event, callback) in self._bound_events:
            self._root.bind(event, callback)

    def spawn_dialog(self, dialog):
        '''
        take an instance of TkDialog and display it, blocks the main application
        '''
        dialog.set_master(self._root)
        dialog.materialize()
        dialog.wait()


class TkApp(TkBaseWindow):
    '''
    this class represents a base tk app - custom apps should inherit from it
    '''

    def __init__(self):
        '''
        constructor
        '''
        super(TkApp, self).__init__()

    def run(self):
        '''
        start the tk main loop
        '''
        self._root.mainloop()

    def quit(self):
        '''
        quit the tk main loop
        '''
        self._root.quit()


class TkDialog(TkBaseWindow):
    '''
    this class represents a tk dialog spawned on top of an application
    '''

    def __init__(self):
        '''
        constructor - set the given dialog layout
        '''
        super(TkDialog, self).__init__()

        self._master = None

    def set_master(self, master):
        '''
        set the parent window of the dialog
        '''
        self._master = master

    def materialize(self):
        '''
        show the dialog and block for a result
        '''
        super(TkDialog, self).materialize()

        self._root.transient(self._master)
        self._root.grab_set()

    def wait(self):
        '''
        block the parent window until the dialog is finished
        '''
        self._master.wait_window(self._root)
