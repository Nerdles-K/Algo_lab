import random

def midpoint_displacement(x1, y1, x2, y2, roughness, depth, points=None):
    if points is None:
        points = []

    if depth == 0:
        points.append((x1, y1))
        return points

    mid_x = (x1 + x2) / 2.0
    mid_y = (y1 + y2) / 2.0

    offset = roughness * random.uniform(-1, 1)
    mid_y += offset

    midpoint_displacement(x1, y1, mid_x, mid_y, roughness / 2, depth - 1, points)
    midpoint_displacement(mid_x, mid_y, x2, y2, roughness / 2, depth - 1, points)

    if x1 == 0 and y1 == 0:
        points.append((x2, y2))

    return points

def generate_terrain(width, height, roughness, depth):
    terrain = [[0.0 for _ in range(height)] for _ in range(width)]
    diamond_square(terrain, 0, 0, width - 1, height - 1, roughness, depth)
    return terrain

def diamond_square(terrain, x1, y1, x2, y2, roughness, depth):
    if depth == 0:
        return

    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2

    c1 = terrain[x1][y1]
    c2 = terrain[x2][y1]
    c3 = terrain[x1][y2]
    c4 = terrain[x2][y2]
    avg = (c1 + c2 + c3 + c4) / 4.0

    terrain[mid_x][mid_y] = avg + roughness * random.uniform(-1, 1)

    diamond_square(terrain, x1, y1, mid_x, mid_y, roughness / 2, depth - 1)
    diamond_square(terrain, mid_x, y1, x2, mid_y, roughness / 2, depth - 1)
    diamond_square(terrain, x1, mid_y, mid_x, y2, roughness / 2, depth - 1)
    diamond_square(terrain, mid_x, mid_y, x2, y2, roughness / 2, depth - 1)

def detect_artifacts(terrain, threshold):
    artifacts = []
    width = len(terrain)
    height = len(terrain[0]) if width > 0 else 0

    for i in range(1, width - 1):
        for j in range(1, height - 1):
            current = terrain[i][j]
            d1 = abs(current - terrain[i-1][j])
            d2 = abs(current - terrain[i+1][j])
            d3 = abs(current - terrain[i][j-1])
            d4 = abs(current - terrain[i][j+1])
            max_diff = max(d1, d2, d3, d4)
            if max_diff > threshold:
                artifacts.append((i, j))
    return artifacts

def run_edge_tests():
    print("--- Exercise 3 Edge Cases Test ---\n")

    print("Test 1: roughness = 0 → terrain should be flat")
    terrain1 = generate_terrain(16, 16, roughness=0, depth=3)
    artifacts1 = detect_artifacts(terrain1, threshold=0.1)
    print(f"Artifacts found: {len(artifacts1)} (should be 0)\n")

    print("Test 2: depth = 0 → no recursion, flat terrain")
    terrain2 = generate_terrain(16, 16, 5, depth=0)
    artifacts2 = detect_artifacts(terrain2, 0.01)
    print(f"Artifacts found: {len(artifacts2)} (should be 0)\n")

    print("Test 3: high roughness → many artifacts")
    terrain3 = generate_terrain(16, 16, 10, 4)
    artifacts3 = detect_artifacts(terrain3, 2.0)
    print(f"Artifacts found: {len(artifacts3)} (should be > 0)\n")

    print("Test 4: midpoint displacement line")
    line = midpoint_displacement(0, 0, 100, 0, 5, depth=5)
    print(f"Generated points count: {len(line)}\n")

if __name__ == "__main__":
    run_edge_tests()
