# import yara
# import os
#
# rule = yara.compile("open_for_c#.yar")
# matches = rule.match(r"example_for_yara.exe")
# for match in matches:
#     if match.rule == "txt_file_name_in_exe":
#         decoded_text = match.strings[0][2].decode('utf-16le')
#         print(decoded_text)
#         continue
#     print(match.strings)

import pygame
import random

pygame.init()

# Set up the display
WIDTH = 500
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load the assets
BACKGROUND = pygame.image.load("background.png").convert()
BASE = pygame.image.load("base.png").convert()
BIRD = pygame.image.load("bird.png").convert_alpha()
PIPE = pygame.image.load("pipe.png").convert_alpha()
FONT = pygame.font.SysFont('Arial', 30)

# Define game variables
gravity = 0.25
bird_movement = 0
bird_position = [50, HEIGHT // 2]
pipe_list = []
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)
score = 0
high_score = 0


def create_pipe():
    random_height = random.choice([200, 250, 300, 350])
    bottom_pipe = PIPE.get_rect(midtop=(WIDTH + 50, random_height))
    top_pipe = PIPE.get_rect(midbottom=(WIDTH + 50, random_height - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT - 100:
            SCREEN.blit(PIPE, pipe)
        else:
            flip_pipe = pygame.transform.flip(PIPE, False, True)
            SCREEN.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_position[1] <= -100 or bird_position[1] >= HEIGHT - 100:
        return False
    return True


def display_score():
    score_surface = FONT.render(f"Score: {int(score)}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
    SCREEN.blit(score_surface, score_rect)

    high_score_surface = FONT.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    SCREEN.blit(high_score_surface, high_score_rect)


# Main game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and check_collision(pipe_list):
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_RETURN and not check_collision(pipe_list):
                pipe_list = []
                bird_movement = 0
                bird_position = [50, HEIGHT // 2]
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())

    SCREEN.blit(BACKGROUND, (0, 0))

    # Bird movement
    bird_movement += gravity
    bird_rect = BIRD.get_rect(center=bird_position)
    bird_position[1] += bird_movement
    SCREEN.blit(BIRD, bird_rect)

    # Pipes movement
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Display score
    display_score()

    # Check collision
    if not check_collision(pipe_list):
        if score > high_score:
            high_score = score
        game_over_surface = FONT.render("Press ENTER to restart", True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(game_over_surface, game_over_rect)

    # Move the base
    SCREEN.blit(BASE, (0, HEIGHT - 100))

    # Update score
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe) and pipe.centerx < bird_rect.centerx:
            score += 0.5

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
