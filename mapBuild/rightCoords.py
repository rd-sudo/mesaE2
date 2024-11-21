# List of coordinates with arrows pointing to the right
right_coords = [
    # LONG STREET row 23 and 22 crosses the MAP ////////////// TURN 1
    # Left lane p1
    *[(x, 1) for x in range(0, 23)],
    # Right lane p1
    *[(x, 0) for x in range(0, 23)],
    # SHORT STREET row 5 and 4 crosses the MAP ////////////// TURN 2
    # Left lane p1
    *[(x, 4) for x in range(7, 12)],
    # Right lane p2
    *[(x, 5) for x in range(7, 12)],
    # SHORT STREET row 8 and 9 crosses the MAP ////////////// TURN 3
    # Left lane p1
    *[(x, 9) for x in range(1, 12)],
    # Left lane p3
    *[(x, 9) for x in range(15, 22)],
    # Right lane p1
    *[(x, 8) for x in range(1, 22)],
    # Parking spots
    # Parking spot 1
    (1, 14),
    # Parking spot 6
    (5, 17),
    # Parking spot 7
    (7, 15),
    # Parking spot 13
    (17, 6),
    # Parking spot 14
    (17, 4),
    # Parking spot 17
    (19, 4),
]
