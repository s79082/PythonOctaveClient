import json
import tkinter as tk

import matplotlib.pyplot as plt
import oct2py

from input import ValueInputGroup
from octave import OctaveFunction, OctaveModel

OUTPUT_LEN = 1241

# load script path
with open("config.json") as f:
    config_file = json.load(f)

script_path = config_file["script_path"]



# setup
o = oct2py.Oct2Py()
o.addpath(script_path)


model = OctaveModel("stinson")
model.add_script(OctaveFunction("calc", "stinson.m", "alpha21", o))
model.add_script(OctaveFunction("calc2", "stinson_2.m", "alpha2", o))

# setup x axis
x = range(OUTPUT_LEN)

for f in model:
    f.load()
    tmp = f.eval(["15e-3", "15e-3", "7e-4", "1e-1"])[0]
    print(tmp)
    plt.plot(x, tmp)
plt.show()


o.eval("run('stinson.m')", verbose=False)

# setup window
window = tk.Tk()
window.title("Absorptionskoeffizient")



def draw_plot():

    # get input
    params = []
    for i in value_inputs:
        if not i.getValue():
            return
        params.append(i.getValue())
    
    cmd = "calc({0}, {1}, {2}, {3})".format(*params)
    a = o.eval(cmd, verbose=False)[0]
    print(a)
    # clear old plot
    plt.clf()

    # draw
    #plt.plot(x, a)
    plt.xlabel("Frequenz (Hz")
    plt.ylabel("Schallabsorptionskoeffizient")
    plt.show()
    
value_inputs = []
value_inputs.append(ValueInputGroup(window, "Porenlänge", draw_plot, 0))
value_inputs.append(ValueInputGroup(window, "Dicke Luftspalt", draw_plot, 1))
value_inputs.append(ValueInputGroup(window, "Porenradius", draw_plot, 2))
value_inputs.append(ValueInputGroup(window, "Porosität", draw_plot, 3))

# calc button
tk.Button(window, text="berechnen", command=draw_plot).grid(row=len(value_inputs))

# initial draw
draw_plot()

try:
    window.mainloop()
except KeyboardInterrupt:
    exit()


