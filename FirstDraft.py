import sys
import os
import time
import pygame as pg

class Singleton():
    def __init__ (self):
        self.colours = {"BLACK": (0,0,0), 
                        "WHITE": (255,255,255),
                        "ROAD": (0,0,0),
                        "DIRT": (139,69,19),
                        "SAND": (218,165,32),
                        "MUD":  (139,69,19),
                        "WATER": (0,191,255),
                        "ROCK": (47,79,79),
                        "RED": (255,0,0),}

        self.terrain_colour = ("ROAD","DIRT",2,3,4,5,6,7,8,"ROCK")

        self. direction = ( (1,0,180),
                            (1,-1,135),
                            (0,-1,90),
                            (-1,-1,45),
                            (-1,0,0),
                            (-1,1,315),
                            (0,1,270),
                            (1,1,225))

        self.current_path = os.path.dirname(__file__) # Where your .py file is located
        self.resource_path = os.path.join(self.current_path, 'resources') # The resource folder path
        self.image_path = os.path.join(self.resource_path, 'images') # The image folder path

        
        
        self. images = {    "Yellow_Car": "y_car.png",
                            "Petrol_Station": "petrol.png",
                            "Left_Pedal": "arrowleft.png",
                            "Right_Pedal": "arrowright.png",
                            "Gas_Pedal": "arrowforward.png"}

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
        pg.init()
        info = pg.display.Info()
        windowWidth = info.current_w-150
        windowHeight = info.current_h-100
        
        


        #set screen size (across, down)
        self.screen_dim = (900,600)
        self.screen = pg.display.set_mode(self.screen_dim)
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

        self.start = [7,1]
        self.goal = [7,9]
        return
    
    def checkstash(self,position):
        stash = -1
        for i in range (len (self.stashes)):
            if position[0]==self.stashes[i][1][0] and position[1]==self.stashes[i][1][1]:
                stash = i
        return stash

class Car ():

    def __init__ (self,attributes={"Fuel":{"Capacity":10.0,"Level":8.0,"Economy":1.0,"Factors":[1.0,1.5]}},pose=[1,7,4]):
        
        self.attributes = attributes

        #pose [row, col , direction row 1 d -1 u, direction]
        self.pose = pose
        
    def add_attribute (self,  attribute="Fuel", volume = 1):
        taken = 0.0
        start_level = self.attributes [attribute]["Level"]
        level = self.attributes [attribute]["Level"]
        capacity = self.attributes [attribute]["Capacity"]
        level = level  + volume
        if level  > capacity:
            level = capacity
            print (attribue," Stoarge Full", level )
        else:
        
            print (attribute," Stoarge is",int(level/capacity*100),"% full.  With", level )
        taken = level - start_level
        self.attributes [attribute]["Level"] = level
        return taken

    def drive (self, terrain):
        distance = 0
        direction_factor = 1.0
        if terrain == 9:
            return (distance)
        if (self.pose[2] in (1,3,5,7)):
            direction_factor = 1.41
        

        for attribute in self.attributes: 
            level = self.attributes [attribute]["Level"]
            economy = self.attributes [attribute]["Economy"]
            factors = self.attributes [attribute]["Factors"]
            capacity = self.attributes [attribute]["Capacity"]
            level = level - economy*factors[terrain]*direction_factor
            if level<0:
                level = 0
                self.attributes [attribute]["Level"] = level
                print ("Out of ",attribute)
                return (distance)
            else: 
                distance = 1
                self.pose[0] = self.pose[0] + g.direction [self.pose[2]][1]
                self.pose[1] = self.pose[1] + g.direction [self.pose[2]][0]
                self.attributes [attribute]["Level"] = level
                print ("Storage is ",int(level/capacity*100),"% full.  With", level)

        return (distance)

    def turn  (self, way):
        if way == "r":
            temp_direction = self.pose[2] + 1
            if temp_direction == 8:
                temp_direction = 0
            
        if way == "l":
            temp_direction = self.pose[2] - 1
            if temp_direction == -1:
                temp_direction = 7

        self.pose[2] = temp_direction

        return

