import pygame
from math import floor, sin, cos, pi
from spritesheet import SpriteSheet
from sprites import Sprites
from minimap import Minimap
import constants as c
import pickle


class Game:
    
    def __init__(self):
        # X and Y start position
        self.posX = 3.0
        self.posY = 10.0 
        # Initial direction vector
        self.dirX = -1.0
        self.dirY = 0.0 
        # The 2d raycaster version of camera plane
        self.planeX = 0.0
        self.planeY = 0.66
        self.textures = []
        self.sprites = []
        # Generate some textures
        self.textures.append(SpriteSheet("assets/eagle.png")) #1
        self.textures.append(SpriteSheet("assets/redbrick.png")) #2
        self.textures.append(SpriteSheet("assets/purplestone.png")) #3
        self.textures.append(SpriteSheet("assets/greystone.png")) #4
        self.textures.append(SpriteSheet("assets/bluestone.png")) #5
        self.textures.append(SpriteSheet("assets/mossy.png")) #6
        self.textures.append(SpriteSheet("assets/wood.png")) #7
        self.textures.append(SpriteSheet("assets/colorstone.png")) #8

        self.projectile_image = pygame.image.load("assets/projectile.png").convert_alpha()
        self.player_image = pygame.image.load("assets/player.png").convert_alpha()
        self.floor_img = pygame.image.load("assets/floor.png").convert()
        self.minimap = Minimap(5)
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        self.time = 0 # time of current frame
        self.oldTime = 0 #time of previous frame
        self.frameTime = 0.0
        self.players = {}
        self.sprites.append(Sprites(1.5, 1.5, 0, 0, self.player_image))
        self.my_id = -1
        self.shoot = False
        self.is_connected = False
        self.done = False
        self.game_map = c.game_map

    def input_handle(self):
        events = pygame.event.get()

        # speed modifiers
        moveSpeed = self.frameTime * 5.0 # The constant value is in squares/second
        rotSpeed = self.frameTime * 3.0 # The constant value is in radians/second

        key = pygame.key.get_pressed()
        # Move forward if no wall in front of you
        if key[pygame.K_w]:
            if(self.game_map[int(self.posX + self.dirX * moveSpeed)][int(self.posY)] == False):
                self.posX += self.dirX * moveSpeed
            if(self.game_map[int(self.posX)][int(self.posY + self.dirY * moveSpeed)] == False):
                self.posY += self.dirY * moveSpeed

        # Move backwards if no wall behind you
        if key[pygame.K_s]:
            if(self.game_map[int(self.posX - self.dirX * moveSpeed)][int(self.posY)] == False):
                self.posX -= self.dirX * moveSpeed
            if(self.game_map[int(self.posX)][int(self.posY - self.dirY * moveSpeed)] == False):
                self.posY -= self.dirY * moveSpeed
        
        if key[pygame.K_d]:
            oldDirX = self.dirX
            self.dirX = self.dirX * cos(-pi/2) - self.dirY * sin(-pi/2)
            self.dirY = oldDirX * sin(-pi/2) + self.dirY * cos(-pi/2)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * cos(-pi/2) - self.planeY * sin(-pi/2)
            self.planeY = oldPlaneX * sin(-pi/2) + self.planeY * cos(-pi/2)

            self.posX += self.dirX * (moveSpeed/2)
            self.posY += self.dirY * (moveSpeed/2)

            oldDirX = self.dirX
            self.dirX = self.dirX * cos(pi/2) - self.dirY * sin(pi/2)
            self.dirY = oldDirX * sin(pi/2) + self.dirY * cos(pi/2)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * cos(pi/2) - self.planeY * sin(pi/2)
            self.planeY = oldPlaneX * sin(pi/2) + self.planeY * cos(pi/2)
        
        if key[pygame.K_a]:
            oldDirX = self.dirX
            self.dirX = self.dirX * cos(-pi/2) - self.dirY * sin(-pi/2)
            self.dirY = oldDirX * sin(-pi/2) + self.dirY * cos(-pi/2)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * cos(-pi/2) - self.planeY * sin(-pi/2)
            self.planeY = oldPlaneX * sin(-pi/2) + self.planeY * cos(-pi/2)

            self.posX -= self.dirX * (moveSpeed/2)
            self.posY -= self.dirY * (moveSpeed/2)

            oldDirX = self.dirX
            self.dirX = self.dirX * cos(pi/2) - self.dirY * sin(pi/2)
            self.dirY = oldDirX * sin(pi/2) + self.dirY * cos(pi/2)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * cos(pi/2) - self.planeY * sin(pi/2)
            self.planeY = oldPlaneX * sin(pi/2) + self.planeY * cos(pi/2)

        # Rotate to the right
        if key[pygame.K_RIGHT]:
            # Both camera direction and camera plane must be rotated
            oldDirX = self.dirX
            self.dirX = self.dirX * cos(-rotSpeed) - self.dirY * sin(-rotSpeed)
            self.dirY = oldDirX * sin(-rotSpeed) + self.dirY * cos(-rotSpeed)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * cos(-rotSpeed) - self.planeY * sin(-rotSpeed)
            self.planeY = oldPlaneX * sin(-rotSpeed) + self.planeY * cos(-rotSpeed)

        # Rotate to the left
        if key[pygame.K_LEFT]:
            # Both camera direction and camera plane must be rotated
            oldDirX = self.dirX
            self.dirX = self.dirX * cos(rotSpeed) - self.dirY * sin(rotSpeed)
            self.dirY = oldDirX * sin(rotSpeed) + self.dirY * cos(rotSpeed)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * cos(rotSpeed) - self.planeY * sin(rotSpeed)
            self.planeY = oldPlaneX * sin(rotSpeed) + self.planeY * cos(rotSpeed)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if key[pygame.K_SPACE]:
                    self.shoot = True
                    #self.sprites.append(Sprites(self.posX, self.posY, self.dirX, self.dirY, self.projectile_image))
            if event.type == pygame.QUIT:
                self.done = True  
                pygame.quit()
        
        if key[pygame.K_ESCAPE]:
            self.done = True
            pygame.quit()
    

    def cast_sprites(self, data_sprites, screen):
        # SPRITE CASTING
        # TODO: Sort sprites from far to close
        #if type(data_sprites) is dict:
        sprites = []
        for key, value in data_sprites.items():
            # If it`s a list it means we are dealing with sprites list, not players
            if type(value) is list:
                for sprite in value:
                    sprites.append(sprite)
            else:
                if not (int(key) == self.my_id and value.is_player):
                    sprites.append(value)

        # After sorting the sprites, do the projection and draw them
        for sprite in sprites:
            # Translate sprite position to relative to camera
            spriteX = sprite.x - self.posX
            spriteY = sprite.y - self.posY

            # Transform sprite with the inverse camera matrix
            # [ planeX   dirX ] -1                                       [ dirY      -dirX ]
            # [               ]       =  1/(planeX*dirY-dirX*planeY) *   [                 ]
            # [ planeY   dirY ]                                          [ -planeY  planeX ]

            invDet = 1.0 / (self.planeX * self.dirY - self.dirX * self.planeY) # Required for correct matrix multiplication

            transformX = invDet * (self.dirY * spriteX - self.dirX * spriteY)
            transformY = invDet * (-self.planeY * spriteX + self.planeX * spriteY) # This is actually the depth inside the screen, that what Z is in 3D, the distance of sprite to player, matching sqrt(spriteDistance[i])

            if transformY == 0:
                transformY = 0.001
            spriteScreenX = int((c.SCREEN_WIDTH / 2) * (1 + transformX / transformY))

            # Parameters for scaling and moving the sprites
            uDiv = 10
            vDiv = 10
            if sprite.uDiv > 0:
                uDiv = sprite.uDiv
            if sprite.vDiv > 0:
                vDiv = sprite.vDiv
            vMove = 60.0
            vMoveScreen = int(vMove / transformY)

            # Calculate height of the sprite on screen
            spriteHeight = abs(int(c.SCREEN_HEIGHT / (transformY))) / vDiv # Using "transformY" instead of the real distance prevents fisheye
            # Calculate lowest and highest pixel to fill in current stripe
            drawStartY = -spriteHeight / 2 + c.SCREEN_HEIGHT / 2 + vMoveScreen
            if drawStartY < 0:
                drawStartY = 0
            drawEndY = spriteHeight / 2 + c.SCREEN_HEIGHT / 2 + vMoveScreen
            if drawEndY >= c.SCREEN_HEIGHT:
                drawEndY = c.SCREEN_HEIGHT - 1

            # Calculate width of the sprite
            spriteWidth = abs( int (c.SCREEN_HEIGHT / (transformY))) / uDiv
            drawStartX = -spriteWidth / 2 + spriteScreenX
            drawEndX = spriteWidth / 2 + spriteScreenX
            if drawEndX >= c.SCREEN_WIDTH:
                drawEndX = c.SCREEN_WIDTH - 1
            if transformY > 0 and drawStartX >= 0 and drawEndX < c.SCREEN_WIDTH:
                if spriteWidth > 9000:
                    spriteWidth = 9000
                if spriteHeight > 9000:
                    spriteHeight = 9000
                tmp_image = pygame.transform.scale(sprite.image, (int(spriteWidth), int(spriteHeight)))
                # Darken sprites that are far from the player
                darken_percent = (1 - (spriteHeight*30/c.SCREEN_HEIGHT))
                dark = pygame.Surface(tmp_image.get_size(), pygame.SRCALPHA).convert_alpha()
                darkness = (darken_percent*255)
                if darkness > 255:
                    darkness = 255
                elif darkness < 0:
                    darkness = 0
                dark.blit(tmp_image, (0 , 0))
                dark.fill((darkness, darkness, darkness, 0), None, pygame.BLEND_RGBA_SUB)
                #print("drawx: {} drawy: {}".format(drawStartX, drawStartY))
                screen.blit(dark, (drawStartX , drawStartY))
            if not self.is_connected:
                sprite.move()
                if self.game_map[int(sprite.x)][int(sprite.y)]:
                    self.sprites.remove(sprite)

    def draw(self, screen):
        pygame.draw.rect(screen, c.BLACK, (0, 0, c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))
        floor_size = self.floor_img.get_size()
        if floor_size[0] != c.SCREEN_WIDTH or floor_size[1] != c.SCREEN_HEIGHT//2:
            self.floor_img = pygame.transform.scale(self.floor_img, (c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))
            self.floor_img.convert()
        screen.blit(self.floor_img, (0, c.SCREEN_HEIGHT//2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT//2))

        for x in range(0, c.SCREEN_WIDTH):

            # Calculate ray position and direction
            cameraX = 2 * x / c.SCREEN_WIDTH - 1 # x-coordinate in camera space
            rayDirX = self.dirX + self.planeX*cameraX
            rayDirY = self.dirY + self.planeY*cameraX

            # Which box of the map we're in
            mapX = int(self.posX)
            mapY = int(self.posY)

            # Length of ray from current position to next x or y-side
            sideDistX = 0.0
            sideDistY = 0.0

            # Length of ray from one x or y-side to next x or y-side
            if rayDirX == 0:
                rayDirX = 0.001
            if rayDirY == 0:
                rayDirY = 0.001
            
            deltaDistX = abs(1 / rayDirX)
            deltaDistY = abs(1 / rayDirY)
            perpWallDist = 0.0

            # What direction to step in x or y-direction (either +1 or -1)
            stepX = -1
            stepY = -1

            hit = 0 # was there a wall hit?
            side = 0 # was a NS or a EW wall hit?

            # Calculate step and initial sideDist
            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.posX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - self.posX) * deltaDistX
            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.posY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - self.posY) * deltaDistY

            # Perform DDA
            while hit == 0:
                # jump to next map square, OR in x-direction, OR in y-direction
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                # Check if ray has hit a wall
                if(self.game_map[mapX][mapY] > 0): 
                    hit = 1

            # Calculate distance of perpendicular ray (Euclidean distance will give fisheye effect!)
            if side == 0:
                perpWallDist = (mapX - self.posX + (1 - stepX) / 2) / rayDirX
            else:
                perpWallDist = (mapY - self.posY + (1 - stepY) / 2) / rayDirY

            # Calculate height of line to draw on screen
            lineHeight = int(c.SCREEN_HEIGHT / perpWallDist)
            if lineHeight > 10*c.SCREEN_HEIGHT:
                lineHeight = 10*c.SCREEN_HEIGHT

            # Calculate lowest and highest pixel to fill in current stripe
            drawStart = -lineHeight / 2 + c.SCREEN_HEIGHT / 2
            if drawStart < 0:
                drawStart = 0
            drawEnd = lineHeight / 2 + c.SCREEN_HEIGHT / 2
            if drawEnd >= c.SCREEN_HEIGHT:
                drawEnd = c.SCREEN_HEIGHT - 1

            # Texturing calculations
            texNum = self.game_map[mapX][mapY] - 1  # 1 subtracted from it so that texture 0 can be used!

            # Calculate value of wallX
            wallX = 0.0 # Where exactly the wall was hit
            if side == 0:
                wallX = self.posY + perpWallDist * rayDirY
            else:
                wallX = self.posX + perpWallDist * rayDirX
            wallX -= floor((wallX))

            # X coordinate on the texture
            texX = int(wallX * c.TEX_WIDTH)
            if(side == 0 and rayDirX > 0):
                texX = c.TEX_WIDTH - texX - 1
            if(side == 1 and rayDirY < 0):
                texX = c.TEX_WIDTH - texX - 1

            # TODO: an integer-only bresenham or DDA like algorithm could make the texture coordinate stepping faster
            # How much to increase the texture coordinate per screen pixel
            step = 1.0 * c.TEX_HEIGHT / lineHeight
            # Starting texture coordinate
            texPos = (drawStart - c.SCREEN_HEIGHT / 2 + lineHeight / 2) * step

            image1 = self.textures[texNum].get_image(int(round(texX)), 0, 1, 64 )
            image2 = pygame.transform.scale(image1, (1, lineHeight))
            darken_percent = (1 - (lineHeight*5/c.SCREEN_HEIGHT))
            dark = pygame.Surface(image2.get_size()).convert_alpha()
            darkness = (darken_percent*255)
            if darkness > 255:
                darkness = 255
            elif darkness < 0:
                darkness = 0
            dark.fill((0, 0, 0, darkness))

            screen.blit(image2, ((x * 1), c.SCREEN_HEIGHT // 2 - lineHeight // 2))
            screen.blit(dark, ((x * 1), c.SCREEN_HEIGHT // 2 - lineHeight // 2))

        # Cast Sprites and Players:
        self.cast_sprites(self.sprites, screen)
        self.cast_sprites(self.players, screen)
        

        # Draw Minimap
        self.minimap.draw(screen, self.game_map, self.posX, self.posY, self.sprites)

        # Timing for input and FPS counter
        self.oldTime = self.time
        self.time = pygame.time.get_ticks()
        self.frameTime = (self.time - self.oldTime) / 1000.0 # Frametime is the time this frame has taken, in seconds
        fps = 1.0 / self.frameTime
        text = self.font.render("FPS: {:.2f}".format(fps), True, c.WHITE)
        screen.blit(text, (10, 10))

    