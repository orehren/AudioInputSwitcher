# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

# Import actions
from .actions.SetInput.SetInput import SetInput
from .actions.ToggleInput.ToggleInput import ToggleInput

class AudioInputSwitcher(PluginBase): # Changed plugin class name
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager

        ## Register actions
        self.set_input_holder = ActionHolder( # Changed name
            plugin_base = self,
            action_base = SetInput, # Changed name
            action_id_suffix = "SetInput", # Changed suffix
            action_name = self.lm.get("ais.actions.set-input.name"), # Changed label
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.set_input_holder)

        self.toggle_input_holder = ActionHolder( # Changed name
            plugin_base = self,
            action_base = ToggleInput, # Changed name
            action_id_suffix = "ToggleInput", # Changed suffix
            action_name = self.lm.get("ais.actions.toggle-input.name"), # Changed label
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.toggle_input_holder)

        # Register plugin
        self.register(
            plugin_name = self.lm.get("plugin.name"),
            github_repo = "https://github.com/orehren/AudioInputSwitcher", # Update with your repo
            plugin_version = "1.0.0",
            app_version = "1.4.5-beta"
        )
