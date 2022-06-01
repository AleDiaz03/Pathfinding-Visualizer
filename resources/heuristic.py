def h(p1, p2):
    # We are using Manhattan distance to calculate heuristic
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)