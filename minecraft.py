import pygame, sys, random
from pygame.locals import *

# constants representing colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED = ( 255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
BROWN = ( 153, 76, 0)
GREY = ( 255, 0, 255)

# cloud positions
cloudx = -200
cloudy = 0

# constants representing the different resources
DIRT = 0
GRASS = 1
WATER = 2
COAL = 3
WOOD = 4
FIRE = 5
SAND = 6
GLASS = 7
ROCK = 8
STONE = 9
BRICK = 10
DIAMOND = 11
LAVA = 12
CLOUD = 13

# game dimensions
TILESIZE = 20
MAPWIDTH = 30
MAPHEIGHT = 20

# dictionary linking resources to colors
colors =    {
                DIRT    : BROWN,
                GRASS   : GREEN,
                WATER   : BLUE,
                COAL    : BLACK,
                ROCK    : GREY,
                LAVA    : RED
            }

# dictionary linking resources to images
textures = {
                DIRT    : pygame.image.load('images/dirt.png'),
                GRASS   : pygame.image.load('images/grass.png'),
                WATER   : pygame.image.load('images/water.png'),
                COAL    : pygame.image.load('images/coal.png'),
                ROCK    : pygame.image.load('images/dirt.png'),
                SAND    : pygame.image.load('images/dirt.png'),
                DIAMOND : pygame.image.load('images/dirt.png'),
                CLOUD   : pygame.image.load('images/cloud.png')
            }

# dictionary linking resources to bag of goods
inventory = {
                DIRT    : 0,
                GRASS   : 20,
                WATER   : 20,
                COAL    : 0,
                WOOD    : 0,
                FIRE    : 0,
                SAND    : 0,
                GLASS   : 0,
                ROCK    : 10,
                STONE   : 0,
                BRICK   : 0,
                DIAMOND : 0
            }

# dictionary linking resources to controls
controls = {
                DIRT    : 49,
                GRASS   : 50,
                WATER   : 51,
                COAL    : 52,
                WOOD    : 53,
                FIRE    : 54,
                SAND    : 55,
                GLASS   : 56,
                ROCK    : 57,
                STONE   : 48,
                BRICK   : 45,
                DIAMOND : 61
            }

# dictionary linking resources to crafts
craft =     {
                FIRE    : { WOOD : 2, ROCK : 2 },
                STONE   : { ROCK : 2 },
                GLASS   : { FIRE : 1, SAND : 2 },
                DIAMOND : { WOOD : 2, COAL : 3 },
                BRICK   : { ROCK : 2, FIRE : 1 },
                SAND    : { ROCK : 2 }
            }

class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x = 0
    change_y = 0
    walls = None

    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # TODO: insert player sprite
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        # Pass in the top-left corner location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, x, y):
        """ Change the speed of the Player """
        self.change_x += x
        self.change_y += y

    def update(self):
        """ """
        # Move left/right
        self.rect.x += self.change_x

        # Check for sprite collision
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            #
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            #
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

#player = Player(50, 50)
#player.walls = wall_list

all_sprite_list = pygame.sprite.Group()
#all_sprite_list.add(player)

class Wall(pygame.sprite.Sprite):
    """ Wall """
    def __init__(self, x, y, width, height):
        """ Constructor """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        # Make our top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

wall_list = pygame.sprite.Group()

wall = Wall(0, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 0, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 200, 100, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

def main():
    random.seed()
    pygame.init()

def load_image(file_name, colorkey=None):
    full_name = os.path.join('data', file_name)

    try:
        image = pygame.image.load(full_name)
    except pygame.error, message:
        print 'Cannot Load Image: ', full_name
        raise SystemExit, message

    image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_color(colorkey, RLEACCEL)

    return image, image.get_rect()

def load_sound(name):
    class No_Sound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return No_Sound()

    fullname = os.path.join('data', name)
    # if os.path.exists(full_name)


resources = [DIRT,GRASS,WATER,COAL,SAND,ROCK,DIAMOND]
#resources = [DIRT,GRASS,WATER,COAL,WOOD,FIRE,SAND,GLASS,ROCK,STONE,BRICK,DIAMOND]

# creating base map
tilemap = [ [random.choice(resources) for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ]

PLAYER = pygame.image.load('images/player.png')
playerPos = [1,1]

ENEMY = pygame.image.load('images/player.png')
enemyPos = [25,25]

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + 50))
#DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + 50), FULLSCREEN)


#INVFONT = pygame.font.SysFont("comicsansms",15)
INVFONT = pygame.font.Font("freesansbold.ttf", 18)
pygame.display.set_caption('M I N E C R A F T -- 2 D')
pygame.mouse.set_visible(False)
pygame.display.set_icon(pygame.image.load('images/player.png'))

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

probs =     {
                DIRT    : 10,
                GRASS   : 30,
                WATER   : 20,
                COAL    : 5,
                WOOD    : 20,
                SAND    : 5,
                ROCK    : 5,
                DIAMOND : 1
            }

