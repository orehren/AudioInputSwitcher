# Import StreamController modules
from GtkHelper.GtkHelper import ComboRow
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Pango

import pulsectl

class SetInput(ActionBase): # Changed class name
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self):
        self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "externalmic.png"), size=0.75) # changed icon

    def get_config_rows(self) -> list:
        self.device_model = Gtk.ListStore.new([str])
        self.device_display_name = Gtk.ListStore.new([str])
        self.device_row = ComboRow(title=self.plugin_base.lm.get("ais.actions.set-device.device.title"), model=self.device_display_name) # changed label

        self.device_cell_renderer = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END, max_width_chars=60)
        self.device_row.combo_box.pack_start(self.device_cell_renderer, True)
        self.device_row.combo_box.add_attribute(self.device_cell_renderer, "text", 0)

        self.load_device_model()

        self.device_row.combo_box.connect("changed", self.on_device_change)

        self.load_config_settings()

        return [self.device_row]

    def load_device_model(self):
        self.device_model.clear()
        with pulsectl.Pulse('set-input') as pulse: # Changed pulsectl name
            for source in pulse.source_list(): # Changed list
                name = self.get_source_identifier(source) # Changed function name
                display_name = self.get_display_name(source)
                if name is None:
                    continue
                self.device_model.append([name])
                self.device_display_name.append([display_name])

    def load_config_settings(self):
        settings = self.get_settings()
        name = settings.get("device")
        for i, device in enumerate(self.device_model):
            if device[0] == name:
                self.device_row.combo_box.set_active(i)
                return

        self.device_row.combo_box.set_active(-1)

    def on_device_change(self, combo_box, *args):
        name = self.device_model[combo_box.get_active()][0]
        settings = self.get_settings()
        settings["device"] = name
        self.set_settings(settings)

    def on_key_down(self):
        settings = self.get_settings()
        device_name = settings.get("device")
        if device_name is None:
            self.show_error(1)
            return

        with pulsectl.Pulse('set-input') as pulse: # Changed pulsectl name
            for source in pulse.source_list(): # Changed list
                proplist = source.proplist
                name = proplist.get("node.name")
                if name == device_name:
                    pulse.source_default_set(source) # Changed set function
                    break

    def get_display_name(self, source) -> str: # Changed source
        proplist = source.proplist # Changed source
        name = (proplist.get("device.product.name") or proplist.get("device.nick") or
                proplist.get("device.description") or source.name or None) # Changed source
        description = proplist.get("device.profile.description")
        if description not in ("", None):
            name = f'{name} ({description})'
        return name
    
    def get_source_identifier(self, source) -> str: # Changed source
        proplist = source.proplist # Changed source
        return proplist.get("node.name") or source.name # Changed source
