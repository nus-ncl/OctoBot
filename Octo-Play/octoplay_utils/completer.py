#!/usr/bin/python3
import glob
import os


class Completer(object):  # Custom completer

    def __init__(self, commands):
        self.commands = commands + ["help"]
        self.matches = []

    def _path_completer(self, text):
        """
            This is the tab completer for systems paths.
            Only tested on *nix systems
        """
        # replace ~ with the user's home dir. See https://docs.python.org/2/library/os.path.html
        if '~' in text:
            text = os.path.expanduser('~')

        return [x for x in glob.glob(text + '*')]

    def complete(self, text, state):
        if state == 0:  # Build new match list
            self.matches = [c for c in self.commands if c.startswith(text)]

            if len(self.matches) == 0:
                self.matches = self._path_completer(text)

        if state < len(self.matches):
            return self.matches[state]
        else:
            return None