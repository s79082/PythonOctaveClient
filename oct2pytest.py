import json
from load_values import load_values_from_file, read_file
import tkinter as tk

import matplotlib.pyplot as plt
import oct2py

from input import ValueInputGroup, UnitValueInputGroup
from input_model import ModelInputGroup
from octave import OctaveFunction, OctaveModel

#OUTPUT_LEN = 1241
OUTPUT_LEN = 126

STRING_NOTHING_LOADED = "keine Datei geladen"

# load script path
with open("config.json") as f:
    config_file = json.load(f)

script_path = config_file["script_path"]

models = config_file["models"]

# setup window
window = tk.Tk()
window.title("Absorptionskoeffizient")

loaded_values = None
loaded_filename = ""
var_draw_loaded_values = tk.BooleanVar(value=True)
label_loaded_filename = tk.Label(window, text=STRING_NOTHING_LOADED)
label_loaded_filename.grid(row=6, column=1)
# setup
o = oct2py.Oct2Py()
o.addpath(script_path)

# setup x axis
x = range(OUTPUT_LEN)
x = range(20, 6300, 50)
o.eval("run('gegenueberstellung.m')", verbose=False)


vars = []
for _ in models:
    vars.append(tk.BooleanVar(master=window, value=True))

vars = [ tk.BooleanVar(master=window, value=True) for _ in models ]
cb_vars = list(zip(models, vars))

#for f in model:
#    f.load()

def draw_plot():

    # calculate frequency for xaxis
    x = calc_xaxis()

    # get input
    params = []
    plt.clf()

    for i in value_inputs:
        if not i.getValue():
            return
        #params.append(str(i.getValue()))
        params.append(i.getNormalizedValue())

    # append frequency params
    params.append(tb_freq_start.get())
    params.append(tb_freq_end.get())
    params.append(tb_freq_step.get())


    #params = list(map(lambda x: str(x), params))

    cmd = "geg({0}, {1}, {2}, {3}, {4}, {5}, {6})".format(*params)
    a = o.eval(cmd, verbose=False, nout=10)
    for i, ret in enumerate(a):

        if cb_vars[i][1].get():
            plt.plot(x, ret[0], label=models[i])
    #plt.xticks(x, x)
    #plt.xlim((20, 6300))

    if loaded_values and var_draw_loaded_values.get():
        plt.plot(x,loaded_values, label=loaded_filename.split("/")[-1])

    #plt.plot(load_values_from_file("test.txt"))
    #for f in model:
     #   f.load()
     #   print("ss")
     #   tmp = f.eval(params)[0]
     #   print(tmp)
     #   plt.plot(x, tmp)
    #tmp = model.scripts[0].eval(params)[0]

    #plt.plot(x, tmp)

    plt.xlabel("Frequenz (Hz)")
    plt.ylabel("Schallabsorptionskoeffizient")
    plt.legend(loc="upper left")
    plt.show()    
    
    
    #print(a)
    # clear old plot

    # draw
    #plt.plot(x, a)

    
value_inputs = []
value_inputs.append(UnitValueInputGroup(window, "Porenlänge", draw_plot, 0))
value_inputs.append(UnitValueInputGroup(window, "Dicke Luftspalt", draw_plot, 1))
value_inputs.append(UnitValueInputGroup(window, "Porenradius", draw_plot, 2))
value_inputs.append(ValueInputGroup(window, "Porosität", draw_plot, 3))

#m = ModelInputGroup(window)
#for i in value_inputs:
#    m.add_input(i)
#def get_load_and_draw(label):
def load_and_draw():
    global loaded_values, loaded_filename, label_loaded_filename
        #print(label_loaded_filename)
    try:
        loaded_filename = tk.filedialog.askopenfilename()
        loaded_values = load_values_from_file(loaded_filename)
        label_loaded_filename["text"] = loaded_filename.split("/")[-1]
            #label_loaded_filename.text = loaded_filename.split("/")[-1]
    except Exception:
        tk.messagebox.showerror(title="Fehler", message="Fehler beim laden der Datei.")
            #label_loaded_filename.text = STRING_NOTHING_LOADED
        label_loaded_filename.text = STRING_NOTHING_LOADED

    draw_plot()

    #return load_and_draw

len_value_inputs = len(value_inputs)
# calc button
tk.Button(window, text="berechnen", command=draw_plot).grid(row=len_value_inputs)
row_loaded = len_value_inputs + 1
tk.Button(window, text="load values", command=load_and_draw).grid(row=row_loaded)
tk.Checkbutton(window, variable=var_draw_loaded_values, command=draw_plot).grid(row=row_loaded, column=2)

def calc_xaxis():
    #global x
    start = int(tb_freq_start.get())
    step =  int(tb_freq_step.get())
    end = int(tb_freq_end.get())
    x = range(start, end, step)
    #print(list(x)[-1])
    return x
    

tb_freq_start = tk.Entry(window)
tb_freq_start.insert(tk.END, "20")
tb_freq_start.grid()
tb_freq_step = tk.Entry(window)
tb_freq_step.insert(tk.END, "50")
tb_freq_step.grid()
var_freq_end = tk.StringVar()
tb_freq_end = tk.Entry(window, textvariable=var_freq_end)
tb_freq_end.insert(tk.END, "6300") 
tb_freq_end.grid()



for m, v in cb_vars:
    tk.Checkbutton(window, variable=v, text=m, command=draw_plot).grid() 

#lb = tk.Listbox(window)
#lb.grid()
#for i,m in enumerate(models):
#    lb.insert(i+1, m)


# initial draw
draw_plot()

try:
    window.mainloop()
except KeyboardInterrupt:
    exit()


