import pygame
import random
pygame.init()
pygame.display.set_caption("EPİC WAR")
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
# images                        #pygame.image.load("C:/Users/90505/Desktop/foto/a.jpg")
bg = pygame.image.load('bg.jpg')  # background

# musics  runs .aiff
screamSound = pygame.mixer.Sound('scream.aiff')
bulletSound = pygame.mixer.Sound("gungun.aiff")
hitSound = pygame.mixer.Sound("hit.aiff")
reloadSound = pygame.mixer.Sound("reload.aiff")
music = pygame.mixer.music.load("paradise.mp3")
pygame.mixer.music.play(-1)

# window
window_height = 480
window_width = 500
size = (window_width, window_height)
win = pygame.display.set_mode((size))  # surface


# character
class player():
    walkRight = [pygame.image.load('R1.png'),
                 pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'),
                 pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'),
                 pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
    char = pygame.image.load('standing.png')  # default

    def __init__(self, player,x, y, width, height, health, power, ammo, rate, vel, jumpcount):
        self.player = player
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.left = False
        self.right = False
        self.walkcount = 0
        self.isjump = False
        self.jumpcount = jumpcount
        self.fixedjumpcount = self.jumpcount
        self.standing = True
        self.hitbox = (self.x + 19, self.y + 13, 26, 50) #it is unchancgeable, doesn't follow our character so you must update it below
        self.hitscore = 0
        self.collision = 0
        self.shootLoop = 0
        self.rate = rate
        self.power = power
        self.ammo = ammo
        self.health = health
        self.fixedhealth = self.health
        self.visible = True
    def redraw(self, win):
        if self.visible == True:
            self.hitbox = (self.x + 19, self.y + 13, 26, 50)
            pygame.draw.rect(win, (255,9,9), self.hitbox, 2)
            font = pygame.font.SysFont("comicsans", 25)
            text = font.render(("player: {}".format(self.player)), 1, (100,0,100))
            win.blit(text, ((self.x + 2 ), (self.y -20)))
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - 20, 50 * (self.health / self.fixedhealth), 10))
            if self.walkcount + 1 >= 27:  # back to the first photo/there are 9 photos
                self.walkcount = 0
            if not (man.standing):
                if self.left:
                    win.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
                    self.walkcount += 1
                elif self.right:
                    win.blit(self.walkRight[(self.walkcount // 3)], (self.x, self.y))
                    self.walkcount += 1
            else:
                if self.right:
                    win.blit(self.walkRight[0], (self.x, self.y))
                else:
                    win.blit(self.walkLeft[0], (self.x, self.y))

    def coll(self, power):
        if self.visible == True:
            print(0)
            if self.collision == 0:
                print(1)
                #screamSound.play()
                self.health -= power
                self.collision += 1
                if self.health > 0:
                    print("2")
                    fontman = pygame.font.SysFont("comicsans", 50)
                    textman = fontman.render(str(self.player) + " -{}".format(power), 1, (255, 0, 0))
                    win.blit(textman, ( ( ( window_width / 2) - ( textman.get_width() / 2)), ( window_height / 2 - textman.get_height() / 2) ) )
                    self.isjump = False
                    self.jumpcount = self.fixedjumpcount
                    self.x = 10
                    self.y = 416
                    pygame.display.update()
                    self.hitscore -= power
                    delay (200)
                else:
                    print("player {} death".format(self.player))
                    self.visible = False
                    fontdeath = pygame.font.SysFont("comicsans", 50, True)
                    textdeath = fontdeath.render("PLAYER {} DİED!".format(self.player), 1, (50,50,50), (255,0,0))
                    win.blit(textdeath, ( ( ( window_width / 2) - ( textdeath.get_width() / 2) ), ( (window_height / 2) - (textdeath.get_height() / 2))))
                    pygame.display.update()
                    delay(200)

# enemy
class enemy():
    walkRight = [pygame.image.load("R1E.png"), pygame.image.load("R2E.png"), pygame.image.load("R3E.png"),
                 pygame.image.load("R4E.png"), pygame.image.load("R5E.png"), pygame.image.load("R6E.png"),
                 pygame.image.load("R7E.png"), pygame.image.load("R8E.png"), pygame.image.load("R9E.png"),
                 pygame.image.load("R10E.png"), pygame.image.load("R11E.png")]
    walkLeft = [pygame.image.load("L1E.png"), pygame.image.load("L2E.png"), pygame.image.load("L3E.png"),
                pygame.image.load("L4E.png"), pygame.image.load("L5E.png"), pygame.image.load("L6E.png"),
                pygame.image.load("L7E.png"), pygame.image.load("L8E.png"), pygame.image.load("L9E.png"),
                pygame.image.load("L10E.png"), pygame.image.load("L11E.png")]

    def __init__(self, x, y, width, height, end, vel, health, power):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.vel = vel
        self.walkCount = 0
        self.hitbox = (self.x + 13, self.y + 4, 40, 57)
        self.power = power
        self.health = health
        self.fixedhealth = self.health
        self.visible = True

    def draw(self, win):
        self.move()
        self.hitbox = (self.x + 13, self.y + 4, 40, 57)
        if self.visible == True:
            if self.walkCount > 32:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - 20, 50 * (self.health / self.fixedhealth), 10))
        if self.fixedhealth <= 0:
            print("death")

    def move(self):
        if self.vel > 0:  # to right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
                self.walkCount += 1
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
                self.walkCount += 1
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self,power):
        hitSound.play()
        if self.health > 0:
            self.health -= power
            print(self.health)
        else:
            self.visible = False
            enemylist.pop(0)


