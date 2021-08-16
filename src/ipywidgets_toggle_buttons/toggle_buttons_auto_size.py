"""class ToggleButtonsAutoSize"""
# Standard library imports
import logging

# Third party imports
import ipywidgets

# Local imports
from .layouts import DICT_LAYOUT_HBOX_ANY
from .layouts import DICT_LAYOUT_VBOX_ANY
from .abc_toggle_buttons import ToggleButtonsABC

LOGGER = logging.getLogger(__name__)


class ToggleButtonsAutoSize(ToggleButtonsABC):
    """Class to show toggle buttons with auto width"""

    def __init__(self, *args, **kwargs):
        """Initialize object

        Args:
            *args, **kwargs - Arguments to give into ipywidgets.ToggleButtons()
        """
        super().__init__(**kwargs)
        self.widget_parent = ipywidgets.ToggleButtons(*args, **kwargs)
        hbox_tmp = ipywidgets.HBox([self.widget_parent])
        hbox_tmp.layout = ipywidgets.Layout(**DICT_LAYOUT_HBOX_ANY)
        self.widget = ipywidgets.VBox([hbox_tmp])
        self.box_widget = self.widget
        self.widget.layout = ipywidgets.Layout(**DICT_LAYOUT_VBOX_ANY)
        self._tuple_value_types = (str, )
        self._update_buttons_for_new_options()
        self._update_widget_view()

    def _update_buttons_for_new_options(self):
        """Update buttons if options were changed"""
        int_width = self.func_to_get_option_width(self.options)
        self.widget_parent.style.button_width = "%dpx" % int_width

    def _update_widget_view(self):
        """Update view of the widget according to all settings"""
        pass
