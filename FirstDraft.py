import sys
import time
import pygame as pg

class Singleton():
    def __init__ (self):
        self.colours = {BLACK: (0,0,0), 
                        WHITE: (255,255,255),
                        ROAD: (0,0,0),
                        DIRT: (139,69,19),
                        SAND: (218,165,32),
                        MUD:  (139,69,19),
                        WATER: (0,191,255),
                        ROCK: (47,79,79),
                        RED: (255,0,0),}

        self.terrain_colour = (ROAD,DIRT,2,3,4,5,6,7,8,ROCK)

        self. direction = ( (1,0,180),
                            (1,-1,135),
                            (0,-1,90),
                            (-1,-1,45),
                            (-1,0,0),
                            (-1,1,315),
                            (0,1,270),
                            (1,1,225))

        self. images = {    "Yellow_Car": "y_car.png",
                            "Petrol_Station": "petrol.png"}


        pg.init()
        info = pg.display.Info()
        windowWidth = info.current_w-150
        windowHeight = info.current_h-100

        self.screen_dim (900,600)
     
        return

class World ():
    def __init__ (self):
        self.size = [10,10]
        self.terrain = [[9,9,9,9,9,9,9,9,9,9],
                        [9,1,1,1,1,1,1,0,1,9],
                        [9,1,1,1,1,0,0,0,1,9],
                        [9,1,1,1,0,1,1,0,1,9],
                        [9,1,1,1,0,1,1,0,1,9],
                        [9,1,1,1,1,0,1,0,1,9],
                        [9,1,1,1,1,0,1,0,1,9],
                        [9,1,1,1,1,1,0,0,1,9],
                        [9,1,1,1,1,1,1,0,1,9],
                        [9,9,9,9,9,9,9,0,9,9]]
        
        self.stashes =   [ ["Petrol_Station",[5,7,3]],
                           ["Petrol_Station",[4,4,10]]]

        self.start = [1,7]
        self.goal = [9,7]
        return
    
    def checkstash(self,position):
        stash = -1
        for i in range (len (self.stash)):
            if position[0]==self.stash[i][1][1] and position[1]==self.stash[i][1][0]:
                stash = i
        return stash

class Piece ():

    def __init__(self, pos=(0, 0), size=20, image="Yellow_Car"):
        
        self.original_image = pg.image.load(images[image])
        self.rescale()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.print()
        
    def update(self,position, dir=0,image = "No Change"):
        
        if image != "No Change":
            self.original_image = pg.image.load(images[image])
            self.rescale()
            self.rect = self.image.get_rect()
        self.rect.centery=position[0]
        self.rect.centerx=position[1]
        self.angle  = g.direction [dir][2]
        self.image = pg.transform.rotate(self.original_image, self.angle)
          # Value will reapeat after 359. This prevents angle to overflow.
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.
        self.print()
        return

    def rescale(self)
        image_width =  self.original_image.get_width()
        image_height =  self.original_image.get_height()
        iscaleh = int(size*0.95)
        iscalew = int(iscaleh/image_height*image_width)  
        self.original_image = pg.transform.scale(self.original_image,(iscalew,iscaleh))
        self.image = self.original_image
        return

    def print(self):
        screen.blit(self.image, self.rect)
        return

class Board():
    def __init__ (self, world_size,screen_dim):
        self.screen_size = screen_dim
        self.header = self.screen_size[0] - self.screen_size[1]
        self.screen_height = self.screen_size[1]
        self.world_size = world_size
        self.border = self.screen_height * 0.05
        self.square_size = (self.screen_height-self.border*2)/self.world_size
        return

    def print (self, terrain,screen):
        for r in range (self.world_size):
            for c in range (self.world_size):
                
                
                rec_d =  self.border +r * self.square_size 
                rec_a =  self.border +  c * self.square_size
                square_rect = pg.Rect( rec_a,rec_d, self.square_size, self.square_size)
                square_colour = COLOURS[terrain[r][c]]
                pg.draw.rect(screen,square_colour,square_rect)

        return

class Guage():
    def __init__(self, name="Test",size=[80,20], position =(60,600) ,value = 10, max = 20 ):
        self.top = position [0]
        self.left = position [1]
        self.width = size[0] 
        self.height =  size[1]
        self.value = value
        self.max = max
        self.main = pg.Rect(self.left,self.top,self.width,self.height)
        self.red = pg.Rect(self.left,self.top,self.width*0.1,self.height)
        
        
        fontsize =self.height
              
        self.font = pg.font.Font(None, fontsize) 
        self.text = self.font.render(name, True, WHITE) 
        self.textRect = self.text.get_rect() 
        self.textRect.top =self.top-self.textRect.height*1.05
        self.textRect.left =self.left
        screen.blit(self.text,self.textRect)

        self.text_max = self.font.render(str(self.max), True, WHITE) 
        self.textRect_max = self.text.get_rect() 
        self.textRect_max.centery =self.top+self.height/2
        self.textRect_max.left =self.left+self.width*1.05
       
        screen.blit(self.text_max,self.textRect_max)

        pg.draw.rect(screen,WHITE,self.main)
        pg.draw.rect(screen,RED,self.red)
        self.needle_across = self.value/self.max* self.width
        self.thickness=3
        pg.draw.line(screen,BLACK,(self.needle_across+self.left,self.top),(self.needle_across+self.left,self.top+self.height),self.thickness)
        return   
    
    def update (self, value, max):
        
        self.value = value

        self.max= max
        self.needle_across = self.value/self.max* self.width
        pg.draw.rect(screen,WHITE,self.main)
        
       
        pg.draw.rect(screen,RED,self.red)
        pg.draw.line(screen,BLACK,(self.needle_across+self.left,self.top),(self.needle_across+self.left,self.top+self.height),self.thickness)
        
        
        self.text_max = self.font.render(str(self.max), True, WHITE) 
              
       
        screen.blit(self.text_max,self.textRect_max)
        
        
        return







 

class GameControl():
    def __init__ (self):
        
        #Get global variable
        
        g = Singleton()

        #initiate objects
        
        
        self.car = Car()
        self.world = World()

        self.stash = []
        for i in range (world.stashes):
            append.stash(Stash (world.stashes[i]))

        #set screen size
        self.screen = pg.display.set_mode(g.screen_dim)
        pg.display.set_caption("Car Wars")

        #initiate board
        self.board = Board (g.board_size,g.screen_dim)

        #set up car graphics
        car_size = self.board.square_size
        self.g_player = Piece(world.start, car_size)   


        self.guage = Guage(attribute[0][0],(car.attribute[0][1],car.attribute[0][2]))

        #set up graphics for stashes
        self.g_stash = []
        for i in range (len (g.stashes)):
            stash_postion = [self.stash[i][1][1],self.stash[i][1][0]]  
            centre = calc_centre(stash_position)
            self.g_stash.append(Piece(centre,board.square_size,world.stashes[i][0]))


    def calc_centre(self, position):
        rec_d =  self.board.border + position[0] * self.board.square_size + self.board.square_size/2
        rec_a =  self.board.border +  position[1] * self.board.square_size+self.board.square_size/2
        centre = [rec_d,rec_a]
        return centre


