def read_file():
    filename = "param.txt"
    movements = []

    with open(filename) as param_file:
        for line in param_file:
            if line[0] == "P":
                movements = line[2:].strip().split(',')
                movements_reverse = movements.copy()
                movements_reverse.reverse()
                
                i = 0
                for x in range(0, len(movements_reverse)):
                    if movements_reverse[i] == "R":
                        movements_reverse[i] = "L"
                    elif movements_reverse[i] == "L":
                        movements_reverse[i] = "R"
                    i += 1

                movements.append("TA")
                movements.extend(movements_reverse)
                movements.append("TA")
                return movements
                                
if __name__ == "__main__":
    print(read_file())
