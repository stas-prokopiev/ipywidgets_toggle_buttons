""""""
# Standard library imports

# Third party imports
from IPython.display import display
from ipywidgets_toggle_buttons import ToggleButtonsAutoSize

# Local imports

# def test_toggle_buttons_auto_size():
def test():
    """"""
    wid = ToggleButtonsAutoSize(options=[str(i) for i in range(10)])
    display(wid)
    def on_value_change(_):
        print("ho")
    wid.observe(on_value_change, 'value')
    wid.value = "2"
    try:
        wid.value = ["2"]
    except ValueError:
        pass
    wid.options = list(wid.options) + ["ajhfkaghnkandjgnakdn"]
    wid.layout.width = "700px"
    print(wid.options)
    wid._ipython_display_()
