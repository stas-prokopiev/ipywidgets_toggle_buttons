"""class MultiToggleButtons"""
# Standard library imports
import logging
from collections import OrderedDict

# Third party imports
import ipywidgets

# Local imports
from .layouts import DICT_LAYOUT_HBOX_ANY
from .abc_toggle_buttons import BaseToggleButtons

LOGGER = logging.getLogger(__name__)


class MultiToggleButtons(BaseToggleButtons):
    """Class to show multi toggle buttons with auto width"""

    def __init__(self, max_chosen_values=999, **kwargs):
        """Initialize object

        Args:
            max_chosen_values (int): Max buttons can be activated at once
        """
        # Main attributes
        widget_parent = ipywidgets.SelectMultiple(**kwargs)
        super().__init__(widget_parent, **kwargs)
        self.max_chosen_values = max_chosen_values
        self._tuple_value_types = (list, tuple)
        # Additional (Hidden) attributes
        self.options = kwargs.get("options", [])
        self._dict_but_by_option = OrderedDict()
        self._update_buttons_for_new_options()
        self.value = kwargs.get("value", [])
        self._update_widget_view()

    def _update_widget_view(self):
        """Update view of the widget according to all settings"""
        for str_option in self._dict_but_by_option:
            but_wid = self._dict_but_by_option[str_option]
            if str_option in self.value:
                but_wid.value = True
                but_wid.button_style = "success"
            else:
                but_wid.value = False
                but_wid.button_style = ""

    def _on_click_button_to_choose_option(self, dict_changes):
        """What to do when button to choose options clicked"""
        wid_but = dict_changes["owner"]
        str_value_to_alter = wid_but.description
        list_cur_values = list(self.value)
        if dict_changes["new"]:
            if str_value_to_alter not in list_cur_values:
                list_cur_values += [str_value_to_alter]
                self.value = list_cur_values
        else:
            if str_value_to_alter in list_cur_values:
                list_cur_values.remove(str_value_to_alter)
                self.value = list_cur_values

    def _update_buttons_for_new_options(self):
        """Update buttons if options were changed"""
        list_buttons = []
        self._dict_but_by_option = OrderedDict()
        int_width = self._get_button_width(self.options)
        for str_option in list(self.options):
            but = ipywidgets.ToggleButton(
                description=str_option,
                layout={"width": "%dpx" % int_width}
            )
            but.observe(self._on_click_button_to_choose_option, "value")
            self._dict_but_by_option[str_option] = but
            list_buttons.append(but)
        hbox_tmp = ipywidgets.HBox(list_buttons, layout=DICT_LAYOUT_HBOX_ANY)
        self.children = [hbox_tmp]
