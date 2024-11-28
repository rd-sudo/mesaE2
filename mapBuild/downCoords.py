# List of coordinates with arrows pointing down
down_coords = [
    # Path down in column 0 and 1////////////////////
    # Left lane
    *[(1, y) for y in range(1, 24)],
    # Right lane
    *[(0, y) for y in range(1, 24)],
    # Path down in column 6 and 7////////////////////
    # Right lane
    *[(6, y) for y in range(2, 9)],
    # Left lane
    *[(7, y) for y in range(2, 9)],
    # Path down in column 12 and 13////////////////////
    # Right lane
    *[(12, y) for y in range(2, 23)],
    # Left lane p1
    *[(13, y) for y in range(2, 9)],
    # Left lane p2
    *[(13, y) for y in range(12, 23)],
    # Parking spots
    # Parking spot 2
    (3, 22),
    # Parking spot 3
    (3, 6),
    # Parking spot 4
    (4, 12),
    # Parking spot 5
    (4, 4),
    # Parking spot 8
    (9, 2),
    # Parking spot 9
    (10, 19),
    # Parking spot 10
    (10, 12),
    # Parking spot 11
    (10, 8),
    # Parking spot 12
    (17, 22),
    # Parking spot 15
    (20, 18),
    # Parking spot 16
    (20, 16),
]
