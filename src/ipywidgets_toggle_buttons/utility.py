"""Different small functions"""
# Standard library imports
import logging

# Third party imports

# Local imports

LOGGER = logging.getLogger(__name__)


def get_buttons_min_width_needed(iter_options):
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
