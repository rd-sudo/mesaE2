down_right_coords = [
    # HORIZONTAL LINES
    *[(x, 9) for x in range(2, 12)],
    *[(x, 9) for x in range(16, 21)],
    # Near Parking 11
    *[(x, 5) for x in range(8, 11)],
    # Button line
    *[(x, 1) for x in range(1, 21)],
    # VERTICAL LINES
    # Right Lane
    *[(0, y) for y in range(1, 22)],
    # Near Parking 5
    *[(6, y) for y in range(3, 8)],
    # Lane 12
    *[(12, y) for y in range(3, 9)],
    *[(12, y) for y in range(13, 22)],
]
