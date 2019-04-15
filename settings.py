import os
from configparser import ConfigParser


class Settings(object):

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        settings_file = dir_path + '/settings.conf'
        self.parser = ConfigParser()
        self.parser.read(settings_file)

    def get_field(self, stanza, field_name):
        return self.parser.get(stanza, field_name)