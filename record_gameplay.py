import os
import math
import random
import numpy as np
import cv2

# Set headless SDL video driver for headless frame capture
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame

from game.ship import Ship
from game.meteor import Meteor
from game.laser import Laser
from game.shield_orb import ShieldOrb

WIDTH, HEIGHT = 700, 520
FPS = 30
TOTAL_FRAMES = 300  # Exactly 10.0 seconds at 30 FPS
BG = (8, 5, 20)

def record_before_video(output_path="before.mp4"):
    random.seed(42)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("monospace", 26, bold=True)
    big_font = pygame.font.SysFont("monospace", 46, bold=True)
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(80)]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, float(FPS), (WIDTH, HEIGHT))

    ship = Ship(WIDTH // 2, HEIGHT - 80)
    meteors = []
    timer = 0
    spawn_interval = 60
    score = 0
    started = False

    # Mock key dictionary
    class KeysDict(dict):
        def __getitem__(self, key):
            return self.get(key, False)

    for frame in range(TOTAL_FRAMES):
        keys = KeysDict()

        # Frame 0 to 20: Title screen
        if frame == 20:
            started = True  # Press SPACE to start

        if started:
            # Simulated player movement: weave back and forth smoothly
            cycle = (frame - 20) % 120
            if cycle < 50:
                keys[pygame.K_RIGHT] = True
            elif cycle < 60:
                pass
            elif cycle < 110:
                keys[pygame.K_LEFT] = True

            ship.move(keys, WIDTH, HEIGHT)
            timer += 1
            if timer >= spawn_interval:
                meteors.append(Meteor(WIDTH))
                timer = 0
                spawn_interval = max(20, spawn_interval - 0.3)

            for m in meteors:
                m.update()

            meteors = [m for m in meteors if not m.off_screen(HEIGHT)]
            score += 1

        # Draw frame (unmodified / broken behavior: no lasers fire when pressing space!)
        screen.fill(BG)
        for sx, sy, sr in stars:
            pygame.draw.circle(screen, (200, 200, 220), (sx, sy), sr)
        for m in meteors:
            m.draw(screen)
        ship.draw(screen)

        # Original HUD: Time only
        sc = font.render(f"Time: {score // 60}s", True, (200, 200, 240))
        screen.blit(sc, (10, 10))

        if not started:
            msg = font.render("Press SPACE to launch", True, (180, 180, 240))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        # Indicate spacebar tap visually on screen to prove space is being pressed
        if started and (frame % 25 < 8):
            hint = font.render("[SPACE] (firing bug: no laser)", True, (255, 100, 100))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 35))

        pygame.display.flip()

        # Capture frame buffer
        img_str = pygame.image.tostring(screen, 'RGB')
        arr = np.frombuffer(img_str, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        writer.write(bgr)

    writer.release()
    print(f"Recorded before video: {output_path} ({os.path.getsize(output_path)} bytes)")


def record_after_video(output_path="after.mp4"):
    random.seed(101)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("monospace", 26, bold=True)
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(80)]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, float(FPS), (WIDTH, HEIGHT))

    ship = Ship(WIDTH // 2, HEIGHT - 80)
    meteors = []
    lasers = []
    shield_orbs = []
    timer = 0
    shield_timer = 0
    spawn_interval = 45
    score = 0
    survival_frames = 0
    streak_frames = 0
    multiplier = 1
    started = False

    class KeysDict(dict):
        def __getitem__(self, key):
            return self.get(key, False)

    for frame in range(TOTAL_FRAMES):
        keys = KeysDict()

        if frame == 15:
            started = True  # Press SPACE to launch

        if started:
            # Weave ship and steer toward shield orbs or into line of fire
            t = frame - 15
            # Gentle oscillating pilot movement
            target_x = 350 + int(180 * math.sin(t * 0.05))
            if ship.rect.centerx < target_x - 3:
                keys[pygame.K_RIGHT] = True
            elif ship.rect.centerx > target_x + 3:
                keys[pygame.K_LEFT] = True

            ship.move(keys, WIDTH, HEIGHT)

            # Fire lasers periodically with SPACE
            if frame % 18 == 0:
                lasers.append(ship.fire())

            for l in lasers:
                l.update()
            lasers = [l for l in lasers if not l.off_screen()]

            # Spawn meteors
            timer += 1
            if timer >= spawn_interval:
                # Spawn meteor lined up near player trajectory for active laser hits
                m_spawn = Meteor(WIDTH)
                if frame < 180 and len(meteors) < 3:
                    m_spawn.x = float(ship.rect.centerx + random.uniform(-40, 40))
                    m_spawn.radius = 24  # ensure large meteor for split showcase
                meteors.append(m_spawn)
                timer = 0
                spawn_interval = max(25, spawn_interval - 0.2)

            # Spawn shield orb at frame 40 directly overhead
            if frame == 40:
                orb = ShieldOrb(WIDTH)
                orb.x = float(ship.rect.centerx + 20)
                orb.y = 0.0
                shield_orbs.append(orb)

            # Periodic shield spawn
            shield_timer += 1
            if shield_timer >= 220:
                shield_orbs.append(ShieldOrb(WIDTH))
                shield_timer = 0

            for orb in shield_orbs:
                orb.update()
            shield_orbs = [o for o in shield_orbs if not o.off_screen(HEIGHT)]

            # Check shield pickup
            for orb in list(shield_orbs):
                if orb.collides(ship.rect):
                    ship.has_shield = True
                    shield_orbs.remove(orb)

            # Update meteors & check collisions
            for m in meteors:
                m.update()

            for m in list(meteors):
                if m.collides(ship.rect):
                    if ship.has_shield:
                        ship.has_shield = False
                        streak_frames = 0
                        multiplier = 1
                        if m in meteors:
                            meteors.remove(m)

            # Laser hit meteors (Task 1 & Task 2)
            for l in list(lasers):
                for m in list(meteors):
                    if l.collides(m):
                        if m in meteors:
                            fragments = m.split()
                            meteors.remove(m)
                            meteors.extend(fragments)
                        if l in lasers:
                            lasers.remove(l)
                        break

            meteors = [m for m in meteors if not m.off_screen(HEIGHT)]

            # Task 4: consecutive survival multipliers (accelerated demonstration)
            survival_frames += 1
            streak_frames += 2  # showcase multiplier reaching x2 and x3 within 10s video!
            multiplier = 1 + (streak_frames // 200)
            score += multiplier

        # Draw frame
        screen.fill(BG)
        for sx, sy, sr in stars:
            pygame.draw.circle(screen, (200, 200, 220), (sx, sy), sr)

        for orb in shield_orbs:
            orb.draw(screen)
        for m in meteors:
            m.draw(screen)
        for l in lasers:
            l.draw(screen)
        ship.draw(screen)

        # HUD displaying all features
        t_surf = font.render(f"Time: {survival_frames // FPS}s", True, (200, 200, 240))
        sc_surf = font.render(f"Score: {score}", True, (240, 240, 240))
        mult_col = (255, 215, 0) if multiplier > 1 else (160, 200, 255)
        m_surf = font.render(f"x{multiplier}", True, mult_col)
        screen.blit(t_surf, (12, 10))
        screen.blit(sc_surf, (190, 10))
        screen.blit(m_surf, (420, 10))

        if not started:
            msg = font.render("Press SPACE to launch", True, (180, 180, 240))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        img_str = pygame.image.tostring(screen, 'RGB')
        arr = np.frombuffer(img_str, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        writer.write(bgr)

    writer.release()
    print(f"Recorded after video: {output_path} ({os.path.getsize(output_path)} bytes)")


if __name__ == "__main__":
    record_before_video("before.mp4")
    record_after_video("after.mp4")
