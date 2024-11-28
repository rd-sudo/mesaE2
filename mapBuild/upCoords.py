# List of coordinates with arrows pointing up
up_coords = [
    # SHORT STREET row 6 ////////////// ROUTE 1
    # Left lane
    *[(6, y) for y in range(11, 22)],
    # Right lane
    *[(7, y) for y in range(11, 22)],
    # LONG STREET row 14 crosses the MAP ////////////// ROUTE 2 **roundabout, lane change
    # Left lane p1
    *[(14, y) for y in range(1, 8)],
    # Left lane p2
    *[(14, y) for y in range(11, 22)],
    # Right lane
    *[(15, y) for y in range(1, 22)],
    # SHORT STREET row 18//////////////////////////////////////
    # Left lane
    *[(18, y) for y in range(1, 8)],
    # Right lane
    *[(19, y) for y in range(1, 8)],
    # LONG STREET row 22//////////////////////////////////////
    # Left lane
    *[(22, y) for y in range(1, 22)],
    # Right lane
    *[(23, y) for y in range(0, 23)],
    # Parking spots
    # Parking spot 2
    (3, 21),
    # Parking spot 3
    (3, 5),
    # Parking spot 4
    (4, 11),
    # Parking spot 5
    (4, 3),
    # Parking spot 8
    (9, 1),
    # Parking spot 9
    (10, 18),
    # Parking spot 10
    (10, 11),
    # Parking spot 11
    (10, 7),
    # Parking spot 12
    (17, 21),
    # Parking spot 15
    (20, 17),
    # Parking spot 16
    (20, 15),
]
