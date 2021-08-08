"""Abstract class for all toggle buttons"""
# Standard library imports
from abc import ABC, abstractmethod

# Third party imports

# Local imports
from .utility import get_buttons_min_width_needed


class ToggleButtonsABC(ABC):
    """Abstract class for all toggle buttons

    Values are stored in self.widget_parent when displayed is self.widget
    Which is updated in the moment when display() is launched
    """

    def __init__(self, **kwargs):
        """Initialize object"""
        self.widget = None  # This attribute should be redefined
        self.widget_parent = None
        self._tuple_value_types = (str, list, tuple)
        #####
        self.func_to_get_option_width = kwargs.get(
            "func_to_get_option_width", get_buttons_min_width_needed)

    @abstractmethod
    def _update_widget_view(self):
        """ABSTRACT: Update view of widget according to self.widget_parent"""

    @abstractmethod
    def _update_buttons_for_new_options(self):
        """ABSTRACT: Update buttons if options were changed"""

    def _ipython_display_(self):
        """
        Showing created self.widget in the class object is displayed in jupyter
        """
        self._update_widget_view()
        return self.widget._ipython_display_()

    def __repr__(self):
        """String representation for widget"""
        self._update_widget_view()
        return self.widget.__repr__()

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
        self._check_new_value(new_value)
        self.widget_parent.value = new_value
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
        self.widget_parent.options = new_value
        self._update_buttons_for_new_options()

    def observe(self, *args, **kwargs):
        """Method for direct observe of changes in widget"""
        return self.widget_parent.observe(*args, **kwargs)

    @property
    def layout(self):
        """Property for direct modify of widgets layout

        Returns:
            ipywidgets.Layout(): Layout of shown widget
        """
        return self.widget.layout

    def _check_new_value(self, new_value):
        """Check that the new value has right type"""

        if not isinstance(new_value, self._tuple_value_types):
            raise ValueError(
                f"New value for widget should be: {self._tuple_value_types}"
                f"but not: {type(new_value)}"
            )
