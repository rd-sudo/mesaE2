down_left_coords = [
    # HORIZONTAL LINES
    # Top Lane
    *[(x, 23) for x in range(2, 23)],
    # Near Parking 9
    *[(x, 18) for x in range(9, 12)],
    # Near Parking 15
    *[(x, 17) for x in range(17, 22)],
    # Near Parkings 4 and 10
    *[(x, 11) for x in range(3, 13)],
    # Near Parking 16
    *[(x, 11) for x in range(16, 22)],
    # Near Parking 3
    *[(x, 5) for x in range(3, 6)],
    # VERTICAL LINES
    # lEFT lANE
    *[(1, y) for y in range(1, 22)],
    # Column 7
    *[(7, y) for y in range(3, 8)],
    # Colyumn 13
    *[(13, y) for y in range(12, 22)],
    *[(13, y) for y in range(3, 8)],
]
