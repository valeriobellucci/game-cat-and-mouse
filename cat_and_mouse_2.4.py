#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 12:30:34 2023

@author: valerio.b

A simple labyrint game
You are the red cat, catch the blue mouse that is hiding in the maze.

"""

# Install Pygame package - uncomment if needed
# !pip install pygame

#%%
import pygame
import random

# Initialize Pygame
pygame.init()
test_state = False # test state True makes for an easy win

# Set the screen dimensions
screen_width = 800
screen_height = 600
screen_rect = pygame.Rect(0, 0, screen_width, screen_height)
buffer = pygame.Surface((screen_width, screen_height)) ## Create a buffer surface

# Set the player dimensions
player_width = 10
player_height = 10

# Set the player speed
player_speed = 1/2

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cat and Mouse")

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# sets the grid step size
grid_step = 25
lab_start = 50 # start x of the labyrinth

# Set the player's initial position
player_x = 20
player_y = screen_height // 2 - player_height // 2

# Set the mouse size and initial position
mouse_size = 10
mouse_speed = 20 # seconds
mouse_x = screen_width - grid_step * random.randint(1,10)
mouse_y = screen_height - grid_step * random.randint(1,10)
if test_state is True:
    mouse_x = 0
    mouse_y = screen_height // 3
    
# Defines start positions for resetting the game
start_conditions = (player_x, player_y, mouse_x, mouse_y)

# Difficulty constants
EASY = "easy"
NORMAL = "normal"
DIFFICULT = "difficult"

# Set initial difficulty
difficulty = EASY
mouse_speeds = {EASY: 30, NORMAL: 20, DIFFICULT: 10}

# Track time for mouse position update
start_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
refresh_rate = 200 # Limit the frame rate to 100 FPS (10 milliseconds per frame)
time_elapsed = 0
mouse_update_interval = mouse_speed * 1000  # mouse speed in milliseconds

# Set the obstacle's generator position and dimensions
obstacle_x = lab_start
obstacle_y = screen_height // 2 - 50
obstacle_width = 2
obstacle_height = grid_step

# Make the labyrinth
def make_maze():
    obstacles = []
    for i in range(30):
        x = obstacle_x + i * obstacle_height
        for j in range(30):
            y = screen_height // 2 + obstacle_height * random.randint(-12, 12)
            if random.randint(0, 1) : 
                width = obstacle_width
                height = obstacle_height
            else : 
                height= obstacle_width
                width = obstacle_height
            new_obstacle = pygame.Rect(x, y, width, height)
            obstacles.append(new_obstacle)
    return obstacles
#obstacles = make_maze()


# Game states
starting_state = "starting"
initialize_state = "initialize"
playing_state = "playing"
winning_state = "winning"
restart_state = "restart"
game_state = starting_state # initial state

# Start screen buttons
# Define button dimensions and position
button_width = 150
button_height = 50
button_spacing = 50
button_x = (screen_width - (button_width * 3 + button_spacing * 2)) // 2
button_y = (screen_height - button_height) * 3 // 4
# Define button rectangles
button_rect_easy = pygame.Rect(button_x, button_y, button_width, button_height)
button_rect_normal = pygame.Rect(button_x + button_width + button_spacing, button_y, button_width, button_height)
button_rect_difficult = pygame.Rect(button_x + (button_width + button_spacing) * 2, button_y, button_width, button_height)
button_rect_quit = pygame.Rect(button_x + button_width + button_spacing, button_y + 1.75 * button_height, button_width, button_height)

# Playing screen buttons
# Define button rectangle for going back to start state
button_rect_back = pygame.Rect(0, 0, 50, 25)

# Winning screen buttons
button_width = 300
button_height = 60
button_x = screen_width // 2 - button_width // 2
button_y = screen_height * 3 // 4
button_restart_rect = pygame.Rect(button_x, button_y - button_height // 2, button_width, button_height)
button_quit_rect = pygame.Rect(button_x, button_y + button_height, button_width, button_height)


# handles the events
def handle_events(running, game_state, button_rect_easy, button_rect_normal
                  , button_rect_difficult, button_rect_quit
                  , button_restart_rect, button_quit_rect
                  , button_rect_back, mouse_update_interval):
    for event in pygame.event.get():
        # QUIT window event
        if event.type == pygame.QUIT:
            running = False
        
        # KEYDOWN events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # exit fullscreen
                pygame.display.set_mode((screen_width, screen_height))
            if event.key == pygame.K_f: # fill-screen
                pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        
        # MOUSEBUTTONDOWN envents
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # START page (menu)
            if game_state == starting_state:
                if button_rect_easy.collidepoint(mouse_pos) or button_rect_normal.collidepoint(mouse_pos) or button_rect_difficult.collidepoint(mouse_pos):
                    if button_rect_easy.collidepoint(mouse_pos):
                        mouse_speed = mouse_speeds["easy"]
                    elif button_rect_normal.collidepoint(mouse_pos):
                        mouse_speed = mouse_speeds["normal"]
                    elif button_rect_difficult.collidepoint(mouse_pos):
                        mouse_speed = mouse_speeds["difficult"]
                    game_state = initialize_state
                    mouse_update_interval = mouse_speed * 1000  # Update the update_interval based on the new mouse_speed
                elif button_rect_quit.collidepoint(mouse_pos):
                    # Quit the game
                    running = False
            
            # WIN page
            elif game_state == winning_state:
                # Check collision with winning screen buttons
                if button_restart_rect.collidepoint(mouse_pos):
                    # Restart the game
                    game_state = restart_state
                elif button_quit_rect.collidepoint(mouse_pos):
                    # Quit the game
                    running = False

            # PLAYING page
            elif game_state == playing_state:
                # Check collision with playing screen buttons
                if button_rect_back.collidepoint(mouse_pos):
                    # Back to start page
                    game_state = starting_state
    
    return running, game_state, mouse_update_interval

# Winning page
def handle_winning_state():
    # Clear the screen
    screen.fill(black)
    
    # Display "YOU WIN" message
    font = pygame.font.Font(None, 150)
    text = font.render("YOU WIN", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 3))
    screen.blit(text, text_rect)

    # Draw the restart button
    font = pygame.font.Font(None, 70)
    pygame.draw.rect(screen, white, button_restart_rect)
    restart_text = font.render("RESTART", True, black)
    restart_text_rect = restart_text.get_rect(center=button_restart_rect.center)
    screen.blit(restart_text, restart_text_rect)
    
    # Draw the quit button
    pygame.draw.rect(screen, white, button_quit_rect)
    quit_text = font.render("QUIT", True, black)
    quit_text_rect = quit_text.get_rect(center=button_quit_rect.center)
    screen.blit(quit_text, quit_text_rect)
    
    # Update the display
    pygame.display.flip()

# restart handling
def handle_restart_state():
    game_state = starting_state
    return game_state

# Start page
def handle_starting_state():
    # Clear the screen
    screen.fill(black)

    # Display introduction message
    font = pygame.font.Font(None, 100)
    text = font.render("Cat and Mouse", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 3.5))
    screen.blit(text, text_rect)

    # Display 2nd introduction message
    font = pygame.font.Font(None, 50)
    text = font.render("You are the red cat, catch the blue mouse", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2.5))
    screen.blit(text, text_rect)

    # Display 3nd introduction message
    font = pygame.font.Font(None, 50)
    text = font.render("choose difficulty", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 1.6))
    screen.blit(text, text_rect)

    # Display full-screen message
    font = pygame.font.Font(None, 30)
    text = font.render("press F for fullscreen", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height - 20))
    screen.blit(text, text_rect)

    # Display difficulty buttons
    font = pygame.font.Font(None, 40)
    text_easy = font.render("EASY", True, black)
    text_normal = font.render("NORMAL", True, black)
    text_difficult = font.render("DIFFICULT", True, black)

    pygame.draw.rect(screen, white, button_rect_easy)
    pygame.draw.rect(screen, white, button_rect_normal)
    pygame.draw.rect(screen, white, button_rect_difficult)

    text_rect_easy = text_easy.get_rect(center=button_rect_easy.center)
    text_rect_normal = text_normal.get_rect(center=button_rect_normal.center)
    text_rect_difficult = text_difficult.get_rect(center=button_rect_difficult.center)

    screen.blit(text_easy, text_rect_easy)
    screen.blit(text_normal, text_rect_normal)
    screen.blit(text_difficult, text_rect_difficult)
    
    # Draw the quit button
    pygame.draw.rect(screen, white, button_rect_quit)
    quit_text = font.render("QUIT", True, black)
    quit_text_rect = quit_text.get_rect(center=button_rect_quit.center)
    screen.blit(quit_text, quit_text_rect)

    # Update the display
    pygame.display.flip()
    
    
# Playing page and playing loop  
def handle_playing_state(game_state
                         , player_x, player_y, mouse_x, mouse_y
                         , start_time, button_rect_back, mouse_update_interval):

    #D efines the objects
    # Define player
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    # Define mouse
    mouse_rect = pygame.Rect(mouse_x, mouse_y, mouse_size, mouse_size)
    
    # Handles movement
    keys = pygame.key.get_pressed()
    # Update the player's position
    up, down, left, right = False, False, False, False
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
        up = True
    if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed
        down = True
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        left = True
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
        right = True

    # Check for collision with the obstacle
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            # Determine the collision side
            if player_y < obstacle.y:
                # Collision from above
                player_y -= 5
            elif player_y + player_rect.height > obstacle.y + obstacle.height:
                # Collision from below
                player_y += 5
            elif player_x < obstacle.x:
                # Collision from the left
                player_x -= 5
            elif player_x + player_rect.height > obstacle.x + obstacle.width:
                # Collision from the right
                player_x += 5
            break  # Exit the loop if there's any collision


    # Check for collision with the mouse
    if player_rect.colliderect(mouse_rect):
        game_state = winning_state

    # Update the mouse position every update_interval milliseconds
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    if elapsed_time >= mouse_update_interval:
        mouse_x = lab_start + random.randint(0, screen_width - lab_start - mouse_size)
        mouse_y = random.randint(0, screen_height - mouse_size)
        start_time = current_time

    # Draw objects on the screen
    # Clear the buffer
    buffer.fill((0, 0, 0))
    # Draw the external borders of the screen
    pygame.draw.rect(buffer, white, screen_rect, width=2)  # All
    # Draw the player
    pygame.draw.rect(buffer, red, player_rect)
    # Draw the mouse
    pygame.draw.rect(buffer, blue, mouse_rect)
    # Draw the obstacle
    for i in obstacles:
        pygame.draw.rect(buffer, white, i)
    # Draw the back button
    pygame.draw.rect(buffer, white, button_rect_back)
    font = pygame.font.Font(None, 25)
    text = font.render("Menu", True, black)
    text_rect = text.get_rect(center=button_rect_back.center)
    buffer.blit(text, text_rect)
    # Update the display with the buffer
    screen.blit(buffer, (0, 0))
    pygame.display.flip()
    
    return game_state, player_x, player_y, mouse_x, mouse_y, start_time


##############
# Game loop
running = True
while running:
    # Limit the frame rate to the refresh_rate
    clock.tick(refresh_rate) 
    
    # Handle events
    running, game_state, mouse_update_interval = handle_events(running
                                        , game_state, button_rect_easy
                                        , button_rect_normal, button_rect_difficult
                                        , button_rect_quit
                                        , button_restart_rect, button_quit_rect
                                        , button_rect_back, mouse_update_interval
                                        )
    if not running: # breaks the game loop after event handling
        break
                    
    # -- Game states and pages

    # handle game initialization
    if game_state == "initialize":    
        start_time = pygame.time.get_ticks()
        obstacles = make_maze()
        player_x, player_y, mouse_x, mouse_y = start_conditions
        game_state = "playing"
    
    # playing page
    if game_state == "playing":
        game_state, player_x, player_y, \
        mouse_x, mouse_y, start_time = handle_playing_state(
            game_state, player_x, player_y, mouse_x, mouse_y,
            start_time, button_rect_back, mouse_update_interval
        )
    
    # start page                                                                                      
    elif game_state == starting_state:
        handle_starting_state()
        
    # win page
    elif game_state == winning_state:
        handle_winning_state()

    # handle restart    
    elif game_state == restart_state:
        game_state = handle_restart_state()

# Quit the game
pygame.quit()
