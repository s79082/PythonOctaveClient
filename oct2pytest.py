import json
import tkinter as tk

import matplotlib.pyplot as plt
import oct2py

from input import ValueInputGroup
from input_model import ModelInputGroup
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

o.eval("run('stinson.m')", verbose=False)

# setup window
window = tk.Tk()
window.title("Absorptionskoeffizient")

#for f in model:
#    f.load()

def draw_plot():

    # get input
    params = []
    plt.clf()

    for i in value_inputs:
        if not i.getValue():
            return
        params.append(str(i.getValue()))

    #params = list(map(lambda x: str(x), params))

    cmd = "calc({0}, {1}, {2}, {3})".format(*params)
    a = o.eval(cmd, verbose=False, nout=2)
    print(params)
    print(len(a))
    print(a)
    for ret in a:
        print(len(ret))
        print(ret)
        plt.plot(x, ret[0])
    #for f in model:
     #   f.load()
     #   print("ss")
     #   tmp = f.eval(params)[0]
     #   print(tmp)
     #   plt.plot(x, tmp)
    #tmp = model.scripts[0].eval(params)[0]

    #plt.plot(x, tmp)

    plt.xlabel("Frequenz (Hz")
    plt.ylabel("Schallabsorptionskoeffizient")
    plt.show()    
    
    
    #print(a)
    # clear old plot

    # draw
    #plt.plot(x, a)

    
value_inputs = []
value_inputs.append(ValueInputGroup(window, "Porenlänge", draw_plot, 0))
value_inputs.append(ValueInputGroup(window, "Dicke Luftspalt", draw_plot, 1))
value_inputs.append(ValueInputGroup(window, "Porenradius", draw_plot, 2))
value_inputs.append(ValueInputGroup(window, "Porosität", draw_plot, 3))

m = ModelInputGroup(window)
for i in value_inputs:
    m.add_input(i)

# calc button
tk.Button(window, text="berechnen", command=draw_plot).grid(row=len(value_inputs))

# initial draw
draw_plot()

try:
    window.mainloop()
except KeyboardInterrupt:
    exit()


