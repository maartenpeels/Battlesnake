import random


def avoid_my_body(my_body, possible_moves):
    remove = []

    for dir, loc in possible_moves.items():
        if loc in my_body:
            remove.append(dir)

    for dir in remove:
        del possible_moves[dir]

    return possible_moves


def avoid_walls(board_width, board_height, possible_moves):
    remove = []

    for dir, loc in possible_moves.items():
        if loc["x"] < 0 or loc["x"] >= board_width \
                or loc["y"] < 0 or loc["y"] >= board_height:
            remove.append(dir)

    for dir in remove:
        del possible_moves[dir]

    return possible_moves


def avoid_snakes(snakes, possible_moves):
    remove = []

    for snake in snakes:
        for dir, loc in possible_moves.items():
            if loc in snake["body"]:
                remove.append(dir)

    remove = set(remove)
    for dir in remove:
        del possible_moves[dir]

    return possible_moves


def get_target_close(foods, my_head):
    closest_food = None
    closest_dist = None
    for food in foods:
        dist = abs(my_head["x"] - food["x"]) + abs(my_head["y"] - food["y"])
        if closest_dist is None or dist < closest_dist:
            closest_dist = dist
            closest_food = food

    return closest_food


def move_target(target, my_head, possible_moves):
    dist_x = abs(my_head["x"] - target["x"])
    dist_y = abs(my_head["y"] - target["y"])

    for dir, loc in possible_moves.items():
        new_dist_x = abs(loc["x"] - target["x"])
        new_dist_y = abs(loc["y"] - target["y"])

        if new_dist_x < dist_x or new_dist_y < dist_y:
            return dir

    return random.choice(list(possible_moves.keys()))


def choose_move(data):
    my_head = data["you"]["head"]
    my_body = data["you"]["body"]
    board_width = data["board"]["width"]
    board_height = data["board"]["height"]
    foods = data["board"]["food"]
    snakes = data["board"]["snakes"]

    possible_moves = {
        "up": {
            "x": my_head["x"],
            "y": my_head["y"] + 1,
        },
        "down": {
            "x": my_head["x"],
            "y": my_head["y"] - 1,
        },
        "left": {
            "x": my_head["x"] - 1,
            "y": my_head["y"],
        },
        "right": {
            "x": my_head["x"] + 1,
            "y": my_head["y"],
        },
    }

    possible_moves = avoid_my_body(my_body, possible_moves)
    possible_moves = avoid_walls(board_width, board_height, possible_moves)
    possible_moves = avoid_snakes(snakes, possible_moves)

    target = get_target_close(foods, my_head)

    if len(possible_moves) > 0:
        if target:
            move = move_target(target, my_head, possible_moves)
        else:
            move = random.choice(list(possible_moves.keys()))
    else:
        move = "up"
        print("Dying..")

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
