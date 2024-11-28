monitoring_coords = {
    1: {
        "pos": (1, 9),
        "area": [*[(x, 9) for x in range(2, 12)], *[(x, 8) for x in range(2, 12)]],
        "direction": "right",
        "posible_destinations": [11, 3, 5, 8],
    },
    2: {
        "pos": (1, 8),
        "area": [*[(x, 9) for x in range(2, 12)], *[(x, 8) for x in range(2, 12)]],
        "direction": "right",
        "posible_destinations": [11, 3, 5, 8],
    },
    3: {
        "pos": (6, 12),
        "area": [*[(6, y) for y in range(12, 22)], *[(7, y) for y in range(12, 22)]],
        "direction": "up",
        "posible_destinations": [7, 6, 2],
    },
    4: {
        "pos": (7, 12),
        "area": [*[(6, y) for y in range(12, 22)], *[(7, y) for y in range(12, 22)]],
        "direction": "up",
        "posible_destinations": [7, 6, 2],
    },
    5: {
        "pos": (6, 8),
        "area": [*[(6, y) for y in range(2, 7)], *[(7, y) for y in range(2, 7)]],
        "direction": "down",
        "posible_destinations": [3, 5, 8],
    },
    6: {
        "pos": (7, 8),
        "area": [*[(6, y) for y in range(2, 7)], *[(7, y) for y in range(2, 7)]],
        "direction": "down",
        "posible_destinations": [3, 5, 8],
    },
    7: {
        "pos": (6, 5),
        "area": [*[(x, 5) for x in range(2, 6)], *[(x, 4) for x in range(2, 6)]],
        "direction": "left",
        "posible_destinations": [3, 5],
    },
    8: {
        "pos": (6, 4),
        "area": [*[(x, 5) for x in range(2, 6)], *[(x, 4) for x in range(2, 6)]],
        "direction": "left",
        "posible_destinations": [3, 5],
    },
    9: {
        "pos": (7, 5),
        "area": [*[(x, 5) for x in range(8, 12)], *[(x, 4) for x in range(8, 12)]],
        "direction": "right",
        "posible_destinations": [14, 17, 13],
    },
    10: {
        "pos": (7, 4),
        "area": [*[(x, 5) for x in range(8, 12)], *[(x, 4) for x in range(8, 12)]],
        "direction": "right",
        "posible_destinations": [14, 17, 13],
    },
    11: {
        "pos": (12, 22),
        "area": [*[(12, y) for y in range(12, 22)], *[(13, y) for y in range(12, 22)]],
        "direction": "down",
        "posible_destinations": [9],
    },
    12: {
        "pos": (13, 22),
        "area": [*[(12, y) for y in range(12, 22)], *[(13, y) for y in range(12, 22)]],
        "direction": "down",
    },
    13: {
        "pos": (12, 18),
        "area": [*[(x, 17) for x in range(8, 12)], *[(x, 18) for x in range(8, 12)]],
        "direction": "left",
    },
    14: {
        "pos": (12, 17),
        "area": [*[(x, 17) for x in range(8, 12)], *[(x, 18) for x in range(8, 12)]],
        "direction": "left",
    },
    15: {
        "pos": (12, 11),
        "area": [*[(x, 11) for x in range(2, 12)], *[(x, 10) for x in range(2, 12)]],
        "direction": "left",
    },
    16: {
        "pos": (12, 10),
        "area": [*[(x, 11) for x in range(2, 12)], *[(x, 10) for x in range(2, 12)]],
        "direction": "right",
    },
    17: {
        "pos": (12, 8),
        "area": [*[(12, y) for y in range(0, 8)], *[(13, y) for y in range(0, 8)]],
        "direction": "down",
    },
    18: {
        "pos": (12, 9),
        "area": [*[(12, y) for y in range(0, 8)], *[(13, y) for y in range(0, 8)]],
        "direction": "down",
    },
    19: {
        "pos": (14, 11),
        "area": [*[(14, y) for y in range(12, 22)], *[(15, y) for y in range(12, 22)]],
        "direction": "up",
    },
    20: {
        "pos": (15, 11),
        "area": [*[(14, y) for y in range(12, 22)], *[(15, y) for y in range(12, 22)]],
        "direction": "up",
    },
    21: {
        "pos": (15, 9),
        "area": [*[(x, 9) for x in range(16, 22)], *[(x, 8) for x in range(16, 22)]],
        "direction": "right",
    },
    22: {
        "pos": (15, 8),
        "area": [*[(x, 9) for x in range(16, 22)], *[(x, 8) for x in range(16, 22)]],
        "direction": "right",
    },
    23: {
        "pos": (14, 1),
        "area": [*[(14, y) for y in range(2, 8)], *[(15, y) for y in range(2, 8)]],
        "direction": "up",
    },
    24: {
        "pos": (15, 1),
        "area": [*[(14, y) for y in range(2, 8)], *[(15, y) for y in range(2, 8)]],
        "direction": "up",
    },
    25: {
        "pos": (18, 1),
        "area": [*[(18, y) for y in range(2, 8)], *[(19, y) for y in range(2, 8)]],
        "direction": "up",
    },
    26: {
        "pos": (19, 1),
        "area": [*[(18, y) for y in range(2, 8)], *[(19, y) for y in range(2, 8)]],
        "direction": "up",
    },
    27: {
        "pos": (22, 1),
        "area": [*[(x, 17) for x in range(16, 22)], *[(x, 16) for x in range(16, 22)]],
        "direction": "right",
    },
    28: {
        "pos": (23, 1),
        "area": [*[(x, 17) for x in range(16, 22)], *[(x, 16) for x in range(16, 22)]],
        "direction": "right",
    },
    29: {
        "pos": (22, 1),
        "area": [*[(x, 17) for x in range(16, 22)], *[(x, 16) for x in range(16, 22)]],
        "direction": "right",
    },
    30: {
        "pos": (22, 10),
        "area": [*[(x, 17) for x in range(16, 22)], *[(x, 16) for x in range(16, 22)]],
        "direction": "right",
    },
}
