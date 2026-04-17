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
    height = len(terrain[0]) if width else 0
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            cur = terrain[i][j]
            d1 = abs(cur - terrain[i-1][j])
            d2 = abs(cur - terrain[i+1][j])
            d3 = abs(cur - terrain[i][j-1])
            d4 = abs(cur - terrain[i][j+1])
            if max(d1, d2, d3, d4) > threshold:
                artifacts.append((i, j))
    return artifacts
def run_edge_tests():
    print("--- Exercise 3 Edge Cases Test ---\n")

    print("Test 1: roughness = 0 → terrain should be flat")
    t1 = generate_terrain(16, 16, 0, 3)
    a1 = detect_artifacts(t1, 0.1)
    print(f"Artifacts found: {len(a1)} (should be 0)\n")

    print("Test 2: depth = 0 → no recursion, flat terrain")
    t2 = generate_terrain(16, 16, 5, 0)
    a2 = detect_artifacts(t2, 0.01)
    print(f"Artifacts found: {len(a2)} (should be 0)\n")

    print("Test 3: high roughness → many artifacts")
    t3 = generate_terrain(16, 16, 10, 4)
    a3 = detect_artifacts(t3, 2.0)
    print(f"Artifacts found: {len(a3)} (should be > 0)\n")

    print("Test 4: midpoint displacement line")
    line = midpoint_displacement(0, 0, 100, 0, 5, 5)
    line.append((100, 0))
    print(f"Generated points count: {len(line)}\n")

if __name__ == "__main__":
    run_edge_tests()
