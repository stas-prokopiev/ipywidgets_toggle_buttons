"""class ToggleButtonsWithHide"""
# Standard library imports
import logging

# Third party imports
import ipywidgets

# Local imports
from .abc_toggle_buttons_with_hide import BaseToggleButtonsWithHide

LOGGER = logging.getLogger(__name__)


class ToggleButtonsWithHide(BaseToggleButtonsWithHide):
    """Class to show toggle buttons with section of hide options
    """

    def __init__(
            self,
            options_visible=None,
            options_hidden=None,
            **kwargs
    ):
        """Initialize object

        Args:
            options_visible (list): Main options to show always
            options_hidden (list): Hidden options to show only when asked
            _widget_parent (ipywidget): Technical arg, please don't touch it
        """
        widget_parent = ipywidgets.ToggleButtons()  #
        super().__init__(
            widget_parent,
            options_visible=options_visible,
            options_hidden=options_hidden,
            **kwargs
        )

        self._tuple_value_types = (str, )
        if "value" in kwargs:
            self.value = kwargs["value"]
        self._update_widget_view()

    def _update_widget_view(self):
        """Update view of the widget according to all settings"""
        self.turn_off_all_buttons()
        # Update main buttons
        if self.value in self._dict_visible_button_by_option:
            but = self._dict_visible_button_by_option[self.value]
            but.button_style = "success"
        # If there are no hidden options then
        # don't create buttons for showing hidden options
        if not self.options_hidden:
            self.children = [self._widget_hbox_main]
            return None
        # Update hidden buttons
        if self.value in self._dict_hidden_button_by_option:
            but = self._dict_hidden_button_by_option[self.value]
            but.button_style = "success"
            self._widget_but_hidden_option_selected.description = self.value
            self._widget_but_hidden_option_selected.button_style = "success"
        else:
            self._widget_but_hidden_option_selected.description = "..."
            self._widget_but_hidden_option_selected.button_style = ""
        # Choose which boxes to show
        if self._wid_but_hide_show.value:
            if not self._bool_is_hidden_options_created:
                self._create_buttons_for_hidden_options()
                self._bool_is_hidden_options_created = True
            self._wid_but_hide_show.description = "Hide Options below"
            self.children = [
                self._widget_hbox_main,
                self._widget_hbox_middle_buttons,
                self._widget_hbox_hidden
            ]
        else:
            self.children = [
                self._widget_hbox_main,
                self._widget_hbox_middle_buttons
            ]
            self._wid_but_hide_show.description = "Show Hidden Options"
        return None

    def _on_click_button_to_choose_option(self, wid_but):
        """What to do when button to choose options clicked"""
        self.value = wid_but.description
