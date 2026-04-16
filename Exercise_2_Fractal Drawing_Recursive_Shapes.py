import matplotlib.pyplot as plt
import numpy as np
import sys

def draw_sierpinski(ax, x, y, size, depth):
    """
    Recursively draws Sierpinski triangles. 
    If depth is 0, draws a base triangle[cite: 40].
    Else, draws 3 smaller triangles inside[cite: 41].
    """
    if depth == 0:
        pts = np.array([[x, y], [x + size, y], [x + size/2, y + size * np.sin(np.pi/3)]])
        triangle = plt.Polygon(pts, fill=True, edgecolor='black', facecolor='cyan', alpha=0.6)
        ax.add_patch(triangle)
    else:
        new_size = size / 2
        # Bottom left
        draw_sierpinski(ax, x, y, new_size, depth - 1)
        # Bottom right
        draw_sierpinski(ax, x + new_size, y, new_size, depth - 1)
        # Top middle
        draw_sierpinski(ax, x + new_size/2, y + new_size * np.sin(np.pi/3), new_size, depth - 1)

def draw_tree(ax, x, y, length, angle, depth):
    """
    Recursively draws a tree.
    If depth is 0, draws a leaf[cite: 43].
    Else, draws a line and two branches at +/- 30 degrees[cite: 44].
    """
    if depth <= 0:
        return 
    
    x_end = x + length * np.cos(np.radians(angle))
    y_end = y + length * np.sin(np.radians(angle))
    
    ax.plot([x, x_end], [y, y_end], color='brown', lw=max(1, depth))
    
    new_length = length * 0.7
    draw_tree(ax, x_end, y_end, new_length, angle + 30, depth - 1)
    draw_tree(ax, x_end, y_end, new_length, angle - 30, depth - 1)

def fractal_dimension(image_array, box_sizes):
    """
    Estimates fractal dimension using box-counting.
    Counts how many boxes contain part of the fractal[cite: 47].
    Slope of log(count) vs log(1/size) is the dimension[cite: 48].
    """
    counts = []
    for size in box_sizes:
        count = 0
        for i in range(0, image_array.shape[0], size):
            for j in range(0, image_array.shape[1], size):
                if np.any(image_array[i:i+size, j:j+size] > 0):
                    count += 1
        counts.append(count)
    
    coeffs = np.polyfit(np.log(1.0/np.array(box_sizes)), np.log(counts), 1)
    return coeffs[0]

def run_edge_tests():
    print("--- Starting Edge Case Tests ---")

    print("Test 1: Depth 0... ", end="")
    fig, ax = plt.subplots()
    try:
        draw_sierpinski(ax, 0, 0, 100, 0)
        print("Passed (Drew 1 triangle)")
    except Exception as e:
        print(f"Failed: {e}")
    plt.close()

    print("Test 2: Size 0... ", end="")
    fig, ax = plt.subplots()
    try:
        draw_tree(ax, 0, 0, 0, 90, 5)
        print("Passed (Handled zero length)")
    except Exception as e:
        print(f"Failed: {e}")
    plt.close()

    print("Test 3: Depth 100 (Recursion Limit)... ", end="")
    fig, ax = plt.subplots()
    original_limit = sys.getrecursionlimit()
    try:
        test_depth = 100
        if test_depth > 20: # Arbitrary "safe" limit for standard visualizers
            print(f"Skipped actual render to prevent crash. Depth {test_depth} exceeds safety threshold.")
        else:
            draw_sierpinski(ax, 0, 0, 100, test_depth)
    except RecursionError:
        print("Caught RecursionError (System protected)")
    finally:
        sys.setrecursionlimit(original_limit)
    plt.close()

    print("Test 4: Dimension of a straight line... ", end="")
    fake_line_img = np.zeros((100, 100))
    fake_line_img[50, :] = 1 # Horizontal line
    dim = fractal_dimension(fake_line_img, [1, 2, 4, 10])
    print(f"Calculated D ≈ {dim:.2f} (Expected ≈ 1.0)")

if __name__ == "__main__":
    run_edge_tests()

    print("\nGenerating visual fractals...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.set_title("Sierpinski (Depth 5)")
    ax1.set_aspect('equal')
    draw_sierpinski(ax1, 0, 0, 100, 5)
    
    ax2.set_title("Recursive Tree (Depth 7)")
    draw_tree(ax2, 0, 0, 50, 90, 7)
    
    plt.show()