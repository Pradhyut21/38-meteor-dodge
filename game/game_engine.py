import pygame
import random
from game.ship import Ship
from game.meteor import Meteor

WIDTH,HEIGHT=700,520
FPS=60
BG=(8,5,20)

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",26,bold=True)
        self.big_font=pygame.font.SysFont("monospace",46,bold=True)
        self.stars=[(random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(1,3)) for _ in range(80)]
        self.reset()

    def reset(self):
        self.ship=Ship(WIDTH//2,HEIGHT-80)
        self.meteors=[]
        self.lasers=[]
        self.timer=0
        self.spawn_interval=60
        self.score=0
        self.game_over=False
        self.started=False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if self.game_over: self.reset()
                    elif not self.started: self.started=True
                    else: self.lasers.append(self.ship.fire())
        return True

    def update(self):
        if self.game_over or not self.started: return
        keys=pygame.key.get_pressed()
        self.ship.move(keys,WIDTH,HEIGHT)
        for l in self.lasers:
            l.update()
        self.lasers=[l for l in self.lasers if not l.off_screen()]
        self.timer+=1
        if self.timer>=self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer=0
            self.spawn_interval=max(20,self.spawn_interval-0.3)
        for m in self.meteors:
            m.update()
            if m.collides(self.ship.rect):
                self.game_over=True
        for l in list(self.lasers):
            for m in list(self.meteors):
                if l.collides(m):
                    if m in self.meteors:
                        fragments = m.split()
                        self.meteors.remove(m)
                        self.meteors.extend(fragments)
                    if l in self.lasers:
                        self.lasers.remove(l)
                    break
        self.meteors=[m for m in self.meteors if not m.off_screen(HEIGHT)]
        self.score+=1

    def draw(self):
        self.screen.fill(BG)
        for sx,sy,sr in self.stars:
            pygame.draw.circle(self.screen,(200,200,220),(sx,sy),sr)
        for m in self.meteors: m.draw(self.screen)
        for l in self.lasers: l.draw(self.screen)
        self.ship.draw(self.screen)
        sc=self.font.render(f"Time: {self.score//60}s",True,(200,200,240))
        self.screen.blit(sc,(10,10))
        if not self.started:
            msg=self.font.render("Press SPACE to launch",True,(180,180,240))
            self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,HEIGHT//2))
        if self.game_over:
            ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            ov.fill((0,0,0,150))
            self.screen.blit(ov,(0,0))
            m=self.big_font.render("DESTROYED!",True,(220,80,60))
            s=self.font.render(f"Survived {self.score//60}s | SPACE to Restart",True,(200,200,200))
            self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
            self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2+20))
        pygame.display.flip()

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