class Piece ():

    def __init__(self, position=(50, 50), size=20, image="Yellow_Car",angle=0):
        
        
        self.size = size
        self.original_image = pg.image.load(os.path.join(g.image_path, g.images[image]))
        self.rescale()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.angle = angle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.print()
        
    def update(self,position, dir=0,image = "No Change"):
        
        if image != "No Change":
            self.original_image = pg.image.load(g.images[image])
            self.rescale()
            self.rect = self.image.get_rect()
        self.rect.centerx=position[0]
        self.rect.centery=position[1]
        self.angle  = g.direction [dir][2]
        self.image = pg.transform.rotate(self.original_image, self.angle)
          # Value will reapeat after 359. This prevents angle to overflow.
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.
        self.print()
        return

    def rescale(self):
        image_width =  self.original_image.get_width()
        image_height =  self.original_image.get_height()
        iscaleh = int(self.size*0.95)
        iscalew = int(iscaleh/image_height*image_width)  
        self.original_image = pg.transform.scale(self.original_image,(iscalew,iscaleh))
        self.image = self.original_image
        return

    def print(self):
        g.screen.blit(self.image, self.rect)
        return

class Board():
    def __init__ (self, world_size = (10,10), terrain =[]):
        
        self.terrain=terrain
        self.screen_size = g.screen_dim
        self.header = self.screen_size[0] - self.screen_size[1]
        self.screen_height = self.screen_size[1]
        self.world_size = world_size
        self.border = self.screen_height * 0.05
        self.square_size = (self.screen_height-self.border*2)/self.world_size[0]
        self.print()
        return

    def print (self):

        #Loop through columns then row
        for r in range (self.world_size[0]):
            for c in range (self.world_size[1]):
                
                

                #calc position for square
                rec_d =  self.border +r * self.square_size 
                rec_a =  self.border +  c * self.square_size
                
                #define rectangle for sqaure
                square_rect = pg.Rect( rec_a,rec_d, self.square_size, self.square_size)
                #get index type of terrain
                colour_index = self.terrain[r][c]
                #get square type from index
                square_type = g.terrain_colour [colour_index]
                #get colour from the sqaure type
                square_colour = g.colours[square_type]
                #draw square to canvas
                pg.draw.rect(g.screen,square_colour,square_rect)

        return

class Guage():
    def __init__(self, name="Test",size=[80,20], position =(60,600) ,value = 10, maxm = 20 ):
       
        self.size=size
        self.top = position [0]
        self.left = position [1]
        self.width = size[0] 
        self.height =  size[1]
        self.value = value
        self.max = maxm
        self.main = pg.Rect(self.left,self.top,self.width,self.height)
        self.red = pg.Rect(self.left,self.top,self.width*0.1,self.height)
        self.name = name   
        fontsize =int(self.height)
        self.thickness=3     
        self.font = pg.font.Font(None, fontsize) 
        self.print()
        return   
    
    def update (self, value, max):
        
        self.value = value
        self.max= max
        self.print()      
        return



    def print(self):
        self.needle_across = self.value/self.max* self.width
        
        self.text = self.font.render(self.name, True, g.colours["WHITE"]) 
        self.textRect = self.text.get_rect() 
        self.textRect.top =self.top-self.textRect.height*1.05
        self.textRect.left =self.left
        g.screen.blit(self.text,self.textRect)
        
        self.text_max = self.font.render(str(self.max), True,g.colours["WHITE"]) 
        self.textRect_max = self.text.get_rect() 
        self.textRect_max.centery =self.top+self.height/2
        self.textRect_max.left =self.left+self.width*1.05
        g.screen.blit(self.text_max,self.textRect_max)

        pg.draw.rect(g.screen,g.colours["WHITE"],self.main)
        pg.draw.rect(g.screen,g.colours["RED"],self.red)     
        pg.draw.line(g.screen,g.colours["BLACK"],(self.needle_across+self.left,self.top),(self.needle_across+self.left,self.top+self.height),self.thickness)

        return





