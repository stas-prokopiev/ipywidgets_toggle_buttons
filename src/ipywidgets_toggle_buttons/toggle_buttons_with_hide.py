"""class ToggleButtonsWithHide"""
# Standard library imports
import logging
from collections import OrderedDict

# Third party imports
import ipywidgets

# Local imports
from .layouts import LAYOUT_HBOX_ANY
from .layouts import LAYOUT_VBOX_ANY
from .abc_toggle_buttons import ToggleButtonsABC

LOGGER = logging.getLogger(__name__)


class ToggleButtonsWithHide(ToggleButtonsABC):
    """Class to show toggle buttons with section of hide options
    """

    def __init__(
            self,
            options_visible=None,
            options_hidden=None,
            _widget_parent=ipywidgets.ToggleButtons, # Don't touch it
            **kwargs
    ):
        """Initialize object

        Args:
            options_visible (list): Main options to show always
            options_hidden (list): Hidden options to show only when asked
            _widget_parent (ipywidget): Technical arg, please don't touch it
        """

        super().__init__(**kwargs)
        self.widget = ipywidgets.VBox(layout=LAYOUT_VBOX_ANY)
        self.widget_parent = _widget_parent()  #
        # hidden attributes to setters
        self._options_visible = []
        self._options_hidden = []
        # Create scaffolds inside self.widgets
        self._create_scaffold_for_widget()
        self._dict_visible_button_by_option = OrderedDict()
        self._dict_hidden_button_by_option = OrderedDict()
        # Set options
        self.options_visible = options_visible
        self.options_hidden = options_hidden
        self._tuple_value_types = (str, )
        if "value" in kwargs:
            self.value = kwargs["value"]
        # self._update_widget_view()

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
        self._options_visible = new_value
        self._create_buttons_for_visible_options()
        # Update hidden options to delete which exists in new visible
        # This will also update the whole widget
        self.options_hidden = self._options_hidden
        self.options = self._options_visible + self._options_hidden

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
        # Filter out from hidden options all options which exists in main
        options_hidden_cleared = []
        for str_option in new_value:
            if str_option not in self.options_visible:
                options_hidden_cleared.append(str_option)
        self._options_hidden = options_hidden_cleared
        self.options = self._options_visible + self._options_hidden
        self._create_buttons_for_hidden_options()
        # self._update_widget_view()

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
        self._create_buttons_for_hidden_options()

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
            self.widget.children = [self._widget_hbox_main]
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
            self._wid_but_hide_show.description = "Hide Options below"
            self.widget.children = [
                self._widget_hbox_main,
                self._widget_hbox_middle_buttons,
                self._widget_hbox_hidden
            ]
        else:
            self.widget.children = [
                self._widget_hbox_main,
                self._widget_hbox_middle_buttons
            ]
            self._wid_but_hide_show.description = "Show Hidden Options"
        return None

    def _create_scaffold_for_widget(self):
        """Create scaffold of ipywidget Boxes for self.widget"""
        # Main buttons box
        self._widget_hbox_main = ipywidgets.HBox(layout=LAYOUT_HBOX_ANY)
        self._widget_hbox_main.layout.flex_flow = "row wrap"
        # Middle buttons box
        self._widget_hbox_middle_buttons = ipywidgets.HBox(layout=LAYOUT_HBOX_ANY)
        self._create_middle_buttons()
        # Hidden buttons box
        self._widget_hbox_hidden = ipywidgets.HBox(layout=LAYOUT_HBOX_ANY)
        self._widget_hbox_hidden.layout.flex_flow = "row wrap"


    def _on_click_button_to_choose_option(self, wid_but):
        """What to do when button to choose options clicked"""
        self.value = wid_but.description


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
        int_button_width = self.func_to_get_option_width(["Show Hidden options"])

        self._wid_but_hide_show = ipywidgets.ToggleButton(
            value=False,
            description="Show Hidden options",
            button_style="info",
            width="%dpx" % int_button_width
        )
        self._wid_but_hide_show.observe(
            lambda _: self._update_widget_view(), "value")
        self._widget_but_hidden_option_selected = ipywidgets.Button(
            description="...", disabled=True)
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
            but_wid.on_click(self._on_click_button_to_choose_option)
            self._dict_hidden_button_by_option[str_option] = but_wid
            list_buttons.append(but_wid)

        self._widget_hbox_hidden.children = list_buttons
        # Update width of middle buttons
        int_button_width2 = self.func_to_get_option_width(
            self.options_hidden + ["Show Hidden options"])
        self._widget_but_hidden_option_selected.layout = {
            "width": "%dpx" % int_button_width2}
