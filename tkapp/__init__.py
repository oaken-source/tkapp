
'''
this module provides an app class to use in python tk gui applications
'''

from tkapp.factories import WidgetFactory


class TkApp(object):
    '''
    this class represents a base tk app - custom apps should inherit from it
    '''

    def __init__(self):
        '''
        constructor
        '''
        self._layout = None
        self._menu = None

        self._materialized = False
        self._bound_events = []

        self._root = None

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
        self._root = WidgetFactory.from_file(self._layout)
        self._materialized = True

        for (event, callback) in self._bound_events:
            self._root.bind(event, callback)

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
