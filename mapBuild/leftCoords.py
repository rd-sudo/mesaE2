# List of coordinates with arrows pointing to the left
left_coords = [
    # LONG STREET row 23 and 22 crosses the MAP ////////////// TURN 1
    # Left lane p1
    *[(x, 23) for x in range(1, 24)],
    # Right lane p1
    *[(x, 22) for x in range(1, 23)],
    # Short street row 18 and 17 red light//////////////// TURN 2
    (8, 18),
    (9, 18),
    (10, 18),
    (11, 18),
    (12, 18),
    (8, 17),
    (9, 17),
    (10, 17),
    (11, 17),
    (12, 17),
    # Short street row 5 and 4 red light////////////////// TURN 5
    (2, 5),
    (3, 5),
    (4, 5),
    (5, 5),
    (6, 5),
    (2, 4),
    (3, 4),
    (4, 4),
    (5, 4),
    (6, 4),
    # LONG STREET row 11 and 10 crosses the MAP////////////// TURN 4
    # Left lane
    *[(x, 11) for x in range(1, 23)],
    # Right lane part 1
    *[(x, 10) for x in range(1, 13)],
    # Right lane part 2
    *[(x, 10) for x in range(16, 23)],
    # Short street row 17 and 16///////////////////////////// TURN 3
    # Left lane
    *[(x, 17) for x in range(15, 23)],
    # Right lane
    *[(x, 16) for x in range(15, 23)],
    # Parking spots
    # Parking spot 1
    (2, 14),
    # Parking spot 6
    (6, 17),
    # Parking spot 7
    (8, 15),
    # Parking spot 13
    (18, 6),
    # Parking spot 14
    (18, 4),
    # Parking spot 17
    (20, 4),
]
