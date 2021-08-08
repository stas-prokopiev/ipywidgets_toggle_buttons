""""""
# Standard library imports

# Third party imports
from IPython.display import display
from ipywidgets_toggle_buttons import MultiToggleButtons

# Local imports

def test():
    """"""
    wid = MultiToggleButtons(
        max_pressed_buttons=2, options=[str(i) for i in range(10)])
    display(wid)
    wid.options = list(wid.options) + ["ajhfkaghnkandjgnakdn"]
    print(wid.layout)
    wid.layout.width = "600px"
    wid.value = ["2"]
    wid.options = ["1", "3", "4"]
    print(wid.options)
