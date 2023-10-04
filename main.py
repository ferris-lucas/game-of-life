'''
Conway's Game of Life Simulation

Code Structure:
1. Initialize Pygame and set up the screen and constants.
2. Define auxiliary functions for drawing the grid, positions, and applying rules.
3. Define a function to generate random positions within the grid.
4. Define a function to count live neighbors for a given position.
5. Define a function to apply the rules of Conway's Game of Life.
6. Define the main function to run the simulation and handle user interactions.
7. Run the main function if this script is executed directly.

Rules:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

'''
import pygame
import random

#initializes pygame library for graphical operations
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1200 # the desired screen dimmension
TILE_SIZE = 5 # the desired size of each block in the grid (in pixels)
GRID_THICKNESS = 1
ROWS, COLS = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

# Colors
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Simulation Parameters
FPS = 60 # frame rate for simulation
UPDATE_FREQ = 2 # update rate for grid drawing
RANDOM_DENSITY = 0.5 # density of random positions in grid

# clock to control the frame rate
clock = pygame.time.Clock()

# pygame window, leave room for instructions window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_grid(screen):
    """
    Draw a grid on the Pygame screen.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        color (tuple): The color of the grid lines in RGB format.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        tile_size (int): The size of each grid tile in pixels.
        grid_thickness (int): The thickness of the grid lines.
    """
    for row in range(ROWS):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (SCREEN_WIDTH, row * TILE_SIZE), GRID_THICKNESS)
    for col in range(COLS):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, SCREEN_HEIGHT), GRID_THICKNESS)

def draw_positions(screen, grid_positions):
    """
    Draw the current live cells positions on the Pygame screen.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        grid_positions (set): A set of positions to be drawn.
        color (tuple): The color of the grid positions in RGB format.
        tile_size (int): The size of each grid tile in pixels.
    """
    for position in grid_positions:
        grid_x, grid_y = position
        pygame.draw.rect(screen, GREEN, (grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def generate_random_grid_positions():
    """
    Generate a set of random positions within the grid.

    Args:
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.

    Returns:
        set: A set of randomly generated positions within the grid.
    """
    random_grid_positions = set()
    for y in range(0, ROWS):
        for x in range(0, COLS):
            if random.random() < RANDOM_DENSITY:
                random_pos = (x, y)
                random_grid_positions.add(random_pos)
    return random_grid_positions

def generate_pattern():
    """
    Generate a set of positions in a pattern within the grid.
    """
    pattern_grid_positions = set()
    for y in range(0, ROWS):
        for x in range(0, COLS):
                if x == COLS // 2 or y == ROWS // 2: # cross pattern
                    pattern_grid_positions.add((x,y))
                if x == y or x == COLS - y: # x pattern
                    pattern_grid_positions.add((x,y))
                if ((ROWS - 10) // 2) ** 2 < (x - COLS // 2) ** 2 + (y - ROWS // 2) ** 2 < (ROWS // 2) ** 2: # circle pattern
                    pattern_grid_positions.add((x,y))
                if y == (ROWS // 2) - (x - COLS // 2) ** 2 // 100: # parabolic pattern
                    pattern_grid_positions.add((x,y))
                if y == (ROWS // 2) - (x - COLS // 2) ** 4 // 1000000: # forth grade equation pattern
                    pattern_grid_positions.add((x,y))
    return pattern_grid_positions

def count_live_neighbors(grid_positions, position):
    """
    Count the live neighbors of a given position in the grid.
    If the position is on the edge of the grid, wrap around to the other side.

    Args:
        grid_positions (set): A set of live positions in the grid.
        position (tuple): The position to count neighbors for.
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.

    Returns:
        int: The count of live neighbors for the given position.
    """
    x, y = position
    count_of_live_neighbors = 0

    # Define offsets for neighbors (we will check all surrounding cells)
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for offset_x, offset_y in offsets:
        neighbor_x = (x + offset_x) % COLS  # Wrap around for x
        neighbor_y = (y + offset_y) % ROWS  # Wrap around for y

        neighbor_pos = (neighbor_x, neighbor_y)
        if neighbor_pos in grid_positions:
            count_of_live_neighbors += 1

    return count_of_live_neighbors

def apply_rules(grid_positions):
    """
    Apply Conway's Game of Life rules to update the grid positions.

    Args:
        grid_positions (set): A set of live positions in the grid.
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.

    Returns:
        set: The updated set of live positions after applying the rules.
    """
    updated_grid_positions = set()
    for row in range(0, ROWS):
        for col in range(0, COLS):
            position = (row, col)
            count_of_live_neighbors = count_live_neighbors(grid_positions, position)
            
            # check the cases of living to the next generation, other cases are dead
            if (position in grid_positions and (count_of_live_neighbors == 2 or count_of_live_neighbors == 3)): #lives
                updated_grid_positions.add(position)
            elif count_of_live_neighbors == 3 and position not in grid_positions: #reproduction
                updated_grid_positions.add(position)

    return updated_grid_positions

def handle_event(event, grid_positions, count, playing, running, iteration):
    """
    Handle various events in the game.

    Args:
        event (pygame.event.Event): The event to handle.
        grid_positions (set): The set of live positions in the grid.
        count (int): The count variable for game logic.
        playing (bool): Flag indicating if the game is currently playing.
        running (bool): Flag indicating if the game is running.

    Returns:
        tuple: Updated grid positions, count, playing, and running flags.
    """
    # quit event -> exit the game
    if event.type == pygame.QUIT:
        running = False
    # keydown event -> pause, clear, randomize, or insert pattern the grid
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            playing = not playing
        elif event.key == pygame.K_c:
            grid_positions.clear()
            playing = False
            count = 0
            iteration = 0
        elif event.key == pygame.K_r:
            grid_positions = generate_random_grid_positions()
            iteration = 0
        elif event.key == pygame.K_p:
            grid_positions = generate_pattern()
            iteration = 0
            playing = False
    # mouse click event -> add or remove a position from the grid
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        grid_positions = handle_mouse_click(grid_positions)

    return grid_positions, count, playing, running, iteration

def handle_mouse_click(grid_positions):
    """
    Handle mouse clicks to add or remove grid positions.

    Args:
        grid_positions (set): The set of live positions in the grid.
        tile_size (int): The size of each grid tile in pixels.

    Returns:
        set: Updated grid positions after handling the mouse click.
    """
    mouse_pos = pygame.mouse.get_pos()
    grid_pos = (mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE)
    if grid_pos in grid_positions:
        grid_positions.remove(grid_pos)
    else:
        grid_positions.add(grid_pos)

    return grid_positions


def main():
    """
    Run the main loop for Conway's Game of Life.

    This function initializes the game and handles the main event loop.

    Returns:
        None
    """

    grid_positions = set()

    running = True
    playing = False
    count = 0 # keeps track of the number of frames passed since the last grid update
    iteration = 0 # keeps track of the number of iterations passed since the start of the simulation

    while running:
        clock.tick(FPS)
        
        pygame.display.set_caption(f"Conway's Game of Life Simulation - Playing - Iteration {iteration}" if playing else "Conway's Game of Life Simulation - Paused")

        if playing:
            count = count + 1
            iteration = iteration + 1
        
        if count >= UPDATE_FREQ:
            count = 0
            grid_positions =  apply_rules(grid_positions)

        for event in pygame.event.get():
            grid_positions, count, playing, running, iteration = handle_event(event, grid_positions, count, playing, running, iteration)

        screen.fill(GRAY)
        draw_grid(screen)
        draw_positions(screen, grid_positions)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