# finish tile map
probsTotal = 0
for test in probs:
    probsTotal += test
print(probsTotal)

for rw in range(MAPHEIGHT):
    for cl in range(MAPWIDTH):
        randomNumber = random.randint(0,probsTotal)
        currentProb = 0
        loopControl = 0
        for i in probs:
            if randomNumber == currentProb:
                tile = probs[i]
            currentProb += i
            loopControl += 1
            tile = DIRT
        tilemap[rw][cl] = tile

        if randomNumber == 0:
            tile = COAL
        elif randomNumber == 1 or randomNumber == 2:
            tile = WATER
        elif randomNumber >= 3 and randomNumber <= 7:
            tile = GRASS
        elif randomNumber >= 8 and randomNumber <= 10:
            tile = SAND
        elif randomNumber >= 11 and randomNumber <= 13:
            tile = ROCK
        elif randomNumber >= 14 and randomNumber <= 15:
            tile = DIAMOND
        else:
            tile = DIRT
        tilemap[rw][cl] = tile

# DISPLAYSURF.fill(WHITE)
# pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0,106)))
# pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
# pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
# pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)
# pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)
# pygame.draw.ellipse(DISPLAYSURF, RED, (300, 250, 40, 80), 1)
# pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

# pixObj = pygame.PixelArray(DISPLAYSURF)
# pixObj[480][380] = BLACK
# pixObj[482][382] = BLACK
# pixObj[484][384] = BLACK
# pixObj[486][386] = BLACK
# pixObj[488][388] = BLACK
# del pixObj
#
# catImg = pygame.image.load('cat.png')
# catx = 10
# caty = 10
# direction = 'right'
#
# fontObj = pygame.font.Font('freesansbold.ttf', 32)
# textSurfaceObj = fontObj.render('Hello world!', True, GREEN, BLUE)
# textRectObj = textSurfaceObj.get_rect()
# textRectObj.center = (200, 150)

while True: #main game loop

    # Clear the screen
    DISPLAYSURF.fill(BLACK)

    for event in pygame.event.get():
        #print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if (event.key == K_RIGHT) and playerPos[0] < MAPWIDTH - 1:
                playerPos[0] += 1
            elif (event.key == K_LEFT) and playerPos[0] > 0:
                playerPos[0] -= 1
            elif (event.key == K_UP) and playerPos[1] > 0:
                playerPos[1] -= 1
            elif (event.key == K_DOWN) and playerPos[1] < MAPHEIGHT - 1:
                playerPos[1] += 1
            elif event.key == K_SPACE:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                inventory[currentTile] += 1
                tilemap[playerPos[1]][playerPos[0]] = DIRT
                print(inventory)
            # place dirt
            for key in controls:
                if (event.key == controls[key]):
                    if pygame.mouse.get_pressed()[0]:
                        if key in craft:
                            canBeMade = True
                            for i in craft[key]:
                                if craft[key][i] > inventory[i]:
                                    canBeMade = False
                                    break

                            if canBeMade == True:
                                for i in craft[key]:
                                    inventory[i] -= craft[key][i]
                                inventory[key] += 1

                    else:
                        currentTile = tilemap[playerPos[1]][playerPos[0]]
                        if inventory[key] > 0:
                            inventory[key] -= 1
                            inventory[currentTile] += 1
                            tilemap[playerPos[1]][playerPos[0]] = key
        # else:
            #print(event)

    if (playerPos[0] > enemyPos[0]):
        enemyPos[0] += 1
    elif (playerPos[0] < enemyPos[0]):
        enemyPos[0] -= 1
    if (playerPos[1] > enemyPos[1]):
        enemyPos[1] += 1
    elif (playerPos[1] < enemyPos[1]):
        enemyPos[1] -= 1

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            # pygame.draw.rect(DISPLAYSURF, colors[tilemap[row][column]], (column*TILESIZE,row*TILESIZE, TILESIZE, TILESIZE))
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))

    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))
    DISPLAYSURF.blit(ENEMY,(enemyPos[0]*TILESIZE,enemyPos[1]*TILESIZE))


    placePositionInv = 10
    for item in resources:
        DISPLAYSURF.blit(textures[item],(placePositionInv,MAPHEIGHT*TILESIZE+20))
        placePositionInv += 45
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePositionInv,MAPHEIGHT*TILESIZE+20))
        placePositionInv += 50

    # Add more clouds
    DISPLAYSURF.blit(textures[CLOUD],(cloudx,cloudy));
    cloudx += 1

    if cloudx > MAPWIDTH*TILESIZE:
        cloudy = random.randint(0,MAPHEIGHT*TILESIZE)
        cloudx = -200

    pygame.display.update()
    fpsClock.tick(FPS)

#if __name__ == '__main__': main()
