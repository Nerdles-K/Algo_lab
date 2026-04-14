def split_region(x, y, width, height, min_size, regions=None):
    if regions is None:
        regions = []
        
    if width <= min_size or height <= min_size:
        regions.append((x, y, width, height))
        return regions
        
    mid_w = width / 2.0
    mid_h = height / 2.0
    
    split_region(x, y, mid_w, mid_h, min_size, regions)
    split_region(x + mid_w, y, mid_w, mid_h, min_size, regions)
    split_region(x, y + mid_h, mid_w, mid_h, min_size, regions)
    split_region(x + mid_w, y + mid_h, mid_w, mid_h, min_size, regions)
    
    return regions


def count_points_in_region(points, region):

    x, y, width, height = region
    count = 0
    for px, py in points:
        if x <= px < x + width and y <= py < y + height:
            count += 1
    return count


def find_dense_regions(points, x, y, width, height, min_size, threshold, dense_regions=None):
    if dense_regions is None:
        dense_regions = []
        
    region = (x, y, width, height)
    count = count_points_in_region(points, region)
    
    if count == 0:
        return dense_regions
        
    if width <= min_size or height <= min_size:
        if count > threshold:
            dense_regions.append((region, count))
        return dense_regions
        
    mid_w = width / 2.0
    mid_h = height / 2.0
    
    find_dense_regions(points, x, y, mid_w, mid_h, min_size, threshold, dense_regions)
    find_dense_regions(points, x + mid_w, y, mid_w, mid_h, min_size, threshold, dense_regions)
    find_dense_regions(points, x, y + mid_h, mid_w, mid_h, min_size, threshold, dense_regions)
    find_dense_regions(points, x + mid_w, y + mid_h, mid_w, mid_h, min_size, threshold, dense_regions)
    
    return dense_regions

def run_edge_tests():
    print("--- (Edge Cases Test) ---\n")
    
    space = (0, 0, 100, 100) # x, y, width, height
    min_size = 10
    
    clustered_points = [(1, 1), (2, 2), (1, 2), (2, 1), (0.5, 0.5)]
    threshold = 2
    print("Test 1: Points clustered in a small area")
    res1 = find_dense_regions(clustered_points, *space, min_size, threshold)
    print(f"Area that meet the density threshold: {len(res1)}")
    print(f"precisely: {res1}\n")
    
    empty_points = []
    print("Test 2: Empty space (empty array of points)")
    res2 = find_dense_regions(empty_points, *space, min_size, threshold=0)
    print(f"Area that meet the density threshold: {len(res2)}")
    print(f"precisely: {res2}\n")
    
    normal_points = [(50, 50), (60, 60), (55, 55)]
    giant_min_size = 200
    print("Test 3: min_size larger than the initial space")
    res3 = find_dense_regions(normal_points, *space, giant_min_size, threshold=1)
    print(f"Area that meet the density threshold: {len(res3)}")
    print(f"precisely: {res3}\n")
    
    out_of_bounds_points = [(-10, -10), (150, 150), (200, -50)]
    print("Test 4: All points are outside the defined main space")
    res4 = find_dense_regions(out_of_bounds_points, *space, min_size, threshold=0)
    print(f"Area that meet the density threshold: {len(res4)}")
    print(f"precisely: {res4}\n")

if __name__ == "__main__":
    run_edge_tests()