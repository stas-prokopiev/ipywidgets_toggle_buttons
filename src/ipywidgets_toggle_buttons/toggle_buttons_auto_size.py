"""class ToggleButtonsAutoSize"""
# Standard library imports
import logging

# Third party imports
import ipywidgets

# Local imports
from .layouts import LAYOUT_HBOX_ANY
from .layouts import LAYOUT_VBOX_ANY
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
        hbox_tmp = ipywidgets.HBox([self.widget_parent], layout=LAYOUT_HBOX_ANY)
        hbox_tmp.layout.flex_flow = "row wrap"
        self.widget = ipywidgets.VBox([hbox_tmp], layout=LAYOUT_VBOX_ANY)
        self._tuple_value_types = (str, )

    def _update_buttons_for_new_options(self):
        """Update buttons if options were changed"""
        int_width = self.func_to_get_option_width(self.options)
        self.widget_parent.style.button_width = "%dpx" % int_width

    def _update_widget_view(self):
        """Update view of the widget according to all settings"""
        pass
