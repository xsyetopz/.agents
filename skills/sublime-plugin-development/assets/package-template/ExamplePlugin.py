# pyright: reportMissingImports=false

import sublime
import sublime_plugin

from .example_core import greeting


def plugin_loaded():
    settings = sublime.load_settings("Example.sublime-settings")
    settings.add_on_change("example.reload", _settings_changed)


def plugin_unloaded():
    sublime.load_settings("Example.sublime-settings").clear_on_change("example.reload")


def _settings_changed():
    return None


class ExampleHelloCommand(sublime_plugin.WindowCommand):
    def run(self, name="workspace"):
        self.window.status_message(greeting(name))
