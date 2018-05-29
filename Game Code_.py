import pygame
pygame.init()

# tons of variables here
clock = pygame.time.Clock()
screenx = 800
screeny = 600
win = pygame.display.set_mode((screenx, screeny))
pygame.display.set_caption("get.rect()")
icon = pygame.image.load('mario.ico')
pygame.display.set_icon(icon)
char = pygame.image.load('Hat_man1.png')
bg = pygame.image.load('maxresdefault.jpg')
hitcount = 0
scorecount = 0
shootl = 0
run = True
scorefont = pygame.font.SysFont("comicsans", 32, True)

lasersound = pygame.mixer.Sound("Laser1.wav")
hitsound = pygame.mixer.Sound("Explosion.wav")
deathsound = pygame.mixer.Sound("Randomize4.wav")
jumpsound = pygame.mixer.Sound("Jump.wav")
music = pygame.mixer.music.load("Map.wav")
pygame.mixer.music.play(-1)


# class for solider and images for animation
class soldier(object):
    walkRight = [pygame.image.load('1.png'), pygame.image.load('2.png'),
                 pygame.image.load('3.png'), pygame.image.load('4.png')]
    walkLeft = [pygame.image.load('5.png'), pygame.image.load('6.png'), pygame.image.load('7.png'),
                pygame.image.load('8.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 50, 100)
        self.health = 10
        self.visible = True


    def draw(self,win):
        self.move()
        if self.visible:

            if self.walkCount + 1 >= 60:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 15], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 15], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5*(10 -self.health)), 10))

            self.hitbox = (self.x + 20, self.y, 50, 100)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #hitbox draw

        pass

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1
            hitsound.play()
        else:
            self.visible = False
            deathsound.play()
        print('ouch')

# class for the player
class player(object):
    walkRight = [pygame.image.load('Hat_man1.png'), pygame.image.load('Hat_man2.png'), pygame.image.load('Hat_man3.png'),
                pygame.image.load('Hat_man4.png')]
    walkLeft = [pygame.image.load('Hat_man5.png'), pygame.image.load('Hat_man6.png'), pygame.image.load('Hat_man7.png'),
                pygame.image.load('Hat_man8.png')]

    def __init__(self,x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + -20, self.y, 90, 100)


    def draw(self,win):
        if self.walkCount + 1 >= 60:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(self.walkLeft[self.walkCount // 15], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount // 15], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + -5, self.y, 80, 100)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # hitbox

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = 500
        self.walkCount = 0
        fonthit = pygame.font.SysFont("comicsans", 100)
        text = fonthit.render("Oof", 1, (255, 0, 0))
        win.blit(text, (screenx /2 - (text.get_width() /2), 200))
        pygame.display.update()

        i = 0
        while i < 50:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


# class for projectile/laser
class projectile(object):
    def __init__(self,x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# screen drawing section
def redrawGameWindow():
    win.fill((0, 0, 0))
    win.blit(bg, (0,0))
    text = scorefont.render("Score: " + str(hitcount), 1, (255, 255, 255))
    win.blit(text, (480, 20))
    wade.draw(win)
    baddie.draw(win)
    for laser in lasers:
        laser.draw(win)
    pygame.display.update()

# some things for the sprites on screen
wade = player(50, 500, 100, 100)
baddie = soldier(200, 500, 100, 100, 700)
lasers = []

#loop time baby

while run:
    clock.tick(60) # FPS Rate PCMR

    if baddie.visible == True:
        if wade.hitbox[1] < baddie.hitbox[1] + baddie.hitbox[3] and wade.hitbox[1] + wade.hitbox[3] > baddie.hitbox[1]:
            if wade.hitbox[0] + wade.hitbox[2] > baddie.hitbox[0] and wade.hitbox[0] < baddie.hitbox[0] + baddie.hitbox[2]:
                wade.hit()
                hitcount -= 5

    if shootl > 0:
        shootl += 1
    if shootl > 12:
        shootl  = 0

    for event in pygame.event.get(): #gotta quit somehow
        if event.type == pygame.QUIT:
            run = False

    for laser in lasers: #pew pew laser moving and removal
        if baddie.visible == True:
            if laser.y - laser.radius < baddie.hitbox[1] + baddie.hitbox[3] and laser.y + laser.radius > baddie.hitbox[1]:
                if laser.x + laser.radius > baddie.hitbox[0] and laser.x - laser.radius < baddie.hitbox[0] + baddie.hitbox[2]:
                    baddie.hit()
                    hitcount += 1
                    #scorecount += hitcount
                    lasers.pop(lasers.index(laser))

       # if hitcount > 3:
        #    hitcount = 0

        if laser.x < screenx and laser.x > 0:
            laser.x += laser.vel
        else:
            lasers.pop(lasers.index(laser))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and shootl == 0: # pressing X shoots the lasers and controls direction
        lasersound.play()
        if wade.left:
            facing = -1
        else:
            facing = 1

        if len(lasers) < 5:
            lasers.append(projectile(round(wade.x + wade.width //2 + 15), round(wade.y + wade.height//2 + 15 ), 3, (123, 255 , 0), facing))

        shootl = 1

    if keys[pygame.K_LEFT] and wade.x > wade.vel: # moving left
        wade.x -= wade.vel
        wade.left = True
        wade.right = False
        wade.standing = False
    elif keys[pygame.K_RIGHT] and wade.x < screenx - wade.width - wade.vel: # moving right
        wade.x += wade.vel
        wade.right = True
        wade.left = False
        wade.standing = False
    else:
        wade.standing = True # standing still
        wade.walkCount = 0

    if not wade.isJump:
        if keys[pygame.K_SPACE]: # jumping
            jumpsound.play()
            wade.isJump = True
            wade.right = False
            wade.left = False
    else:
        if wade.jumpCount >= -10: #jump math, not perfect
            neg = .6
            if wade.jumpCount < 0:
                neg = -.6
            wade.y -= (wade.jumpCount ** 2) / 2 * neg
            wade.jumpCount -= 1
        else:
            wade.isJump = False
            wade.jumpCount = 10
    redrawGameWindow()


pygame.quit()



