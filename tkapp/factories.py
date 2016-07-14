
'''
this module provides the foctories used in tkapp
'''

import importlib
import tkinter as tk
import xml.etree.ElementTree as et


class WidgetFactory(object):
    '''
    this class produces tk widgets from xml
    '''

    def __init__(self, app):
        '''
        constructor - store the app reference
        '''
        self._app = app

    def from_file(self, path):
        '''
        produce a widget from an xml file
        '''
        with open(path) as xml:
            return self.from_string(xml.read())

    def from_string(self, xml):
        '''
        produce a widget from an xml string
        '''
        return self.from_etree(et.fromstring(xml.strip()))

    def from_etree(self, xml, master=None):
        '''
        produce a widget from an xml etree - magic happens here
        '''
        attributes = PartitionedAttributes(xml.attrib)
        attributes.bind_callbacks(self._app)

        # cover menu command and separator special cases
        if xml.tag == 'tkinter.Menu.add_command':
            master.add_command(**attributes)
            return
        elif xml.tag == 'tkinter.Menu.add_separator':
            master.add_separator(**attributes)
            return

        # produce instance from tag name
        instance = self._get_class(xml.tag)(master, **attributes)

        # dispatch further processing by master widget
        if isinstance(master, tk.Menu) and isinstance(instance, tk.Menu):
            master.add_cascade(menu=instance, **attributes.add_cascade)
        elif isinstance(instance, tk.Menu):
            master.config(menu=instance)
        elif isinstance(master, tk.PanedWindow):
            master.add(instance)
        elif master is not None:
            instance.pack(**attributes.pack)

        # produce child widgets
        for child in xml.getchildren():
            self.from_etree(child, instance)

        # all done - return created widget instance
        return instance

    @classmethod
    def _get_class(cls, name):
        '''
        produce the class from the given import name
        '''
        modname, clsname = name.rsplit('.', 1)
        return getattr(importlib.import_module(modname), clsname)


class PartitionedAttributes(object):
    '''
    this class allows partitioned access to a dictionary
    '''
    _separator = '.'

    def __init__(self, attributes):
        '''
        constructor - produce partition data and set partitions as attributes
        '''
        self._attributes = dict()

        tmp = dict()
        while attributes:
            key, value = attributes.popitem()
            head, sep, tail = key.partition(self._separator)
            if not sep:
                self._attributes[key] = value
            else:
                tmp.setdefault(head, dict())[tail] = value

        for partition in tmp:
            setattr(self, partition, PartitionedAttributes(tmp[partition]))

        self._partitions = tmp.keys()

    def bind_callbacks(self, app):
        '''
        bind callback strings to methods on the app instance
        '''
        if 'command' in self._attributes:
            self._attributes['command'] = getattr(app, self._attributes['command'])

        for partition in self._partitions:
            getattr(self, partition).bind_callbacks(self)

    def __getattr__(self, _):
        '''
        produce an empty dict if a non existing attribute is queried
        '''
        return dict()

    def __len__(self):
        '''
        relay len calls to the attribute dict
        '''
        return self._attributes.__len__()

    def __contains__(self, key):
        '''
        relay contains calls to the attribute dict
        '''
        return self._attributes.__contains__(key)

    def __getitem__(self, key):
        '''
        relay getitem calls to the attribute dict
        '''
        return self._attributes.__getitem__(key)

    def __iter__(self):
        '''
        relay __iter__ calls to the attribute dict
        '''
        return self._attributes.__iter__()

    def items(self):
        '''
        relay items calls to the attribute dict
        '''
        return self._attributes.items()

    def keys(self):
        '''
        relay keys calls to the attribute dict
        '''
        return self._attributes.keys()

    def values(self):
        '''
        relay values calls to the attribute dict
        '''
        return self._attributes.values()
