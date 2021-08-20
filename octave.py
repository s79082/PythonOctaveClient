
class OctaveFunction:
    
    def __init__(self, name, file_name, result_name, octave):
        self.name = name
        self.octave = octave
        self.file_name = file_name

    def load(self):
        cmd = "run({0})".format("'" + self.file_name + "'")

        self.octave.eval(cmd, verbose=False)

    def eval(self, param_list):
        params = ""
        for p in param_list:
            params += ( p + ",")

        # remove last ','
        params = params[:-1]
        cmd = "{0}({1})".format(self.name, params)

        return self.octave.eval(cmd, verbose=False)


class OctaveModel:
    """
    An OctaveModel holds multiple OctaveScripts belonging to one model
    """
    def __init__(self, name):
        self.name = name
        self.scripts = []

        self.current = -1
        self.size = 0

    def add_script(self, script):
        """
        Adds an OctaveScript to the collection of scripts
        """
        self.scripts.append(script)
        self.size = len(self.scripts)

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.size:
            return self.scripts[self.current]
        else:
            self.current = -1
            raise StopIteration



if __name__ == "__main__":
    m = OctaveModel("soosmodel")
    m.add_script("soosscript1")
    m.add_script("soosscript2")
    print(m.scripts)
    for s in m:
        print(s)