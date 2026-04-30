# Student number: 20024094 Daniel Barbu
# Module: Dissertation
# Application title: Visualising swarming behaviour for autonomous drones
# Version: 1.0
# File: main.py
# Date: Build across January, February, March, and April
# Date for submission: Deadline 01/05/2026


import csv
import os
import pygame
from swarm import Swarm

# Simulation window for width, height, background colour and FPS is frames per second
WIDTH = 1000
HEIGHT = 700
BACKGROUND = (20, 20, 30)
FPS = 60
CSV_FILENAME = "results.csv"


def draw_text(screen, text, x, y, font, color=(255, 255, 255)):
    # Renders and displays text on the simulation screen
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))


def get_next_run_id(filename):
    """
    Returns the next run ID in the format run_001, run_002, etc.
    """
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return "run_001"

    last_run_number = 0

    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header

        for row in reader:
            if not row:
                continue

            run_id = row[0].strip()
            if run_id.startswith("run_"):
                try:
                    run_number = int(run_id.split("_")[1])
                    if run_number > last_run_number:
                        last_run_number = run_number
                except (IndexError, ValueError):
                    pass

    return f"run_{last_run_number + 1:03d}"


def ensure_csv_header(filename):
    """
    Creates the CSV header only if the file does not exist or is empty.
    """
    file_exists = os.path.exists(filename)
    file_empty = (not file_exists) or os.path.getsize(filename) == 0

    if file_empty:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "run_id",
                "frame",
                "drone_count",
                "base_speed",
                "speed_multiplier",
                "neighbor_distance",
                "collisions",
                "avg_distance"
            ])


def main():
    pygame.init()  # Initializes pygame module
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Drone Swarm Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)

    drone_count = 40
    base_speed = 3.0
    speed_multiplier = 1.0
    neighbor_dist = 60

    swarm = Swarm(   # Initialize swarm system
        drone_count,
        WIDTH,
        HEIGHT,
        neighbor_dist=neighbor_dist,
        base_speed=base_speed
    )

    ensure_csv_header(CSV_FILENAME)  # Ensure CSV file structure exists
    current_run_id = get_next_run_id(CSV_FILENAME)  # Assign new experiment ID

    frame_count = 0  # Tracks simulation time steps
    run_started = False

    file = open(CSV_FILENAME, "a", newline="")
    writer = csv.writer(file)

    running = True
    while running:
        clock.tick(FPS)  # Maintains constant simulation speed (frames per second)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    drone_count += 10
                    swarm.reset(drone_count)
                    frame_count = 0
                    run_started = False

                elif event.key == pygame.K_DOWN:
                    drone_count = max(10, drone_count - 10)
                    swarm.reset(drone_count)
                    frame_count = 0
                    run_started = False

                elif event.key == pygame.K_s:
                    speed_multiplier += 0.2
                    frame_count = 0
                    run_started = False

                elif event.key == pygame.K_a:
                    speed_multiplier = max(0.2, speed_multiplier - 0.2)
                    frame_count = 0
                    run_started = False

                elif event.key == pygame.K_RIGHT:
                    neighbor_dist += 10
                    swarm.set_neighbor_distance(neighbor_dist)
                    frame_count = 0
                    run_started = False

                elif event.key == pygame.K_LEFT:
                    neighbor_dist = max(10, neighbor_dist - 10)
                    swarm.set_neighbor_distance(neighbor_dist)
                    frame_count = 0
                    run_started = False

                elif event.key == pygame.K_r:
                    swarm.reset(drone_count)
                    current_run_id = get_next_run_id(CSV_FILENAME)
                    frame_count = 0
                    run_started = True

        if run_started:  # Only increment frame counter when run is active
            frame_count += 1

        swarm.update(speed_multiplier=speed_multiplier)

        collisions = swarm.metrics.collisions  # Retrieve performance metrics
        avg_distance = swarm.metrics.average_distance()

        if run_started and frame_count % 30 == 0:  # Log data every 30 frames (controlled sampling interval)
            writer.writerow([
                current_run_id,
                frame_count,
                drone_count,
                base_speed,
                round(speed_multiplier, 2),
                neighbor_dist,
                collisions,
                round(avg_distance, 2)
            ])
            file.flush()

        screen.fill(BACKGROUND)  # Clear screen for new frame rendering
        swarm.draw(screen)

        draw_text(screen, f"Drones: {len(swarm.drones)}", 15, 15, font)
        draw_text(screen, f"Collisions: {collisions}", 15, 40, font)
        draw_text(screen, f"Avg Distance: {avg_distance:.2f}", 15, 65, font)
        draw_text(screen, f"Speed Multiplier: {speed_multiplier:.2f}", 15, 90, font)
        draw_text(screen, f"Neighbor Distance: {neighbor_dist}", 15, 115, font)

        draw_text(screen, "UP/DOWN: Drone Count", 15, 155, font)
        draw_text(screen, "S/A: Speed + / -", 15, 180, font)
        draw_text(screen, "RIGHT/LEFT: Neighbor Distance + / -", 15, 205, font)
        draw_text(screen, "R: Start New Logged Run", 15, 230, font)
        draw_text(screen, f"Current Run ID: {current_run_id}", 15, 255, font)

        if not run_started:
            draw_text(screen, "Set parameters, then press R to start a new run", 15, 290, font, (255, 220, 120))
        else:
            draw_text(screen, f"Run active - frame {frame_count}", 15, 290, font, (120, 255, 120))

        pygame.display.flip()

    file.close()
    pygame.quit()


if __name__ == "__main__":
    main()