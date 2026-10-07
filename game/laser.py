import pygame

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = -10
        self.width = 4
        self.height = 14
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height, self.width, self.height)
        self.color = (60, 240, 255)

    def update(self):
        self.y += self.vy
        self.rect.y = int(self.y - self.height)

    def off_screen(self):
        return self.y < -20

    def collides(self, meteor):
        dx = meteor.x - self.x
        dy = meteor.y - self.y
        return (dx**2 + dy**2)**0.5 < (meteor.radius + 6)

    def draw(self, screen):
        # Laser core
        pygame.draw.rect(screen, (220, 255, 255), self.rect, border_radius=2)
        # Laser glow
        glow_rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4)
        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*self.color, 120), (0, 0, glow_rect.width, glow_rect.height), border_radius=3)
        screen.blit(glow_surf, (glow_rect.x, glow_rect.y))
