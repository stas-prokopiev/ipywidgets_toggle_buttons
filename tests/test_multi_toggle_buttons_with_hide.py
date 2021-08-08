""""""
# Standard library imports

# Third party imports
from IPython.display import display
from ipywidgets_toggle_buttons import MultiToggleButtonsWithHide

# Local imports


def test():
    """"""
    wid = MultiToggleButtonsWithHide(
        options_visible=[str(i) for i in range(10)],
    #     options_hidden=[],
        options_hidden=[str(i) for i in range(5, 15)],
    )
    display(wid)
    print(wid.options_hidden)
    print(wid.options)
    print(wid.value)
    wid.options_visible = list(wid.options_visible) + ["ajhfkaghnkandjgnakdn"]
    def on_value_change(_):
        print("ho")

    wid.observe(on_value_change, 'value')
    wid.value = ["12"]
    wid.layout.width = "700px"