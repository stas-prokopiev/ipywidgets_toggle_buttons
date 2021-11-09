"""class ToggleButtonsAutoSize"""
# Standard library imports
import logging

# Third party imports
import ipywidgets

# Local imports
from .layouts import DICT_LAYOUT_HBOX_ANY
from .abc_toggle_buttons import BaseToggleButtons

LOGGER = logging.getLogger(__name__)


class ToggleButtonsAutoSize(BaseToggleButtons):
    """Class to show toggle buttons with auto width"""

    def __init__(self, *args, **kwargs):
        """Initialize object

        Args:
            *args, **kwargs - Arguments to give into ipywidgets.ToggleButtons()
        """
        widget_parent = ipywidgets.ToggleButtons(*args, **kwargs)
        super().__init__(widget_parent, **kwargs)
        hbox_tmp = ipywidgets.HBox(
            [self.widget_parent], layout=DICT_LAYOUT_HBOX_ANY)
        # hbox_tmp.layout = ipywidgets.Layout(**DICT_LAYOUT_HBOX_ANY)
        self.children = [hbox_tmp]
        self._tuple_value_types = (str, )
        self._update_buttons_for_new_options()
        self._update_widget_view()

    def _update_buttons_for_new_options(self):
        """Update buttons if options were changed"""
        int_width = self._get_button_width(self.options)
        self.widget_parent.style.button_width = "%dpx" % int_width

    def _update_widget_view(self):
        """Update view of the widget according to all settings"""
        pass
