import pygame
import random
#------WASD to move------E to Attack------SPACE to Roll------R to Heal------

pygame.init()
FPS=60 #Set FPS
SCREENWIDTH=1280
SCREENHEIGHT=720       
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) #Set Resolution
clock = pygame.time.Clock()
running = True
entities=pygame.sprite.Group()
xoffset=0
yoffset=0
border_image=pygame.transform.scale_by((pygame.image.load('Map\\borders.png')).convert_alpha(),4)
border_rect=border_image.get_bounding_rect()
floor_image=pygame.transform.scale_by((pygame.image.load('Map\\Floor.png')).convert_alpha(),4)

class Animation:
    def __init__(self, anim):
        self.right=anim
        self.left=[pygame.transform.flip(x,True, False) for x in self.right]
        self.length=len(anim)
    def get_img(self, index, direction):
        if direction==1:
            return self.right[index]
        elif direction==-1:
            return self.left[index]
        
class Entity(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x=x
        self.y=y
        self.x_speed=0
        self.y_speed=0
        entities.add(self)
    
    def change_anim(self,new_anim,index,speed):
        self.current_anim=new_anim   #3shan n8ayar el animation
        self.anim_index=index   #3shan el attack mybtdeesh mn el nos
        self.anim_speed=speed   #attack is slow so when we change to attack 5ly el speed asr3

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.skeleton_idle=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\Idle\\Idle_0{i}.png').convert_alpha(), 2.4) for i in range(1,5)])
        self.skeleton_walk=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\Walk\\Walk_0{i}.png').convert_alpha(), 2.4) for i in range(1,5)])
        self.skeleton_attack=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\Attack\\Attack_0{i}.png').convert_alpha(), 2.4) for i in range(1,9)])
        self.skeleton_hit=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\TakeHit\\TakeHit_0{i}.png').convert_alpha(), 2.4) for i in range(1,4)])
        self.skeleton_death=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\Death\\Death_0{i}.png').convert_alpha(), 2.4) for i in range(1,4)])
        self.current_anim=self.skeleton_idle
        self.anim_index=0
        self.anim_speed=0.1
        self.is_attacking=False
        self.speed=8        
        self.direction=1
        self.image=self.current_anim.get_img(self.anim_index,self.direction)
        self.rect=self.image.get_rect()
        self.enemybox_rect=self.image.get_bounding_rect()
    def turn(self):
        pygame.draw.line(screen,'blue',(self.x+150-xoffset,self.y-yoffset),(self.x-150-xoffset,self.y-yoffset))
        pygame.draw.line(screen,'blue',(self.x-xoffset,self.y-150-yoffset),(self.x-xoffset,self.y+150-yoffset))               
        pygame.draw.line(screen,'purple',(player1.x-xoffset,0),(player1.x-xoffset,1080-yoffset))
        pygame.draw.line(screen,'purple',(0,player1.y-yoffset),(1920-xoffset,player1.y-yoffset))
        if not self.is_attacking or (self.is_attacking and self.anim_index<5):
            if player1.x<self.x:
                self.direction=-1
            elif player1.x>self.x:
                self.direction=1     
        if self.x-player1.x<=150 and self.x-player1.x>=-150 and self.y-player1.y<=150 and self.y-player1.y>=-150:
            pygame.draw.line(screen,'red',(self.x-xoffset,self.y-yoffset),(player1.x-xoffset,player1.y-yoffset)) 
            pygame.draw.circle(screen,'red',(self.x-xoffset,self.y-yoffset),150,2)
           
            self.is_attacking=True
        else:
            
            pygame.draw.line(screen,'green',(self.x-xoffset,self.y-yoffset),(player1.x-xoffset,player1.y-yoffset)) 
            pygame.draw.circle(screen,(200,200,200,200),(self.x-xoffset,self.y-yoffset),150,2)


    def animation(self):
        if self.is_attacking==True:
            if self.current_anim!=self.skeleton_attack:
                self.x_speed=0
                self.y_speed=0
                self.change_anim(self.skeleton_attack,0,0.1)
        if self.is_attacking==False:
            if self.current_anim!=self.skeleton_idle:
                self.change_anim(self.skeleton_idle,0,0.1)
        

    def update(self):
        self.turn()
        self.animation()
        self.anim_index+=self.anim_speed   #ex: anim_index=1 ,anim_speed=0.2. so speed ratio is 1:5
        if self.anim_index >= len(self.current_anim.right):   #to reiterate the animation
            if self.current_anim==self.skeleton_attack:
                self.is_attacking=False
            self.anim_index=0
        self.image=self.current_anim.get_img(int(self.anim_index),self.direction)  #ex: current_anim is a variable to a changeable lists, with anim_index inside stating which sprite to display
        super().update()  # calls the inheritance "update" from Entity aka Entity's update
        self.rect.center=(self.x,self.y) 
        self.enemybox_rect.center=(self.x,self.y)
        pygame.draw.rect(screen,"red",self.enemybox_rect.move(-xoffset,-yoffset),2)  



class Player(Entity):
    player_idle=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\1.Idle\\1.Idle_0{i}.png').convert_alpha(), 3) for i in range(1,9)])
    player_run=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\2.Run\\Run_0{i}.png').convert_alpha(), 3) for i in range(1,9)])
    player_roll=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\4.Roll\\Roll_0{i}.png').convert_alpha(), 3) for i in range(1,5)])
    player_heal=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\5.Heal\\Heal_0{i}.png').convert_alpha(), 3) for i in range(1,9)])
    player_death=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\6.Death\\Death_0{i}.png').convert_alpha(), 3) for i in range(1,5)])
    player_hurt=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\7.Hurt\\Hurt_0{i}.png').convert_alpha(), 3) for i in range(1,4)])
    player_attack_1=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\3.Attacks\\Attacks_{i}.png').convert_alpha(), 3) for i in range(1,7)])
    player_attack_2=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\3.Attacks\\Attacks_{i}.png').convert_alpha(), 3) for i in range(7,11)])
    player_attack_3=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\3.Attacks\\Attacks_{i}.png').convert_alpha(), 3) for i in range(11,15)])
    player_attack_4=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\3.Attacks\\Attacks_{i}.png').convert_alpha(), 3) for i in range(15,21)])

    def __init__(self,x,y):
        super().__init__(x,y)
        self.anim_index=0
        self.direction=1
        self.current_anim=self.player_idle
        self.image=self.current_anim.get_img(self.anim_index,self.direction)
        self.speed=10
        self.rect=self.image.get_rect()
        self.hitbox_rect=self.image.get_bounding_rect()
        self.hpflaskimg_image= pygame.transform.scale_by(pygame.image.load("potions\\Health potion.png").convert_alpha(),0.15)
        self.flask_rect= self.hpflaskimg_image.get_rect()
        self.anim_speed=0.1 #default animation speed used as increment on anim_index to act as time between every sprite
        self.is_attacking=False
        self.is_rolling=False
        self.is_healing=False
        self.dead=False
        self.healing_flask=2
        self.flask_intensity=50
        self.current_health=10
        self.max_health=100    
        self.attack_timer=0
        self.attack_count=0
        self.font= pygame.font.SysFont("Cambria",32)
        self.text= self.font.render(f"x {self.healing_flask}",True,(0,0,0))
        self.text_rect= self.text.get_rect()
        self.atkbox_rect= pygame.Rect((self.hitbox_rect.width+self.hitbox_rect.x),self.hitbox_rect.y,70,130) if self.direction==1 else pygame.Rect((-70+self.hitbox_rect.x),self.hitbox_rect.y,70,130)
        self.atk=False

    def healthbar(self):
        self.hpbar = pygame.draw.rect(screen, (255,0,0), (20,20,self.current_health*5,30))
        self.hpbarborder = pygame.draw.rect(screen, (0,0,0), (20,20,self.max_health*5,30),5,4)
        #self.blue = pygame.draw.rect(screen, (255, 165, 0), (10,10, self.health_bar_len,15))

    def movement(self):
        key=pygame.key.get_pressed()
        if not self.is_attacking and not self.is_rolling and not self.is_healing and not self.dead:

            if (key[pygame.K_w] or key[pygame.K_UP]) and not self.y<=border_rect.y:
                self.y_speed=-self.speed

            elif (key[pygame.K_s] or key[pygame.K_DOWN]) and not self.y+160>=border_rect.y+border_rect.height:
                self.y_speed=self.speed
            else:
                self.y_speed=0
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and not self.x+80>=border_rect.x+border_rect.width:
                self.direction=1
                self.x_speed=self.speed
            elif (key[pygame.K_a] or key[pygame.K_LEFT]) and not self.x-60<=border_rect.x:
                self.direction=-1
                self.x_speed=-self.speed
            else:
                self.x_speed=0          
        if key[pygame.K_r] and not self.dead:
            pass
        if key[pygame.K_e]:
            if not self.is_attacking and not self.dead and not self.is_healing:
                self.x_speed=0
                self.y_speed=0
                self.is_attacking=True
                self.atk=True
                player1.attack_timer=0
                player1.attack_count+=1
            if self.is_attacking and self.anim_index >= self.current_anim.length-1:
                player1.attack_timer=0
                player1.attack_count+=1

        if self.is_attacking:
            if self.attack_count==1 and self.current_anim!=self.player_attack_1:
                    if not player1.x-60<=border_rect.x and not player1.x+80>=border_rect.x+border_rect.width:
                        self.x_speed+=10*self.direction
            elif self.attack_count==2 and self.current_anim!=self.player_attack_2:
                    if not player1.x-60<=border_rect.x and not player1.x+80>=border_rect.x+border_rect.width:                    
                        self.x_speed+=10*self.direction
            elif self.attack_count==3 and self.current_anim!=self.player_attack_3:
                    if not player1.x-60<=border_rect.x and not player1.x+80>=border_rect.x+border_rect.width:                  
                        self.x_speed+=10*self.direction
            elif self.attack_count==4 and self.current_anim!=self.player_attack_4:
                     if not player1.x-60<=border_rect.x and not player1.x+80>=border_rect.x+border_rect.width:                   
                        self.x_speed+=10*self.direction
            if self.x_speed!=0:
                self.x_speed-=1*self.direction

        if self.current_health<=0:
            self.dead=True

        self.x+=self.x_speed
        self.y+=self.y_speed

    def animation(self):
        if not self.is_attacking and not self.is_rolling and not self.is_healing and not self.dead:
            if self.y_speed!=0 or self.x_speed!=0:
                if self.current_anim!=self.player_run:
                    self.change_anim(self.player_run,0,0.1)

            else:
                if self.current_anim!=self.player_idle:
                    self.change_anim(self.player_idle,0,0.1) 

        if self.is_attacking: 
            self.is_rolling=0
            if self.attack_count==1:
                if self.current_anim!=self.player_attack_1:
                    self.change_anim(self.player_attack_1,0,0.25)
            elif self.attack_count==2:
                if self.current_anim!=self.player_attack_2:
                    self.change_anim(self.player_attack_2,0,0.15)
            elif self.attack_count==3:
                    if self.current_anim!=self.player_attack_3:
                        self.change_anim(self.player_attack_3,0,0.15)
            elif self.attack_count==4:
                    if self.current_anim!=self.player_attack_4:
                        self.change_anim(self.player_attack_4,0,0.15)
            if self.atk:
                self.atkbox_rect= pygame.Rect((self.hitbox_rect.width+self.hitbox_rect.x),self.hitbox_rect.y,70,130) if self.direction==1 else pygame.Rect((-70+self.hitbox_rect.x),self.hitbox_rect.y,70,130)
                pygame.draw.rect(screen,"green",self.atkbox_rect.move(-xoffset,-yoffset))

        if self.is_healing:
                if self.current_anim!=self.player_heal:
                    self.change_anim(self.player_heal,0,0.1)
                    self.healing_flask-=1
                    if self.flask_intensity+self.current_health>=self.max_health:
                        self.current_health=self.max_health
                    else:
                        self.current_health+=self.flask_intensity
                
        
        if self.is_rolling:
                if self.current_anim!=self.player_roll:
                    self.change_anim(self.player_roll,0,0.15)

        if self.dead:
            if self.current_anim!=self.player_death:
                self.change_anim(self.player_death,0,0.15)
                    
        if self.attack_timer>50:
            self.attack_count=0

    def update(self):
        self.attack_timer+=1
        print(self.is_attacking, self.is_rolling)
        print(self.x,self.y)
        self.healthbar()
        self.movement()
        self.animation()
        global xoffset,yoffset
        xoffset=player1.x-SCREENWIDTH/2
        yoffset=player1.y-SCREENHEIGHT/2
        self.anim_index+=self.anim_speed   #ex: anim_index=1 ,anim_speed=0.2. so speed ratio is 1:5
        if self.anim_index >= self.current_anim.length:   #to reiterate the animation
            if self.current_anim==self.player_roll:
                self.is_rolling=0
                self.attack_timer=-50
            if self.current_anim==self.player_attack_1:
                self.is_attacking=0
                self.change_anim(self.player_idle,0,0.1)
            if self.current_anim==self.player_attack_2:
                self.is_attacking=0
                self.change_anim(self.player_idle,0,0.1)
            if self.current_anim==self.player_attack_3:
                self.is_attacking=0
                self.change_anim(self.player_idle,0,0.1)
            if self.current_anim==self.player_attack_4:
                self.is_attacking=0
                self.attack_count=0
                self.change_anim(self.player_idle,0,0.1) 
            if self.current_anim==self.player_heal:
                self.is_healing=False
            self.atk=0
            self.anim_index=0
            if self.current_anim==self.player_death:
                self.change_anim(self.player_death,3,0)
                
        self.image=self.current_anim.get_img(int(self.anim_index),self.direction)  #ex: current_anim is a variable to a changeable lists, with anim_index inside stating which sprite to display
        self.rect.center=(self.x,self.y)  #to put the player at the center of his rectangle
        self.hitbox_rect.center=(self.x,self.y+25)
        self.flask_rect.center=(100,1000)
        self.text_rect.center=(150,1000)
        self.text= self.font.render(f"x {self.healing_flask}",True,(0,0,0))   

player1=Player(1000,1000)
skeletons=pygame.sprite.Group()

for skeleton in range(10):
    skeletons.add(Enemy(random.randint(800,1800),random.randint(800,1800)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not player1.dead:
                if not player1.is_healing and not player1.is_attacking and not player1.is_rolling and player1.healing_flask>0 and not player1.current_health>=player1.max_health:
                    player1.x_speed=0
                    player1.y_speed=0
                    player1.is_healing=True

            if event.key == pygame.K_RIGHTBRACKET:
                player1.current_health+=50
            if event.key == pygame.K_LEFTBRACKET:
                player1.current_health-=50

            if event.key == pygame.K_SPACE :
                if not player1.is_rolling and not player1.is_attacking and not player1.is_healing and not player1.dead or (player1.is_attacking and player1.anim_index>=player1.current_anim.length-1):
                    if not player1.y<=border_rect.y and not player1.y+160>=border_rect.y+border_rect.height and not player1.x-60<=border_rect.x and not player1.x+80>=border_rect.x+border_rect.width:
                        player1.x_speed=7.5*player1.direction 
                    player1.is_rolling=True
                    player1.is_attacking=False
                    player1.attack_count=2
                    player1.attack_timer=-50

        if player1.y<=border_rect.y or player1.y+160>=border_rect.y+border_rect.height or player1.x-60<=border_rect.x or player1.x+80>=border_rect.x+border_rect.width:
            player1.x_speed=0
            player1.y_speed=0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        for skeleton in skeletons:                
            if player1.atkbox_rect.colliderect(skeleton.enemybox_rect) and player1.atk:
                skeleton.kill()

        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((137,207,240)) #fill the screen with a color to wipe away anything from last frame
    screen.blit(floor_image,(-xoffset,-yoffset))
    screen.blit(border_image,(-xoffset,-yoffset))
    screen.blit(player1.hpflaskimg_image,player1.flask_rect) #Health potion
    screen.blit(player1.text,player1.text_rect)

    pygame.draw.rect(screen,"green",border_rect.move(-xoffset,-yoffset),2)
    #pygame.draw.rect(screen,"red",border_rect.move(-xoffset,-yoffset),2)    
    pygame.draw.rect(screen,"green",player1.hitbox_rect.move(-xoffset,-yoffset),2) 
    #pygame.draw.rect(screen,"red",player1.rect) 
    #pygame.draw.circle(screen,"green",(xoffset-xoffset,yoffset-yoffset),5,2)

    entities.update()
    
    for sprite in entities:
        sprite.rect.move_ip(-xoffset,-yoffset)
    entities.draw(screen)
  



    pygame.display.flip() # flip() the display to put your work on screen
    clock.tick(FPS)  # limits FPS to 60
pygame.quit()








# class Potion(Entity):
#     def __init__(self, x, y, width, height):
#         super().__init__(x, y)
#         self.image = pygame.image.load("potions\st_potion1.png")
#         self.rect = self.image.get_rect()
#         self.image = pygame.transform.scale(self.image, (width, height))
#         self.rect = self.image.get_rect(topleft=(x, y))
#         self.used = False 
# st_potion1 = Potion(50-xoffset,50-yoffset, 200, 200)
# potion_group = pygame.sprite.Group()
# potion_group.add(st_potion1)
#max_health = 100
#current_health = 50   


#potion_got = False

            # if pygame.sprite.collide_rect(player1, st_potion1) and not potion_got:
            #     st_potion1.used = True
            #     st_potion1.kill()
            #     player1.current_health += 100
            #     potion_got = True

            # if player1.current_health > player1.max_health:
            #     player1.current_health = player1.max_health 

    #potion_group.draw(screen)
    #potion_group.update()