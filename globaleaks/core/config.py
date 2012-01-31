
"""
This module handles general customizable informations about the GL node.
"""
from __future__ import with_statement

import ConfigParser
import os.path

def copyform(form, settings):
    """Copy each form value into the specific settings subsection. """
    for name, value in form.iteritems():
        setattr(settings, name, value)
    settings.commit()

class Config(object):
    """
    A Storage-like class which loads and store each attribute into a portable
    conf file.
    """

    __slots__ = ['_cfgfile', '_cfgparser']

    def __init__(self, cfgfile, section):
        super(ConfigFile, self).__init__()

        self._cfgfile = cfgfile
        # setting up confgiparser
        self._cfgparser = ConfigParser.ConfigParser()
        self._cfgparser.read([self._cfgfile])

    def __getitem__(self, section, name):
        """
        Return the attribute stored in [section] name = value
        If not found, raise KeyError
        """
        try:
            value = self._cfgparser.get(section, name)
            if value.isdigit():
                return int(value)
            elif value.lower() in ('true', 'false'):
                return value.lower() == 'true'
            else:
                return value
        except ConfigParser.NoOptionError:
            raise KeyError('Name %s in section %s not found.' % (section, name))

    def __setitem__(self, section, name, value):
        """
        Set the attribute stored in [section] name = values
        If not found, raise NameError.
        """
        try:
            self._cfgparser.set(self._section, name, str(value))
        except ConfigParser.NoOptionError:
            raise NameError(name)

    def commit(self):
        """
        Commit changes in config file.
        """
        with open(self._cfgfile, 'w') as cfgfile:
            self._cfgparser.write(cfgfile)
