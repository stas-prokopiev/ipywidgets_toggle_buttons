"""Abstract class for all toggle buttons"""
# Standard library imports
import logging
from collections import OrderedDict

# Third party imports
import ipywidgets

# Local imports
from .abc_toggle_buttons import BaseToggleButtons
from .layouts import DICT_LAYOUT_HBOX_ANY

LOGGER = logging.getLogger(__name__)


class BaseToggleButtonsWithHide(BaseToggleButtons):
    """Abstract class for all toggle buttons

    Values are stored in self.widget_parent when displayed is self.widget
    Which is updated in the moment when display() is launched
    """

    def __init__(
            self,
            widget_parent,
            options_visible=None,
            options_hidden=None,
            **kwargs
    ):
        """Initialize object"""
        super().__init__(widget_parent, **kwargs)
        # hidden attributes to setters
        self._options_visible = []
        self._options_hidden = []
        self._bool_is_hidden_options_created = False
        # Create scaffolds inside self.widgets
        self._create_scaffold_for_widget()
        self._dict_visible_button_by_option = OrderedDict()
        self._dict_hidden_button_by_option = OrderedDict()
        # Set options
        self.options_visible = options_visible
        self.options_hidden = options_hidden
        self._update_buttons_for_new_options()

    @property
    def options_visible(self):
        """Getter for visible options used in widget"""
        return self._options_visible

    @options_visible.setter
    def options_visible(self, new_value):
        """Setter for visible options in widget

        Args:
            new_value (list or tuple): New options to set for widgets
        """
        if new_value is None:
            new_value = []
        if set(new_value) == set(self.options_visible):
            return None
        self._options_visible = new_value
        self._create_buttons_for_visible_options()
        # Update hidden options to delete which exists in new visible
        # This will also update the whole widget
        self.options_hidden = self._options_hidden
        self.options = self._options_visible + self._options_hidden
        self._update_widget_view()

    @property
    def options_hidden(self):
        """Getter for hidden options used in widget"""
        return self._options_hidden

    @options_hidden.setter
    def options_hidden(self, new_value):
        """Setter for hidden options in widget

        Args:
            new_value (list or tuple): New options to set for widgets
        """
        if new_value is None:
            new_value = []
        if set(new_value) == set(self.options_hidden):
            return None
        # Filter out from hidden options all options which exists in main
        options_hidden_cleared = []
        for str_option in new_value:
            if str_option not in self.options_visible:
                options_hidden_cleared.append(str_option)
        self._options_hidden = options_hidden_cleared
        self.options = self._options_visible + self._options_hidden
        # self._create_buttons_for_hidden_options()
        self._update_widget_view()

    def turn_off_all_buttons(self):
        """Mark all buttons as not clicked"""
        for str_option in self._dict_visible_button_by_option:
            but = self._dict_visible_button_by_option[str_option]
            but.button_style = ""
        for str_option in self._dict_hidden_button_by_option:
            but = self._dict_hidden_button_by_option[str_option]
            but.button_style = ""
        # Change style of selected hidden button
        # self._widget_but_hidden_option_selected.description = "..."
        # self._widget_but_hidden_option_selected.button_style = ""

    def _update_buttons_for_new_options(self):
        """Update buttons if options were changed"""
        self._create_buttons_for_visible_options()
        self._bool_is_hidden_options_created = False
        # self._create_buttons_for_hidden_options()

    def _create_scaffold_for_widget(self):
        """Create scaffold of ipywidget Boxes for self"""
        # Main buttons box
        self._widget_hbox_main = ipywidgets.HBox()
        self._widget_hbox_main.layout = ipywidgets.Layout(**DICT_LAYOUT_HBOX_ANY)
        # self._widget_hbox_main.layout.flex_flow = "row wrap"
        # Middle buttons box
        self._widget_hbox_middle_buttons = ipywidgets.HBox()
        self._widget_hbox_middle_buttons.layout = ipywidgets.Layout(**DICT_LAYOUT_HBOX_ANY)
        self._create_middle_buttons()
        # Hidden buttons box
        self._widget_hbox_hidden = ipywidgets.HBox()
        self._widget_hbox_hidden.layout = ipywidgets.Layout(**DICT_LAYOUT_HBOX_ANY)
        # self._widget_hbox_hidden.layout.flex_flow = "row wrap"

    def _create_buttons_for_visible_options(self):
        """Create buttons for all visible options"""
        self._dict_visible_button_by_option = OrderedDict()
        int_button_width = self.func_to_get_option_width(self.options_visible)
        list_buttons = []
        for str_option in list(self.options_visible):
            but_wid = ipywidgets.Button(
                description=str_option,
                layout={"width": "%dpx" % int_button_width}
            )
            but_wid.on_click(self._on_click_button_to_choose_option)
            self._dict_visible_button_by_option[str_option] = but_wid
            list_buttons.append(but_wid)
        self._widget_hbox_main.children = list_buttons

    def _create_middle_buttons(self):
        """Create buttons which are in charge what to do with hidden buttons"""
        self._wid_but_hide_show = ipywidgets.ToggleButton(
            value=False,
            description="Show Hidden options",
            button_style="info",
        )
        self._wid_but_hide_show.layout.width = "40%"
        self._wid_but_hide_show.observe(
            lambda _: self._update_widget_view(), "value")
        self._widget_but_hidden_option_selected = ipywidgets.Button(
            description="...", disabled=True)
        self._widget_but_hidden_option_selected.layout.width = "40%"
        self._widget_hbox_middle_buttons.children = [
            self._widget_but_hidden_option_selected, self._wid_but_hide_show]

    def _create_buttons_for_hidden_options(self):
        """Create buttons for all hidden options"""
        self._dict_hidden_button_by_option = OrderedDict()
        int_button_width = self.func_to_get_option_width(self.options_hidden)
        list_buttons = []
        for str_option in list(self.options_hidden):
            but_wid = ipywidgets.Button(
                description=str_option,
                layout={"width": "%dpx" % int_button_width}
            )
            if str_option in self.value:
                but_wid.button_style = "success"
            but_wid.on_click(self._on_click_button_to_choose_option)
            self._dict_hidden_button_by_option[str_option] = but_wid
            list_buttons.append(but_wid)
        self._widget_hbox_hidden.children = list_buttons