class GameControl():
    def __init__ (self):
        
        
        #initiate objects
        
        
        self.car = Car({"Fuel":{"Capacity":10.0,"Level":8.0,"Economy":1.0,"Factors":[1.0,1.5]}},[7,1,0])
        self.world = World()

        #self.stash = []
        #for i in range (world.stashes):
        #    self.stash.append( (world.stashes[i]))

        
        #initiate board
        self.board = Board (self.world.size,self.world.terrain)

        #set up car graphics
        car_size = self.board.square_size
        
        car_centre = self.calc_centre([self.car.pose[0],self.car.pose[1]])

        angle = g.direction[self.car.pose[2]][2]
        self.g_player = Piece(car_centre, car_size,"Yellow_Car",angle)   
        count = 0
        
        
        #graphics for guages set up
        
        self.guages =[]

        for attribute in self.car.attributes:
            name= attribute
            value = self.car.attributes [attribute]["Level"]
            maxm = self.car.attributes [attribute]["Capacity"]
            height = g.screen_dim[1]/15
            width = g.screen_dim [0] - (self.world.size [1] * self.board.square_size - self.board.border*2)*1.4
            across =  (self.world.size [1] * self.board.square_size + self.board.border*1.5)            
            down = (count * height) * 1.2+self.board.border+self.board.square_size
            size=[width,height] 
            position =(down,across) 
            count = count + 1
        
            self.guages.append(Guage(name, size, position, value, maxm))

        #set up graphics for stashes
        self.g_stash = []
        for i in range (len (self.world.stashes)):
            stash_position = [self.world.stashes[i][1][1],self.world.stashes[i][1][0]]  
            centre = self.calc_centre(stash_position)
            self.g_stash.append(Piece(centre,self.board.square_size,self.world.stashes[i][0]))
    
      
        #Graphics for controls

        pedal_size = g.screen_dim[1]/10
        direction_down = g.screen_dim[1] - pedal_size*2  -self.board.border
        left_across = across =  (self.world.size [1] * self.board.square_size + self.board.border*1.5)  + pedal_size 
        right_across =across =  (self.world.size [1] * self.board.square_size + self.board.border*1.5) + pedal_size * 2 
        gas_down = direction_down + pedal_size * 1.1
        gas_across = (left_across + right_across)/2
        self.g_left = Piece((left_across,direction_down), pedal_size, "Left_Pedal", 0)
        self.g_right = Piece((right_across,direction_down), pedal_size, "Right_Pedal", 0)
        self.g_drive = Piece((gas_across,gas_down), pedal_size, "Gas_Pedal", 0)

        #Display canvas
        pg.display.flip()

        self.run()
      
        
    def run (self):
        running = True
        while (running):

            for event in pg.event.get():
                
                #manage quit
                if event.type == pg.QUIT:
                   
                    running = False
                #in press mouse check if on a pedal movement    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    if self.g_drive.rect.collidepoint(mousex, mousey):
                        print('clicked on drive')
                        car_across = self.car.pose[0]
                        car_down = self.car.pose[1]
                        terrain = self.world.terrain[car_down][car_across]
                        self.car.drive(terrain)
                        stash = self.world.checkstash([car_across,car_down])
                        if stash>0:
                            attribute = world.stashes[i][0]
                            volume = world.stashes[i][1][2]
                            stash_transfer = self.car.add_attribute (attribute, volume)
                            world.stashes[stash][1][2] = volume - fuel_transfer
                            print ("Fuel stash...",stash_transfer,"used.", world.stashes[stash][1][2],"left.")    
                   

                    elif self.g_left.rect.collidepoint(mousex, mousey):
                        print('clicked on left')
                        self.car.turn("l")
                                                
                       
                    elif self.g_right.rect.collidepoint(mousex, mousey):
                        print('clicked on right')
                        self.car.turn("r")
                    
                    #re-print graphics

                    self.board.print()
                    for g_stash in self.g_stash:
                        g_stash.print()
                    car_centre = self.calc_centre([self.car.pose[0],self.car.pose[1]])
                    car_direction = self.car.pose[2]
                    self.g_player.update(car_centre, car_direction)                  
                    self.g_player.print()

                    #update guages
                    i=0
                    for attribute in self.car.attributes:
                        
                        value = self.car.attributes [attribute]["Level"]
                        maxm = self.car.attributes [attribute]["Capacity"]
                        self.guages[i].update (value, maxm)

                    pg.display.flip()
                    
        pg.QUIT




        
        return

    def calc_centre(self, position):
        rec_d =  self.board.border + position[0] * self.board.square_size + self.board.square_size/2
        rec_a =  self.board.border +  position[1] * self.board.square_size+self.board.square_size/2
        centre = [rec_d,rec_a]
        return centre


g=Singleton()
game=GameControl()




