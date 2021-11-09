"""Abstract class for all toggle buttons"""
# Standard library imports
import logging
from abc import abstractmethod

# Third party imports
from ipywidgets import VBox

# Local imports
from .layouts import DICT_LAYOUT_VBOX_ANY

LOGGER = logging.getLogger(__name__)


class BaseToggleButtons(VBox):
    """Abstract class for all toggle buttons

    Values are stored in self.widget_parent when displayed is self.widget
    Which is updated in the moment when display() is launched
    """

    def __init__(self, widget_parent, **kwargs):
        """Initialize object"""
        self.widget_parent = widget_parent
        self.observe = self.widget_parent.observe
        super().__init__(layout=DICT_LAYOUT_VBOX_ANY)
        self._tuple_value_types = (str, list, tuple)
        #####
        # self._get_button_width = self._get_buttons_min_width_needed

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

    @staticmethod
    def _get_button_width(iter_options):
        """Get width to use for buttons with given options

        Args:
            iter_options (any iterable): options for toggle buttons

        Returns:
            int: width in px to use for buttons with given options
        """
        if not iter_options:
            return 100
        list_lengths = []
        for option in iter_options:
            int_length = 5
            for str_letter in str(option):
                int_length += 8
                if str_letter.isupper():
                    int_length += 4
            list_lengths.append(int_length)
        int_button_width = max(list_lengths)
        int_button_width = max(120, int_button_width)
        int_button_width = min(300, int_button_width)
        return int_button_width
