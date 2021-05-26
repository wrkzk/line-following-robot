# Read a file containing the path, and return the result as a list
def read_file():
    filename = "param.txt"
    movements = []

    with open(filename) as param_file:
        for line in param_file:
            if line[0] == "P":
                movements = line[2:].strip().split(',')
                return movements
                                
if __name__ == "__main__":
    print(read_file())
