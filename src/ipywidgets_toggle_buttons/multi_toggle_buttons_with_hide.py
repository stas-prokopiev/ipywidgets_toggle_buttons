"""class MultiToggleButtonsWithHide"""
# Standard library imports
import logging

# Third party imports
import ipywidgets

# Local imports
from .toggle_buttons_with_hide import ToggleButtonsWithHide

LOGGER = logging.getLogger(__name__)


class MultiToggleButtonsWithHide(ToggleButtonsWithHide):
    """Class to show multi toggle buttons with section of hide options
    """

    def __init__(
            self,
            max_chosen_values=999,
            options_visible=None,
            options_hidden=None,
            **kwargs
    ):
        """"""
        # Main attributes
        super().__init__(
            options_visible=options_visible,
            options_hidden=options_hidden,
            _widget_parent=ipywidgets.SelectMultiple,
            **kwargs
        )
        self.max_chosen_values = max_chosen_values
        self._update_width_of_middle_buttons_at_start()
        self._tuple_value_types = (list, tuple)

    def _update_width_of_middle_buttons_at_start(self):
        """Update width for buttons in middle box"""
        int_button_width = self.func_to_get_option_width(
            ["Hidden options selected: 100"])
        self._widget_but_hidden_option_selected.layout.width = \
            "%dpx" % int_button_width
        self._wid_but_hide_show.layout.width = "%dpx" % int_button_width

    def _on_click_button_to_choose_option(self, wid_but):
        """What to do when button to choose options clicked"""
        list_cur_values = list(self.value)
        str_value_to_alter = wid_but.description
        if str_value_to_alter in list_cur_values:
            if str_value_to_alter in list_cur_values:
                list_cur_values.remove(str_value_to_alter)
                self.value = list_cur_values
        else:
            list_cur_values += [str_value_to_alter]
            self.value = list_cur_values
        # self._update_widget_view()

    def _update_widget_view(self):
        """Update view of the widget according to all settings"""
        self.turn_off_all_buttons()
        for str_value in self.value:
            # Update main buttons
            if str_value in self._dict_visible_button_by_option:
                but = self._dict_visible_button_by_option[str_value]
                but.button_style = "success"
        # If there are no hidden options then
        # don't create buttons for showing hidden options
        if not self.options_hidden:
            self.widget.children = [self._widget_hbox_main]
            return None
        int_hidden_options_selected = 0
        for str_value in self.value:
            # Update hidden buttons
            if str_value in self._dict_hidden_button_by_option:
                but = self._dict_hidden_button_by_option[str_value]
                but.button_style = "success"
                int_hidden_options_selected += 1

        self._widget_but_hidden_option_selected.description = \
            "Hidden options selected: %d" % int_hidden_options_selected
        if int_hidden_options_selected:
            self._widget_but_hidden_option_selected.button_style = "success"
        else:
            self._widget_but_hidden_option_selected.button_style = ""
        # Choose to show all boxes if button to_show_hidden pressed
        if self._wid_but_hide_show.value:
            self._wid_but_hide_show.description = "Hide Options below"
            self.widget.children = [
                self._widget_hbox_main,
                self._widget_hbox_middle_buttons,
                self._widget_hbox_hidden
            ]
            return None
        # Do not show hidden options
        self.widget.children = [
            self._widget_hbox_main,
            self._widget_hbox_middle_buttons
        ]
        self._wid_but_hide_show.description = "Show Hidden Options"
        return None
