import pygame

SPEED = 5

class Ship:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x-20, y-20, 40, 40)
        self.color = (80, 160, 240)
        self.trail = []
        self.has_shield = False
        self.shield_anim = 0

    def fire(self):
        from game.laser import Laser
        return Laser(self.rect.centerx, self.rect.top)

    def move(self, keys, width, height):
        dx=dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx=-SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx=SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy=-SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy=SPEED
        self.rect.x=max(0,min(width-self.rect.width,self.rect.x+dx))
        self.rect.y=max(0,min(height-self.rect.height,self.rect.y+dy))
        self.trail.append(tuple(self.rect.center))
        if len(self.trail)>10: self.trail.pop(0)
        if self.has_shield:
            self.shield_anim = (self.shield_anim + 0.1) % 360

    def draw(self, screen):
        for i,pos in enumerate(self.trail):
            alpha=20+i*20
            r=3+i//2
            s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(s,(80,160,240,alpha),(r,r),r)
            screen.blit(s,(pos[0]-r,pos[1]-r))
        # ship body
        cx,cy=self.rect.center
        pts=[(cx,cy-18),(cx-14,cy+14),(cx,cy+6),(cx+14,cy+14)]
        pygame.draw.polygon(screen,self.color,pts)
        # engine glow
        pygame.draw.circle(screen,(255,180,60),(cx,cy+12),5)

        # energy shield barrier
        if self.has_shield:
            import math
            pulse = int(2 * math.sin(self.shield_anim))
            shield_r = 28 + pulse
            s = pygame.Surface((shield_r*2+4, shield_r*2+4), pygame.SRCALPHA)
            pygame.draw.circle(s, (80, 220, 255, 65), (shield_r+2, shield_r+2), shield_r)
            pygame.draw.circle(s, (180, 240, 255, 200), (shield_r+2, shield_r+2), shield_r, width=2)
            screen.blit(s, (cx - shield_r - 2, cy - shield_r - 2))