# projectile
class projectile():
    def __init__(self, win, color, x, y, radius, facing):
        self.win = win
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.vel = 8 * self.facing

    def draw(self):
        pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

#boosts
class boost():
    def __init__(self):
        self.x = random.randrange(100, 400)
        self.y = random.randrange(300, 400)
        self.radius = random.randrange(15, 20)
        self.font = pygame.font.SysFont("comicsans", 30, False, True)
class boost_rate(boost):
    def draw(self,win):
        pygame.draw.circle(win, (100,0,0), (self.x, self.y), self.radius)
    def impact(self, who):
        who.rate *= 0.75
        text = self.font.render("player{} +rate".format(who.player), 1, (100,0,0))
        win.blit(text, ( ( ( window_width / 2) - (text.get_width() / 2) ), ( ( window_height / 2) - (text.get_height() / 2 ) ) ) )
        pygame.display.update()
        delay(200)
class boost_ammo(boost):
    def draw(self, win):
        pygame.draw.circle(win, (0,0,100), (self.x, self.y), self.radius)
    def impact(self, who):
        who.ammo += 1
        text = self.font.render("player{} +ammo".format(who.player), 1, (0,0,100) )
        win.blit(text, ( ( ( window_width / 2) - (text.get_width() / 2)), ( ( window_height / 2) - (text.get_height() / 2 ) ) ) )
        pygame.display.update()
        delay(200)
class boost_vel(boost):
    def draw(self, win):
        pygame.draw.circle(win, (200,100,200), (self.x, self.y), self.radius)
    def impact(self, who):
        who.vel += 1
        text = self.font.render("player{} +velocity".format(who.player), 1, (200,100,100))
        win.blit(text, ( ( ( window_width / 2 ) - (text.get_width() / 2 )),( (window_height / 2 ) - (text.get_height() / 2) ) ) )
        pygame.display.update()
        delay(200)
class boost_health(boost):
    def draw(self, win):
        pygame.draw.circle(win, (255,255,0), (self.x, self.y), self.radius)
    def impact(self, who):
        who.health += 50
        text = self.font.render("player{} +health".format(who.player), 1, (255,255,0))
        win.blit(text, ( ( ( window_width / 2 ) - (text.get_width() / 2)), ( ( window_height / 2) - (text.get_height() / 2) ) ) )
        pygame.display.update()
        delay(200)
class boost_power(boost):
    def draw(self, win):
        pygame.draw.circle(win, (50,200,100), (self.x, self.y), self.radius)
    def impact(self, who):
        who.power += 2
        text = self.font.render("player{} +power".format(who.player), 1, (50,200,100))
        win.blit(text, ( ( (window_width / 2) - (text.get_width() / 2) ), ( (window_height / 2) - (text.get_height() / 2) ) ) )
        pygame.display.update()
        delay(200)
