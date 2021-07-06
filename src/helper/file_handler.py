import matplotlib.pyplot as plt
import matplotlib.patches as patches

BIG_BOARD_WIDTH = 2800
BIG_BOARD_HEIGHT = 2070

class FileHandler:
    def __init__(self):
        pass

    def read_data(self, file_name):
        try:
            with open(file_name, "r") as f:
                string_data = [line.split() for line in f]
            
            data = [[int(val) for val in row] for row in string_data]
            return data

        except:
            print("Could not read data from file " + file_name)
            print('This file should be placed in directory from which program is executed')
            exit(-1)

    def save_data_as_txt(self, file_name, best, data_for_ga):
        try:
            fitness = best[0]
            solution = best[1]
            sum = 0
            with open(file_name, "w") as f:
                print(int(fitness), file=f)
                for idx, board in enumerate(solution):
                    width = data_for_ga[idx]["width"]
                    height = data_for_ga[idx]["height"]
                    x = board["x"]
                    y = board["y"]
                    r = board["r"]
                    if board["e"] == 0:
                        x = -1
                        y = -1
                        r = 0
                    print(str(width) + " " + str(height) + " " + str(x) + " " + str(y) + " " + str(r), file = f)

        except:
            print("Could not save data to file " + file_name)

    def save_data_as_png(self, file_name, best, data_for_ga):
        plt_gca = plt.gca()
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.ylim(-100, BIG_BOARD_HEIGHT + 100)
        plt.xlim(-100, BIG_BOARD_WIDTH + 100)
        plt_gca.invert_yaxis()
        big_board = patches.Rectangle((0, 0), BIG_BOARD_WIDTH - 1, BIG_BOARD_HEIGHT - 1, linewidth = 1, edgecolor = 'black', facecolor = 'none')
        plt_gca.add_patch(big_board)
        solution = best[1]

        for idx, board in enumerate(solution):
            if board["e"] == 1:
                x = solution[idx]["x"]
                y = solution[idx]["y"]
                width = data_for_ga[idx]["width"]
                height = data_for_ga[idx]["height"]
                if board["r"] == 1:
                    width, height = height, width

                board = patches.Rectangle((x, y), width - 1, height - 1, linewidth = 1, edgecolor = 'red', facecolor = 'blue')
                plt_gca.add_patch(board)
        plt.savefig(file_name)