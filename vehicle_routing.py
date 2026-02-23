from collections import deque

def bfs_vehicle_route(grid, start, stop):
    """
    grid: 2D list (0=free, 1=obstacle)
    start: (row, col)
    stop: (row, col)
    Returns: path as list of (row, col) or None
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == stop:
            return path
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path+[(nr, nc)]))
    return None

def print_grid_with_path(grid, path):
    grid_disp = [row[:] for row in grid]
    for r, c in path:
        grid_disp[r][c] = '*'
    for row in grid_disp:
        print(' '.join(str(x) for x in row)) 