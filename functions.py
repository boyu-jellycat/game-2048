import copy

def initialize_game():
    grid = [[0]*4 for _ in range(4)]
    grid = add_random_two(grid)
    return grid

def add_random_two(grid):
    import random
    empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = 2
    return grid

def compress(grid):
    new_grid = []
    for row in grid:
        new_row = [num for num in row if num != 0]
        new_row += [0]*(4 - len(new_row))
        new_grid.append(new_row)
    return new_grid

def merge(grid):
    score = 0
    for i in range(4):
        for j in range(3):
            if grid[i][j] == grid[i][j+1] and grid[i][j] != 0:
                grid[i][j] *= 2
                grid[i][j+1] = 0
                score += grid[i][j]
    return grid, score

def reverse(grid):
    new_grid = []
    for row in grid:
        new_grid.append(row[::-1])
    return new_grid

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def move_left(grid):
    try:
        grid = compress(grid)
        grid, score = merge(grid)
        grid = compress(grid)
        return grid, score
    except Exception as e:
        raise e

def move_right(grid):
    try:
        grid = reverse(grid)
        grid, score = move_left(grid)
        grid = reverse(grid)
        return grid, score
    except Exception as e:
        raise e

def move_up(grid):
    try:
        grid = transpose(grid)
        grid, score = move_left(grid)
        grid = transpose(grid)
        return grid, score
    except Exception as e:
        raise e

def move_down(grid):
    try:
        grid = transpose(grid)
        grid, score = move_right(grid)
        grid = transpose(grid)
        return grid, score
    except Exception as e:
        raise e

def check_game_over(grid):
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return False
            if j < 3 and grid[i][j] == grid[i][j+1]:
                return False
            if i < 3 and grid[i][j] == grid[i+1][j]:
                return False
    return True
