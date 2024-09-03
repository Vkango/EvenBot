# plugin_interface.py
class PluginInterface:
    def perform_action(self):
        raise NotImplementedError("Each plugin must implement the perform_action method.")