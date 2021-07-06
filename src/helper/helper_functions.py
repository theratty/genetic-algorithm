BIG_BOARD_WIDTH = 2800
BIG_BOARD_HEIGHT = 2070
BIG_BOARD_FIELD = BIG_BOARD_WIDTH * BIG_BOARD_HEIGHT

def calc_two_rect_overlapsing_field(rect1, rect2):
    x_overlap = max(0, min(rect1[2], rect2[2]) - max(rect1[0], rect2[0]) + 1)
    y_overlap = max(0, min(rect1[3], rect2[3]) - max(rect1[1], rect2[1]) + 1)
    return x_overlap * y_overlap

def calc_full_overlapsing_sum(individual, data, power=1):
    sum_of_overlapsed_field = 0
    for first in range(len(individual)):
        if individual[first]["e"] == 0:
            continue

        first_x_1 = individual[first]["x"]
        first_y_1 = individual[first]["y"]
        if individual[first]["r"] == 0:
            first_x_2 = first_x_1 + data[first]["width"] - 1
            first_y_2 = first_y_1 + data[first]["height"] - 1
        else:
            first_x_2 = first_x_1 + data[first]["height"] - 1
            first_y_2 = first_y_1 + data[first]["width"] - 1

        rect1 = [first_x_1, first_y_1, first_x_2, first_y_2]

        for second in range(first + 1, len(individual)):
            if individual[second]["e"] == 0:
                continue
            
            second_x_1 = individual[second]["x"]
            second_y_1 = individual[second]["y"]
            if individual[second]["r"] == 0:
                second_x_2 = second_x_1 + data[second]["width"] - 1
                second_y_2 = second_y_1 + data[second]["height"] - 1
            else:
                second_x_2 = second_x_1 + data[second]["height"] - 1
                second_y_2 = second_y_1 + data[second]["width"] - 1

            rect2 = [second_x_1, second_y_1, second_x_2, second_y_2]    

            sum_of_overlapsed_field = sum_of_overlapsed_field + calc_two_rect_overlapsing_field(rect1, rect2)**power
        
    return sum_of_overlapsed_field

def check_if_elements_protrutes(individual, data, power=1):
    sum = 0

    rect1 = [0, 0, BIG_BOARD_WIDTH - 1, BIG_BOARD_HEIGHT - 1]

    for idx, el in enumerate(individual):
        if el["e"] == 0:
            continue

        x_1 = individual[idx]["x"]
        y_1 = individual[idx]["y"]
        if individual[idx]["r"] == 0:
            x_2 = x_1 + data[idx]["width"] - 1
            y_2 = y_1 + data[idx]["height"] - 1
        else:
            x_2 = x_1 + data[idx]["height"] - 1
            y_2 = y_1 + data[idx]["width"] - 1

        rect2 = [x_1, y_1, x_2, y_2]
        overlapsing_field = calc_two_rect_overlapsing_field(rect1, rect2)
        field_of_rectangle = data[idx]["width"] * data[idx]["height"]
        protruting = field_of_rectangle - overlapsing_field

        sum = sum + protruting**power

    return sum