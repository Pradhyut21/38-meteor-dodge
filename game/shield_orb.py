import pygame
import random
import math

class ShieldOrb:
    def __init__(self, width=700):
        self.x = float(random.randint(50, width - 50))
        self.y = -25.0
        self.vy = random.uniform(1.2, 2.0)
        self.radius = 11
        self.timer = random.uniform(0, 100)
        self.color = (60, 220, 255)

    def update(self):
        self.timer += 0.08
        self.x += math.sin(self.timer) * 0.9
        self.y += self.vy

    def off_screen(self, height):
        return self.y > height + 30

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery
        dx, dy = self.x - cx, self.y - cy
        return (dx**2 + dy**2)**0.5 < (self.radius + 18)

    def draw(self, screen):
        cx, cy = int(self.x), int(self.y)
        # Pulsing outer ring
        pulse = int(3 * math.sin(self.timer * 2))
        outer_r = self.radius + 4 + pulse
        s = pygame.Surface((outer_r * 2 + 4, outer_r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(s, (60, 220, 255, 70), (outer_r + 2, outer_r + 2), outer_r)
        pygame.draw.circle(s, (140, 240, 255, 180), (outer_r + 2, outer_r + 2), outer_r, width=2)
        screen.blit(s, (cx - outer_r - 2, cy - outer_r - 2))

        # Core orb
        pygame.draw.circle(screen, (220, 255, 255), (cx, cy), self.radius - 2)
        pygame.draw.circle(screen, self.color, (cx, cy), self.radius, width=2)
