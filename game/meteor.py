import pygame
import random
import math

class Meteor:
    def __init__(self, width=None, x=None, y=None, radius=None, vx=None, vy=None, color=None):
        if x is not None and y is not None:
            self.x = float(x)
            self.y = float(y)
            self.radius = radius if radius is not None else 10
            self.vx = vx if vx is not None else random.uniform(-2, 2)
            self.vy = vy if vy is not None else random.uniform(2, 4)
            self.color = color if color is not None else (180, 100, 60)
        else:
            self.x = float(random.randint(0, width if width else 700))
            self.y = -30.0
            self.radius = random.randint(12, 28)
            angle = random.uniform(70, 110)
            speed = random.uniform(2, 5)
            self.vx = math.cos(math.radians(angle)) * speed
            self.vy = math.sin(math.radians(angle)) * speed
            self.color = (
                random.randint(160, 220),
                random.randint(80, 120),
                random.randint(40, 80)
            )
        self.rot = 0
        self.rot_speed = random.uniform(-4, 4)

    def is_large(self):
        return self.radius > 16

    def split(self):
        if not self.is_large():
            return []
        child_radius = max(8, int(self.radius * 0.58))
        f1 = Meteor(
            x=self.x - child_radius,
            y=self.y,
            radius=child_radius,
            vx=self.vx - random.uniform(1.8, 3.2),
            vy=self.vy * 0.9 + random.uniform(-0.5, 1.2),
            color=self.color
        )
        f2 = Meteor(
            x=self.x + child_radius,
            y=self.y,
            radius=child_radius,
            vx=self.vx + random.uniform(1.8, 3.2),
            vy=self.vy * 0.9 + random.uniform(-0.5, 1.2),
            color=self.color
        )
        return [f1, f2]

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot = (self.rot + self.rot_speed) % 360

    def off_screen(self, height):
        return self.y > height + 60 or self.x < -60 or self.x > 760

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery
        dx, dy = self.x - cx, self.y - cy
        return (dx**2 + dy**2)**0.5 < self.radius + 16

    def draw(self, screen):
        pts = []
        for i in range(7):
            angle = math.radians(self.rot + i * (360 / 7))
            r = self.radius * (0.8 + 0.2 * (i % 2))
            pts.append((int(self.x + r * math.cos(angle)), int(self.y + r * math.sin(angle))))
        pygame.draw.polygon(screen, self.color, pts)
        inner = [(int(self.x + (r * 0.5) * math.cos(math.radians(self.rot + i * (360 / 7)))),
                  int(self.y + (r * 0.5) * math.sin(math.radians(self.rot + i * (360 / 7)))))
                 for i, (cx, cy) in enumerate(pts)]
        pygame.draw.polygon(screen, tuple(max(0, c - 40) for c in self.color), inner)
