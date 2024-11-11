import pygame
import random
import math

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables
house_x = 170
house_width = 250
cloud_x = 100
cloud_y = 110
cloud_z = 120
ground_height = 100
house_height = 180
house_y = HEIGHT - ground_height - house_height
tree_sway_angle = 0  # Variable to control the sway of the trees
tree_sway_speed = 0.05  # Controls how fast the trees sway
smoke_puffs = []  # List to store smoke puffs
smoke_interval = 0  # To control how often new smoke puffs appear
# ---------------------------

def create_smoke(chimney_x, chimney_y):
    """Generate a new puff of smoke."""
    puff = {
        'x': chimney_x,
        'y': chimney_y,
        'radius': random.randint(10, 20),
        'alpha': 255,  # Full opacity
        'speed': random.uniform(1, 2),  # Speed of upward movement
        'drift': random.uniform(-1, 1)  # Drift of the smoke puff
    }
    smoke_puffs.append(puff)

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

    # GAME STATE UPDATES
    cloud_x += 7
    if cloud_x > WIDTH + 40:
        cloud_x = -100

    cloud_y += 5
    if cloud_y > WIDTH + 40:
        cloud_y = -100
    
    cloud_z += 3
    if cloud_z > WIDTH + 40:
        cloud_z = -100

    # Update the sway angle for the trees (create oscillating movement)
    tree_sway_angle += tree_sway_speed
    if tree_sway_angle > 2 * math.pi:  # Keep the angle within a full circle (0 to 2π)
        tree_sway_angle -= 2 * math.pi

    # Manage smoke puff generation
    smoke_interval += 1
    if smoke_interval > 10:  # Create a puff every 10 frames
        smoke_interval = 0
        chimney_x = house_x + house_width / 2  # Chimney's X position (center of the house)
        chimney_y = house_y - 40  # Chimney's Y position (just above the house)
        create_smoke(chimney_x, chimney_y)

    # Move and fade smoke puffs
    for puff in smoke_puffs[:]:
        puff['y'] -= puff['speed']  # Move puff upward
        puff['x'] += puff['drift']  # Slightly drift left or right
        puff['alpha'] -= 2  # Fade out (decrease alpha)
        if puff['alpha'] <= 0:
            smoke_puffs.remove(puff)  # Remove puff when fully transparent

    # DRAWING
    screen.fill((135, 206, 235))  # Sky color

    # Draw the mountains in the background (touching the grass)
    pygame.draw.polygon(screen, (169, 169, 169), [(0, HEIGHT - ground_height), (150, 150), (300, HEIGHT - ground_height)])  # Left mountain
    pygame.draw.polygon(screen, (169, 169, 169), [(200, HEIGHT - ground_height), (450, 50), (600, HEIGHT - ground_height)])  # Right mountain
    pygame.draw.polygon(screen, (105, 105, 105), [(0, HEIGHT - ground_height), (100, 120), (200, HEIGHT - ground_height)])  # Middle mountain
    pygame.draw.polygon(screen, (105, 105, 105), [(300, HEIGHT - ground_height), (450, 30), (600, HEIGHT - ground_height)])  # Distant right mountain

    # Draw the grass (ground)
    pygame.draw.rect(screen, (0, 200, 0), (0, HEIGHT - ground_height, WIDTH, ground_height))

    # Draw clouds
    pygame.draw.circle(screen, (255, 255, 255), (cloud_x, 100), 40)
    pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 34, 80), 40)
    pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 45, 100), 40)

    pygame.draw.circle(screen, (255, 255, 255), (cloud_y + 100, 100), 40)
    pygame.draw.circle(screen, (255, 255, 255), (cloud_y + 134, 80), 40)
    pygame.draw.circle(screen, (255, 255, 255), (cloud_y + 145, 100), 40)

    pygame.draw.circle(screen, (255, 255, 255), (cloud_z + 100, 100), 40)
    pygame.draw.circle(screen, (255, 255, 255), (cloud_z + 140, 87), 40)
    pygame.draw.circle(screen, (255, 255, 255), (cloud_z + 150, 105), 40)

    # Draw the house
    house_width = 250
    house_height = 180
    house_x = 170
    house_y = HEIGHT - ground_height - house_height  # House is placed right at the bottom of the screen

    # House body (rectangle)
    pygame.draw.rect(screen, (255, 223, 186), (house_x, house_y, house_width, house_height))  # Light tan color for walls

    # Roof (gable style with a triangle and ridge line)
    roof_points = [
        (house_x - 30, house_y),  # Left corner
        (house_x + house_width + 30, house_y),  # Right corner
        (house_x + house_width / 2, house_y - 80)  # Top point of the roof
    ]
    pygame.draw.polygon(screen, (139, 69, 19), roof_points)  # Dark brown roof

    # Chimney (rectangle on the roof)
    chimney_width = 40
    chimney_height = 60
    pygame.draw.rect(screen, (200, 200, 200), (house_x + house_width / 2 - chimney_width / 2, house_y - chimney_height - 40, chimney_width, chimney_height))  # Gray chimney

    # Draw smoke puffs
    for puff in smoke_puffs:
        pygame.draw.circle(screen, (175, 175, 175), (int(puff['x']), int(puff['y'])), puff['radius'], width=0)
        # Use 'width=0' to fill the circle completely with the alpha transparency.

    # Door (rectangle)
    door_width = 60
    door_height = 100
    pygame.draw.rect(screen, (0, 0, 0), (house_x + house_width / 2 - door_width / 2, house_y + house_height - door_height, door_width, door_height))  # Black door

    # Doorknob (circle)
    pygame.draw.circle(screen, (255, 223, 0), (house_x + house_width / 2 + 15, house_y + house_height - door_height + 30), 8)  # Yellow doorknob

    # Windows (rectangles with window panes)
    window_size = 40
    # Left window
    pygame.draw.rect(screen, (0, 191, 255), (house_x + 40, house_y + 40, window_size, window_size))  # Light blue window
    pygame.draw.line(screen, (0, 0, 0), (house_x + 40 + window_size / 2, house_y + 40), (house_x + 40 + window_size / 2, house_y + 40 + window_size), 3)  # Vertical line
    pygame.draw.line(screen, (0, 0, 0), (house_x + 40, house_y + 40 + window_size / 2), (house_x + 40 + window_size, house_y + 40 + window_size / 2), 3)  # Horizontal line

    # Right window (fixed alignment)
    right_window_x = house_x + house_width - 40 - window_size  # Adjusted position
    pygame.draw.rect(screen, (0, 191, 255), (right_window_x, house_y + 40, window_size, window_size))  # Light blue window
    # Vertical divider for the right window
    pygame.draw.line(screen, (0, 0, 0), (right_window_x + window_size / 2, house_y + 40), 
                     (right_window_x + window_size / 2, house_y + 40 + window_size), 3)  # Vertical line
    # Horizontal divider for the right window
    pygame.draw.line(screen, (0, 0, 0), (right_window_x, house_y + 40 + window_size / 2), 
                     (right_window_x + window_size, house_y + 40 + window_size / 2), 3)  # Horizontal line

    # Trees beside the house (adjusted to be farther from the house and touching the grass)
    # Left tree (positioned farther from the house and touching the grass)
    tree_trunk_x = house_x - 100  # Move tree farther left from the house
    tree_trunk_y = HEIGHT - ground_height - 60  # Place tree trunk directly on the grass
    pygame.draw.rect(screen, (139, 69, 19), (tree_trunk_x, tree_trunk_y, 20, 60))  # Tree trunk
    # Tree leaves sway left-right based on sine wave
    tree_leaves_x_offset = math.sin(tree_sway_angle) * 15  # Maximum sway of 15 pixels
    pygame.draw.circle(screen, (34, 139, 34), (tree_trunk_x + 10 + tree_leaves_x_offset, tree_trunk_y - 20), 40)  # Tree leaves

    # Right tree (positioned farther from the house and touching the grass)
    tree_trunk_x = house_x + house_width + 40  # Move tree farther right from the house
    pygame.draw.rect(screen, (139, 69, 19), (tree_trunk_x, tree_trunk_y, 20, 60))  # Tree trunk
    # Tree leaves sway left-right based on sine wave
    tree_leaves_x_offset = math.sin(tree_sway_angle + math.pi) * 15  # Maximum sway of 15 pixels (phase shift for opposite movement)
    pygame.draw.circle(screen, (34, 139, 34), (tree_trunk_x + 10 + tree_leaves_x_offset, tree_trunk_y - 20), 40)  # Tree leaves

    # Must be the last two lines
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

