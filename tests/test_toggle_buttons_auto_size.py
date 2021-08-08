""""""
# Standard library imports

# Third party imports
from IPython.display import display
from ipywidgets_toggle_buttons import ToggleButtonsAutoSize

# Local imports

def test_toggle_buttons_auto_size():
    """"""
    wid = ToggleButtonsAutoSize(options=[str(i) for i in range(10)])
    display(wid)
