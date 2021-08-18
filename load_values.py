def load_values_from_file(file_name):

    with open(file_name) as f:
        
        lines = f.readlines()
        # remove the header
        del lines[0]
        
        return list(map(lambda ln: float(ln.split(",")[1]), lines))
        #for line in lines:
            #line_list = line.split(",")
