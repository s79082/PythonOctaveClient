import tkinter as tk

class ModelInputGroup:
    """
    Each ModelInputGroup groups the ValueInputGroups assoziatet with this model. 
    """
    def __init__(self, root) -> None:
        self.value_inputs = []
        self.var_active = tk.BooleanVar(value=True)
        self.cb_active = tk.Checkbutton(root, variable=self.var_active, command=self._on_active_toggle)
        self.cb_active.grid(row=5, column=2)

    def add_input(self, input):
        self.value_inputs.append(input)

    def _on_active_toggle(self):
        print(self.var_active)
        for i in self.value_inputs:
            if self.var_active.get():
                i.hide()
            else:
                i.show()

