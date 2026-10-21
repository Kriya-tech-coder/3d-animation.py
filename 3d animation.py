
import math
import random
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Revolving Particle Heart")

clock = pygame.time.Clock()
BLACK = (5, 5, 18)

particles = []

def heart(t):
    x = 16 * math.sin(t) ** 3
    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )
    return x * 15, -y * 15


# Create particles
for i in range(1000):
    t = random.uniform(0, 2 * math.pi)
    tx, ty = heart(t)

    particles.append({
        "x": random.uniform(-300, 300),
        "y": random.uniform(-300, 300),
        "z": random.uniform(-100, 100),
        "tx": tx,
        "ty": ty,
        "tz": random.uniform(-35, 35),
    })

angle = 0
running = True

mouse_radius = 100
mouse_strength = 60

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    screen.fill(BLACK)
    angle += 0.012



    for p in particles:
        # Move particles toward heart shape
        p["x"] += (p["tx"] - p["x"]) * 0.06
        p["y"] += (p["ty"] - p["y"]) * 0.06
        p["z"] += (p["tz"] - p["z"]) * 0.06

        # Rotate particles in 3D
        x = (
            p["x"] * math.cos(angle)
            - p["z"] * math.sin(angle)
        )
        z = (
            p["x"] * math.sin(angle)
            + p["z"] * math.cos(angle)
        )
        y = p["y"]

        # Project 3D coordinates onto screen
        depth = z + 350
        scale = 350 / max(depth, 100)

        sx = int(WIDTH / 2 + x * scale)
        sy = int(HEIGHT / 2 + y * scale)

        # Mouse interaction
        dx = sx - mouse_x
        dy = sy - mouse_y
        distance = math.hypot(dx, dy)

        if 0 < distance < mouse_radius:
            force = (
                1 - distance / mouse_radius
            ) * mouse_strength

            if mouse_pressed:
                force *= 2

            p["x"] += (dx / distance) * force * 0.15
            p["y"] += (dy / distance) * force * 0.15

        # Draw every visible particle
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            glow = max(80, min(255, int(255 - z * 0.5)))
            color = (255, glow // 3, glow)
            radius = max(1, min(3, int(scale * 2)))

            pygame.draw.circle(
                screen, color, (sx, sy), radius
            )

    pygame.display.flip()

pygame.quit()
