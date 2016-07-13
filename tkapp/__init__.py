
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

        self._root = None

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

    def run(self):
        '''
        start the tk main loop
        '''
        self._root.mainloop()