# score table
class score():
    def __init__(self, win, x, y, width, height):
        self.win = win
        self.y = y
        self.x = x
        self.width = width
        self.height = height
    def draw(self, who):
        if who.hitscore < 255 and who.hitscore >= 0:
            pygame.draw.rect(self.win, (255 - who.hitscore, 0 + who.hitscore, 0), (self.x, self.y, self.width, self.height))
        elif who.hitscore < 0:
            pygame.draw.rect(self.win, (255, 0, 0), (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.win, (0, 255, 0), (self.x, self.y, self.width, self.height))

#time delay
def delay(time):
    i = 0
    while i < time:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
#redraw
def redrawgamewindow():
    win.blit(bg, (0, 0))  # restart background
    man.redraw(win)  # put man
    if player_number == 2:
        man2.redraw(win)
    if len(enemylist) > 1:
        enemylist[0].draw(win)
        enemylist[1].draw(win)
    elif len(enemylist) > 0 :
        enemylist[0].draw(win)

    else :
        font_win = pygame.font.SysFont("comicsans", 100, True)
        textwin = font_win.render("WİN", 1, (0,0,0))
        win.blit(textwin, (((window_width // 2 ) - (textwin.get_width() // 2)), ((window_height // 2) - (textwin.get_height() //2))))
        pygame.display.update()
        delay(1000)
        pygame.quit()

    fontlose = pygame.font.SysFont("comicsans", 50, True)
    if player_number == 2:
        if man.visible == False and man2.visible == False:
            textlose = fontlose.render("LOSE !", 1, (255, 0, 0))
            win.blit(textlose, (
            ((window_width / 2) - (textlose.get_width() / 2)), ((window_height / 2) - (textlose.get_height() / 2))))
            pygame.display.update()
            delay(1000)
            pygame.quit()
    else :
        if man.visible == False :
            textlose = fontlose.render("LOSE !", 1, (255, 0, 0))
            win.blit(textlose, (
                ((window_width / 2) - (textlose.get_width() / 2)), ((window_height / 2) - (textlose.get_height() / 2))))
            pygame.display.update()
            delay(1000)
            pygame.quit()

    if len(active) > 0:
        active[0].draw(win)
    font_score = pygame.font.SysFont("comicsans", 20, True, True)
    score.draw(man)
    text = font_score.render("MAN1-Score: {} ".format(man.hitscore), 1, (0,0,0))
    win.blit(text, (score.x + 20, score.y + 10))
    score2.draw(man2)
    text = font_score.render("MAN2-Score: {} ".format(man2.hitscore), 1, (0, 0, 0))
    win.blit(text, (score2.x + 20, score2.y + 10))
    for bullet in bullets:
        bullet.draw()
    for bullet in bullets2:
        bullet.draw()
    pygame.display.update()  # update the scree

#player 1/2
win.fill((255,255,255))#delete ex
pygame.draw.circle(win, (255,0,0), (130,200), 100)
pygame.draw.circle(win, (0,255,0), (370,200), 100)
fontchoose = pygame.font.SysFont("comicsans", 30, True)
textchoose1 = fontchoose.render("1 PLAYER(space)", 1, (0,0,100))
textchoose2 = fontchoose.render(" 2 PLAYER(enter)", 1, (0,0,100))
win.blit(textchoose1, (60,180))
win.blit(textchoose2, (280,180))
pygame.display.update()
player_number = 1
i = 0
while i < 100:
    keys = pygame.key.get_pressed()
    pygame.time.delay(100)
    i += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
    if keys[pygame.K_KP_ENTER]:
        player_number = 2
        i = 1000
    if keys[pygame.K_SPACE]:
        player_number = 1
        i = 1000





#customization
location = [0,0]

fontplayer = pygame.font.SysFont("comicsans", 50, True)
fontulti = pygame.font.SysFont("comicsans", 40, False, True)
fontskill = pygame.font.SysFont("comicsans", 30)


def rect(surface, color, position, width = 0):
    pygame.draw.rect(surface, color, position, width)
    pygame.display.update()
class custom():
    def __init__(self, default, value,color, location, x, y = 315 , width = 50, height = 50):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.location = location
            self.default = default
            self.change = value
            self.value = 0
            self.ultinumber = 0
    def draw(self,name):
            rect(win, self.color, (self.x, self.y, self.width, self.height))
            if location == self.location:
                rect(win, (0, 0, 200), (self.x - 3, self.y - 3, self.width + 6, self.height + 6))
            textname = fontskill.render(name, 1, self.color)
            win.blit(textname, (self.x, self.y - 65))
            textvalue = fontskill.render("{}".format(self.default + self.value), 1, (0, 0, 0))
            win.blit(textvalue, (self.x + ((self.width / 2) - (textvalue.get_width() / 2)),  (self.y + ((self.height / 2) - (textvalue.get_height() / 2)))))
            pygame.display.update()

    def val(self, turn = None):
            if turn == 1:
                self.value  += self.change
            elif turn == -1:
                self.value -= self.change
            return self.default + self.value

class ulti(custom):
    def draw(self,name):
            rect(win, self.color, (self.x, self.y, self.width, self.height))
            if location == self.location:
                rect(win, (0, 0, 200), (self.x - 3, self.y - 3, self.width + 6, self.height + 6))

            textname = fontulti.render(name, 1, self.color)
            win.blit(textname, (self.x + ((self.width / 2) - (textname.get_width() / 2)), self.y - 35))

            ultichoose = ultilist[self.ultinumber]
            textvalue = fontulti.render("{}".format(ultichoose), 1, (0, 0, 0))
            win.blit(textvalue, (self.x + ((self.width / 2) - (textvalue.get_width() / 2)),(self.y + (self.height / 2) - (textvalue.get_height() / 2))))
            pygame.display.update()

    def val(self, turn = None):
        if turn == 1 and self.ultinumber < 3:
            self.ultinumber += 1
        elif turn == 1 and self.ultinumber == 3:
            self.ultinumber = 0
        if turn == -1 and self.ultinumber > 0:
            self.ultinumber -= 1
        elif turn == -1 and self.ultinumber == 0:
            self.ultinumber = 3


ultilist = ["dragon","apple","banana","cherry"]
ulti = ulti(ultilist[0], 1, (100,100,100), [0,1], 200, 125, 100, 75)



health = custom(50, 20,(0,150,0), [0,0], 50)

power = custom(3, 1, (100,0,0), [1,0], 125)

ammo = custom(3, 1, (0,100,100), [2,0],200)

rate = custom(15, 1, (100, 100, 0), [3,0], 275)

vel = custom(5,1, (200,200,200), [4,0], 350)

jump = custom(8, 1, (0,0,200), [5,0], 425)

limit = 30

win.fill((255,255,255))

delay(20)

while True:
    delay(10)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if location[1] == 0:
            if location[0] < 6:
                location[0] += 1
            else :
                location[0] = 0

    elif keys[pygame.K_LEFT]:
        if location[1] == 0:
            if location[0] > 0:
                location[0] -= 1
            else:
                location[0] = 6

    if keys[pygame.K_KP_ENTER]:
        if location[1] < 1:
            location[0] = 0
            location[1] += 1
        elif location[1] > 0:
            location[1] -= 1

    if keys[pygame.K_a]:
        break

    if keys[pygame.K_UP]:
        if location == [0,0] and limit > 0:
            health.val(1)
            limit -= 1
        elif location == [1,0] and limit > 0:
            power.val(1)
            limit -= 1
        elif location == [2,0] and limit > 0:
            ammo.val(1)
            limit -= 1
        elif location == [3,0] and limit > 0:
            rate.val(-1)
            limit -= 1
        elif location == [4,0] and limit > 0:
            vel.val(1)
            limit -= 1
        elif location == [5,0] and limit > 0:
            jump.val(1)
            limit -= 1
        elif location == [0,1] :
            ulti.val(1)
            limit -= 1
    if keys[pygame.K_DOWN]:
        if location == [0,0] and health.default < health.default + health.value :
            health.val(-1)
            limit += 1
        elif location == [1,0] and power.default < power.default + power.value :
            power.val(-1)
            limit += 1
        elif location == [2,0] and ammo.default < ammo.default + ammo.value :
            ammo.val(-1)
            limit += 1
        elif location == [3,0] and rate.default < rate.default + rate.value :
            rate.val(1)
            limit += 1
        elif location == [4,0] and vel.default < vel.default + vel.value :
            vel.val(-1)
            limit += 1
        elif location == [5,0] and jump.default < jump.default + jump.value :
            jump.val(-1)
            limit += 1
        elif location == [0,1] :
            ulti.val(-1)
            limit += 1

    textplayer = fontplayer.render("player - {}".format(1), 1, (0, 0, 0))
    win.blit(textplayer, ((window_width / 2) - (textplayer.get_width() / 2), 10))

    ulti.draw("ulti")

    health.draw("health")
    power.draw("power")
    rate.draw("rate")
    ammo.draw("ammo")
    vel.draw("velocity")
    jump.draw("jump")

    pygame.display.update()





#if player_number == 2
# main loop
man = player(1, 300, 416, 64, 64, health.val(), power.val(), ammo.val(), rate.val(), vel.val(), jump.val())
man2 = player(2, 100, 416, 64, 64, 300, 20, 5, 10, 10, 8)
if player_number == 2:
    playerlist = [man, man2]
else:
    playerlist = [man]

enemy2 = enemy(60, 421, 64, 64, 450, 5, 500, 30)
enemy = enemy(50, 421, 64, 64, 450, 2, 220, 20)
enemylist = [enemy,enemy2]



man.left = True
man2.left = True

bullets = []
bullets2 = []

score2 = score(win, 30, 10, 170, 50)
score = score(win, 300, 10, 170, 50)

brate = boost_rate()
bvel = boost_vel()
bammo = boost_ammo()
bhealth = boost_health()
bpower = boost_power()
boostlist = [brate, bvel, bammo, bhealth, bpower]
active = []
activelimit = 0
run = True
while run:
    keys = pygame.key.get_pressed()
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if len(active) == 0 and activelimit == 0:
        x = random.randrange(0,5)
        active.append(boostlist[x])
    elif activelimit > 500:
        activelimit = 0
    else :
        activelimit += 1

    for player in playerlist:
        if player.collision > 20:
            player.collision = 0
        elif player.collision > 0 :
            player.collision +=1
    #player1
    if man.visible == True :
        if man.shootLoop > man.rate:
            reloadSound.play()
            man.shootLoop = 0
        elif man.shootLoop > 0:
            man.shootLoop += 1
        if len(active) > 0:
            if man.hitbox[0] + man.hitbox[2] > active[0].x - active[0].radius and man.hitbox[0] < active[0].x + active[0].radius:
                if man.hitbox[1] + man.hitbox[3] > active[0].y - active[0].radius and man.hitbox[1] <active[0].y + active[0].radius:
                    active[0].impact(man)
                    active.pop(0)

        if len(enemylist) > 0:
            for enemy in enemylist:
                if enemy.visible == True:
                    for bullet in bullets:
                        if len(enemylist) > 0:
                            if bullet.y < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                                if bullet.x - bullet.radius < (enemy.hitbox[0]) + (enemy.hitbox[2]) and bullet.x + bullet.radius > enemy.hitbox[0]:
                                    enemy.hit(man.power)
                                    man.hitscore += 10
                                    bullets.pop(bullets.index(bullet))
                        if bullet.x < 500 and bullet.x > 0:
                            bullet.x += bullet.vel
                        else:
                            bullets.pop(bullets.index(bullet))

                    if enemy.visible == True :
                        if man.hitbox[0] + man.hitbox[2] > enemy.hitbox[0] and man.x < (enemy.hitbox[0]) + (enemy.hitbox[2]):
                            if man.hitbox[1] + man.hitbox[3] > enemy.hitbox[1] and man.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3]:
                                man.coll(enemy.power)
                                print("man.col")
        if player_number == 2:
            if keys[pygame.K_KP_ENTER] and man.shootLoop == 0:
                bulletSound.play()
                if man.left:
                    projectile.facing = -1
                else:
                    projectile.facing = 1
                if len(bullets) < man.ammo:
                    bullets.append(projectile(win, (255, 0, 0), round(man.x + man.width // 2), round(man.y + man.height // 2), 5, projectile.facing))
                man.shootLoop = 1
        else:
            if keys[pygame.K_SPACE] and man.shootLoop == 0:
                bulletSound.play()
                if man.left:
                    projectile.facing = -1
                else:
                    projectile.facing = 1
                if len(bullets) < man.ammo:
                    bullets.append(projectile(win, (255, 0, 0), round(man.x + man.width // 2), round(man.y + man.height // 2), 5, projectile.facing))
                man.shootLoop = 1
        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False

        elif keys[pygame.K_RIGHT] and man.x < window_width - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False

        else:  # reset when no input
            man.walkcount = 0


        if not (man.isjump):
            if keys[pygame.K_UP]:
                man.isjump = True
                man.right = False
                man.Left = False
                man.walkcount = 0
        else:
            if man.jumpcount >= - man.fixedjumpcount:  # jump action
                neg = 1
                if man.jumpcount < 0:
                    neg = -1
                man.y -= (man.jumpcount ** 2) * 0.5 * neg
                man.jumpcount -= 1

            else:  # when jump finished
                man.isjump = False
                man.jumpcount = man.fixedjumpcount


    # player2
    if player_number == 2:
        if man2.visible == True :
            if man2.shootLoop > man2.rate:
                reloadSound.play()
                man2.shootLoop = 0
            elif man2.shootLoop > 0:
                man2.shootLoop += 1
            if len(active) > 0 :
                if man2.hitbox[0] + man2.hitbox[2] > active[0].x - active[0].radius and man2.hitbox[0] < active[0].x + active[0].radius:
                    if man2.hitbox[1] + man2.hitbox[3]  > active[0].y - active[0].radius and man2.hitbox[1] <active[0].y + active[0].radius:
                        active[0].impact(man2)
                        active.pop(0)
            if len(enemylist) > 0:
                for enemy in enemylist:
                    pygame.draw.rect(win, (255, 0, 0), enemy.hitbox, 3)
                    pygame.display.update()
                    if enemy.visible == True:
                        for bullet in bullets2:
                            if len(enemylist) > 0:
                                if bullet.y < enemy.y + enemy.height and bullet.y + bullet.radius > enemy.y:
                                    if bullet.x - bullet.radius < (enemy.hitbox[0]) + (
                                    enemy.hitbox[2]) and bullet.x + bullet.radius > enemy.hitbox[0]:
                                        enemy.hit(man.power)
                                        man2.hitscore += 10
                                        bullets2.pop(bullets2.index(bullet))
                            if bullet.x < 500 and bullet.x > 0:
                                bullet.x += bullet.vel
                            else:
                                bullets2.pop(bullets2.index(bullet))

                        if enemy.visible == True:

                            if man2.hitbox[0] + man2.hitbox[2] > enemy.hitbox[0] and man2.hitbox[0] < (enemy.hitbox[0]) + (enemy.hitbox[2]):
                                if man2.hitbox[1] + man2.hitbox[3] > enemy.hitbox[1] and man2.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3]:
                                    man2.coll(enemy.power)

            if keys[pygame.K_SPACE] and man2.shootLoop == 0:
                bulletSound.play()
                if man2.left:
                    projectile.facing = -1
                else:
                    projectile.facing = 1
                if len(bullets2) < man2.ammo:
                    bullets2.append(projectile(win, (200, 0, 200), round(man2.x + man2.width // 2), round(man2.y + man2.height // 2), 5, projectile.facing))
                man2.shootLoop = 1

            if keys[pygame.K_a] and man2.x > man.vel:
                man2.x -= man2.vel
                man2.left = True
                man2.right = False
                man2.standing = False

            elif keys[pygame.K_d] and man2.x < window_width - man2.width - man2.vel:
                man2.x += man2.vel
                man2.right = True
                man2.left = False
                man2.standing = False

            else:  # reset when no input
                man2.walkcount = 0

            if not (man2.isjump):
                if keys[pygame.K_w]:
                    man2.isjump = True
                    man2.right = False
                    man2.Left = False
                    man2.walkcount = 0
            else:
                if man2.jumpcount >= - man2.fixedjumpcount:  # jump action
                    neg = 1
                    if man2.jumpcount < 0:
                        neg = -1
                    man2.y -= (man2.jumpcount ** 2) * 0.5 * neg
                    man2.jumpcount -= 1

                else:  # when jump finished
                    man2.isjump = False
                    man2.jumpcount = man2.fixedjumpcount

    redrawgamewindow()

pygame.quit()
