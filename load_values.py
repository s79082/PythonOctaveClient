
import typing


def load_values_from_file(file_name):

    with open(file_name) as f:
        
        lines = f.readlines()
        # remove the header
        lines = lines[3:]

        return list(map(lambda ln: float((ln.split()[1]).replace(",", ".")), lines))

def read_file(file_obj: typing.TextIO):
    lines = file_obj.readlines()
    file_obj.close()
    # remove the heasder
    lines = lines[3:]

    return list(map(lambda ln: float((ln.split()[1]).replace(",", ".")), lines))
