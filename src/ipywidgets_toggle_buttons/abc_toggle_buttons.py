"""Abstract class for all toggle buttons"""
# Standard library imports
import logging
from abc import abstractmethod

# Third party imports
from ipywidgets import VBox

# Local imports
from .utility import get_buttons_min_width_needed
from .layouts import DICT_LAYOUT_VBOX_ANY

LOGGER = logging.getLogger(__name__)


class BaseToggleButtons(VBox):
    """Abstract class for all toggle buttons

    Values are stored in self.widget_parent when displayed is self.widget
    Which is updated in the moment when display() is launched
    """

    def __init__(self, widget_parent, func_to_get_option_width=None, **kwargs):
        """Initialize object"""
        self.widget_parent = widget_parent
        self.observe = self.widget_parent.observe
        super().__init__(layout=DICT_LAYOUT_VBOX_ANY)
        self._tuple_value_types = (str, list, tuple)
        #####
        self.func_to_get_option_width = get_buttons_min_width_needed
        if func_to_get_option_width is not None:
            self.func_to_get_option_width = func_to_get_option_width

    @abstractmethod
    def _update_widget_view(self):
        """ABSTRACT: Update view of widget according to self.widget_parent"""

    @abstractmethod
    def _update_buttons_for_new_options(self):
        """ABSTRACT: Update buttons if options were changed"""

    @property
    def value(self):
        """Getter for value used in widget"""
        return self.widget_parent.value

    @value.setter
    def value(self, new_value):
        """Setter for value used in widget with update of widget view

        Args:
            new_value (Any): Value to set for widget
        """
        if new_value != self.value:
            self.widget_parent.value = self._check_type_of_new_value(new_value)
            self._update_widget_view()

    @property
    def options(self):
        """Getter for options used in widget"""
        return self.widget_parent.options

    @options.setter
    def options(self, new_value):
        """Setter for options used in widget with update of widget view

        Args:
            new_value (list or tuple): New options to set for widgets
        """
        if new_value is None:
            new_value = []
        if set(new_value) == set(self.options):
            return None
        self.widget_parent.options = new_value
        self._update_buttons_for_new_options()

    def _check_type_of_new_value(self, new_value):
        """Check that the new value has right type"""
        if not isinstance(new_value, self._tuple_value_types):
            raise ValueError(
                f"New value for widget should be: {self._tuple_value_types}"
                f"but not: {type(new_value)}"
            )
        if hasattr(self, "max_chosen_values"):
            LOGGER.debug("Max number of pressed buttons reached")
            new_value = new_value[-self.max_chosen_values:]
        return new_value
