import pygame
import random
import math
#------WASD to move------E to Attack------SPACE to Roll------R to Heal------

pygame.init()
FPS=60 #Set FPS
SCREENWIDTH=1280
SCREENHEIGHT=720
NUMBER_OF_SKELETONS=10
NUMBER_OF_BATS=10

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) #Set Resolution
clock = pygame.time.Clock()
running = True
entities=pygame.sprite.Group()
xoffset=0
yoffset=0
border_image=pygame.transform.scale_by((pygame.image.load('Map\\borders.png')).convert_alpha(),4)
border_rect=border_image.get_bounding_rect()
floor_image=pygame.transform.scale_by((pygame.image.load('Map\\Floor.png')).convert_alpha(),4)
mapobjects_image=pygame.transform.scale_by((pygame.image.load('Map\\mapobjects.png')).convert_alpha(),4)

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
        self.skeleton_walk=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\Walk\\Walk_0{i}.png').convert_alpha(), 2.4) for i in range(1,4)])
        self.skeleton_attack=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\Attack\\Attack_0{i}.png').convert_alpha(), 2.4) for i in range(1,9)])
        self.skeleton_hit=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\TakeHit\\TakeHit_0{i}.png').convert_alpha(), 2.4) for i in range(1,4)])
        self.skeleton_death=Animation ([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Skeleton\\Death\\Death_0{i}.png').convert_alpha(), 2.4) for i in range(1,4)])
        self.current_anim=self.skeleton_idle
        self.current_health=50
        self.anim_index=0
        self.anim_speed=0.1
        self.is_attacking=False
        self.is_hit=False
        self.is_dead=False
        self.speed=4      
        self.direction=1
        self.image=self.current_anim.get_img(self.anim_index,self.direction)
        self.rect=self.image.get_rect()
        self.enemybox_rect=self.image.get_bounding_rect()
        self.atkbox_rect=pygame.Rect((self.enemybox_rect.width+self.enemybox_rect.x),self.enemybox_rect.y,70,130) if self.direction==1 else pygame.Rect((-70+self.enemybox_rect.x),self.enemybox_rect.y,70,130)
    
    def movement(self):
        if not self.is_attacking and not self.is_hit and not self.is_dead:
            self.x_speed=player1.x-self.x
            self.y_speed=player1.y-self.y
            resultant=math.sqrt(self.x_speed**2+self.y_speed**2)
            self.x_speed*=self.speed/resultant
            self.y_speed*=self.speed/resultant

        self.x+=self.x_speed
        self.y+=self.y_speed
    
    def turn(self):
        #pygame.draw.line(screen,'blue',(self.x+150-xoffset,self.y-yoffset),(self.x-150-xoffset,self.y-yoffset)) #Enemy Detection Box
        #pygame.draw.line(screen,'blue',(self.x-xoffset,self.y-150-yoffset),(self.x-xoffset,self.y+150-yoffset)) #Enemy Detection Box           
        #pygame.draw.line(screen,'purple',(player1.x-xoffset,0),(player1.x-xoffset,1080-yoffset)) #Enemy Detection Box
        #pygame.draw.line(screen,'purple',(0,player1.y-yoffset),(1920-xoffset,player1.y-yoffset)) #Enemy Detection Box
        
        if not self.is_attacking or (self.is_attacking and self.anim_index<5):
            if player1.x<self.x:
                self.direction=-1
            elif player1.x>self.x:
                self.direction=1     
                
        if self.x-player1.x<=150 and self.x-player1.x>=-150 and self.y-player1.y<=50 and self.y-player1.y>=-50:
            #pygame.draw.line(screen,'red',(self.x-xoffset,self.y-yoffset),(player1.x-xoffset,player1.y-yoffset)) #Enemy Detection Box
            #pygame.draw.circle(screen,'red',(self.x-xoffset,self.y-yoffset),150,2) #Enemy Detection Box
            self.is_attacking=True
        else:
            pass
            #pygame.draw.line(screen,'green',(self.x-xoffset,self.y-yoffset),(player1.x-xoffset,player1.y-yoffset))  #Enemy Detection Box
            #pygame.draw.circle(screen,(200,200,200,200),(self.x-xoffset,self.y-yoffset),150,2) #Enemy Detection Box


    def animation(self):
        if (self.x_speed!=0 or self.y_speed!=0) and not self.is_attacking and not self.is_hit and not self.is_dead:
            if self.current_anim!=self.skeleton_walk:
                self.change_anim(self.skeleton_walk,0,0.1)

        if self.is_attacking and not self.is_hit and not self.is_dead:
            if self.current_anim!=self.skeleton_attack:
                self.x_speed=0
                self.y_speed=0
                self.change_anim(self.skeleton_attack,0,0.1)
        
        if self.is_hit and not self.is_dead:
            if self.current_anim!=self.skeleton_hit:
                self.change_anim(self.skeleton_hit,0,0.1)

        if self.is_dead:
            self.x_speed=0
            self.y_speed=0
            if self.current_anim!=self.skeleton_death:
                self.change_anim(self.skeleton_death,0,0.05)


    def atkbox(self):
        self.atkbox_rect=pygame.Rect(-500,-500,70,130) if self.direction==1 else pygame.Rect(-500,-500,70,130)                
        if self.current_anim==self.skeleton_attack:
            if self.anim_index>=6:
                self.atkbox_rect=pygame.Rect((self.enemybox_rect.width+self.enemybox_rect.x),self.enemybox_rect.y,70,130) if self.direction==1 else pygame.Rect((-70+self.enemybox_rect.x),self.enemybox_rect.y,70,130)
                #pygame.draw.rect(screen,"red",self.atkbox_rect.move(-xoffset,-yoffset)) # Enemy Attack Hitbox

    def update(self):
        self.movement()
        self.turn()
        self.animation()
        self.atkbox()
        self.anim_index+=self.anim_speed   #ex: anim_index=1 ,anim_speed=0.2. so speed ratio is 1:5

        if self.current_anim==self.skeleton_attack:
            if self.anim_index>=6:
                self.anim_speed=0.2

        if self.anim_index >= len(self.current_anim.right):   #to reiterate the animation
            if self.current_anim==self.skeleton_attack:
                self.is_attacking=False
            if self.current_anim==self.skeleton_hit:
                self.is_hit=False
            if self.current_anim==self.skeleton_death:
                self.kill()
            self.anim_index=0
            self.anim_speed=0.1

        self.image=self.current_anim.get_img(int(self.anim_index),self.direction)  #ex: current_anim is a variable to a changeable lists, with anim_index inside stating which sprite to display
        super().update()  # calls the inheritance "update" from Entity aka Entity's update
        self.rect.center=(self.x,self.y) 
        self.enemybox_rect.center=(self.x,self.y)
        #pygame.draw.rect(screen,"red",self.enemybox_rect.move(-xoffset,-yoffset),2) #Enemy Hitbox 



class Player(Entity):
    player_idle=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\1.Idle\\1.Idle_0{i}.png').convert_alpha(), 3) for i in range(1,9)])
    player_run=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\2.Run\\Run_0{i}.png').convert_alpha(), 3) for i in range(1,9)])
    player_roll=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\4.Roll\\Roll_0{i}.png').convert_alpha(), 3) for i in range(1,5)])
    player_heal=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\5.Heal\\Heal_0{i}.png').convert_alpha(), 3) for i in range(1,9)])
    player_death=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\6.Death\\Death_0{i}.png').convert_alpha(), 3) for i in range(1,5)])
    player_hurt=Animation([pygame.transform.scale_by(pygame.image.load(f'2D_SL_Knight_v1.0\\7.Hurt\\Hurt_0{i}.png').convert_alpha(), 3) for i in range(1,3)])
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
        self.is_dead=False
        self.is_invincible=False
        self.is_hit=False
        self.healing_flask=5
        self.flask_intensity=50
        self.current_health=100
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


    #sound effects    
    
    def play_music_loop(music_file):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load("sound_effects/game_loop.wav")
        pygame.mixer.music.play(-1)  

    music_path = "sound_effects/game_loop.wav"  
    play_music_loop(music_path)    
    
    def steps(self):
            steps_sound = pygame.mixer.Sound("sound_effects/foot.wav")
            steps_sound.play(0,1)
            
    def roll_sound(self):
            roll_s = pygame.mixer.Sound("sound_effects/mixkit-explainer-video-game-alert-sweep-236.wav")
            roll_s.play()
            
    def sword_sound(self):
            sword = pygame.mixer.Sound("sound_effects/sword.wav")
            sword.play(1)

    def health_sound(self):
            health = pygame.mixer.Sound("sound_effects/r.wav")
            health.play()


    def movement(self):
        key=pygame.key.get_pressed()
        if not self.is_attacking and not self.is_rolling and not self.is_healing and not self.is_dead and not self.is_hit:

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

        if key[pygame.K_e]:
            if not self.is_attacking and not self.is_dead and not self.is_healing and not self.is_hit:
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
            self.is_dead=True

        self.x+=self.x_speed
        self.y+=self.y_speed

    def animation(self):
        if not self.is_attacking and not self.is_rolling and not self.is_healing and not self.is_dead and not self.is_hit:
            if self.y_speed!=0 or self.x_speed!=0:
                self.steps()
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
                #pygame.draw.rect(screen,"green",self.atkbox_rect.move(-xoffset,-yoffset)) # Player Attack Hitbox
        
        if self.is_hit and not self.is_dead:
            if self.current_anim!=self.player_hurt:
                self.y_speed=0
                self.is_invincible=True
                self.change_anim(self.player_hurt,0,0.15)
    
        if self.is_healing:
                if self.current_anim!=self.player_heal:
                    self.change_anim(self.player_heal,0,0.1)
                
        if self.is_rolling:
                if self.current_anim!=self.player_roll:
                    self.roll_sound()
                    self.is_invincible=True
                    self.change_anim(self.player_roll,0,0.15)

        if self.is_dead:
            self.x_speed=0
            self.y_speed=0
            if self.current_anim!=self.player_death:
                self.change_anim(self.player_death,0,0.1)

        if self.is_dead or self.is_hit:
            self.is_healing=False
            self.is_attacking=False

        if self.attack_timer>50:
            self.attack_count=0


    def update(self):
        self.attack_timer+=1
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
                self.sword_sound()
                self.is_attacking=0
                self.change_anim(self.player_idle,0,0.1)
            if self.current_anim==self.player_attack_2:
                self.sword_sound()
                self.is_attacking=0
                self.change_anim(self.player_idle,0,0.1)
            if self.current_anim==self.player_attack_3:
                self.sword_sound()
                self.is_attacking=0
                self.change_anim(self.player_idle,0,0.1)
            if self.current_anim==self.player_attack_4:
                self.sword_sound()
                self.is_attacking=0
                self.attack_count=0
                self.change_anim(self.player_idle,0,0.1) 
            if self.current_anim==self.player_heal:
                self.health_sound()
                self.is_healing=False
            if self.current_anim==self.player_hurt:
                self.is_hit=False
            if self.current_anim==self.player_heal:
                    self.healing_flask-=1
                    if self.flask_intensity+self.current_health>=self.max_health:
                        self.current_health=self.max_health
                    else:
                        self.current_health+=self.flask_intensity
            self.is_invincible=False
            self.atk=0
            self.anim_index=0
            if self.current_anim==self.player_death:
                self.change_anim(self.player_death,3,0)
                
        self.image=self.current_anim.get_img(int(self.anim_index),self.direction)  #ex: current_anim is a variable to a changeable lists, with anim_index inside stating which sprite to display
        self.rect.center=(self.x,self.y)  #to put the player at the center of his rectangle
        self.hitbox_rect.center=(self.x,self.y+25)
        self.flask_rect.center=(100,650)
        self.text_rect.center=(150,650)
        self.text= self.font.render(f"x {self.healing_flask}",True,(0,0,0))   
        


class Dagger(Entity):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.current_anim=Animation([pygame.transform.scale(pygame.image.load('Dagger r.png').convert_alpha(), (50, 50))])
        self.image=self.current_anim.get_img(0,player1.direction)
        self.rect=self.image.get_bounding_rect()
        self.x_speed=player1.direction*20         #dagger speed
        self.distance_travelled=0

    def update(self):
        self.x+=self.x_speed
        self.rect.center=(self.x,self.y)
        self.distance_travelled += 20  # Assuming 20 is the movement speed. Increment the distance traveled.

        if self.distance_travelled >= 500:
            self.kill()  # Remove the Dagger from the group when it reaches the limit # Check if the Dagger has traveled 500 pixels

        for skeleton in skeletons:
            if self.rect.colliderect(skeleton.enemybox_rect):
                skeleton.current_health-=15
                skeleton.is_hit=True
                skeleton.is_attacking=False
                skeleton.x_speed+=0.2*player1.direction
                if skeleton.current_health <= 0:
                    skeleton.is_dead=True
                self.kill()

        for bat in bats:
            if self.rect.colliderect(bat.hitbox_rect):
                bat.current_health-=20
                bat.is_attacking=False
                if bat.current_health <= 0:
                    bat.is_dead=True
                self.kill()
        #pygame.draw.rect(screen,"green",self.rect.move(-xoffset,-yoffset)) #Dagger Attack box
                
class Fireball(Entity):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image=pygame.transform.scale(pygame.image.load('fireball.png').convert_alpha(), (50, 50))
        self.rect=self.image.get_bounding_rect()
        self.distance_travelled=0

        self.x_speed=player1.x-self.x
        self.y_speed=player1.y-self.y
        resultant=math.sqrt(self.x_speed**2+self.y_speed**2) #magnitude of vector (distance between player and fireball)
        self.x_speed*=7/resultant #fireball speed x
        self.y_speed*=7/resultant #fireball speed y
    
    def update(self):
        self.x+=self.x_speed
        self.y+=self.y_speed
        self.rect.center=(self.x,self.y) 
        self.distance_travelled += 7  # Assuming 10 is the movement speed. Increment the distance traveled.
 
        if self.distance_travelled >= 700:        # Check if the Fireball has traveled 700 pixels
            self.kill()  # Remove the Fireball from the group when it reaches the limit


        if self.rect.colliderect(player1.hitbox_rect) and not player1.is_invincible:
            if not player1.is_dead:
                player1.x_speed+=10*bat.direction
            player1.is_attacking=False
            player1.is_healing=False
            player1.is_hit=True
            player1.current_health-=2
            self.kill()
        #pygame.draw.rect(screen,"green",self.rect.move(-xoffset,-yoffset)) #Dagger Attack box

class Bat(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.Bat_Flight = Animation([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Flying eye\\2.Flight\\Flight_0{i}.png').convert_alpha(), 2.4) for i in range(1, 8)])
        self.Bat_attack = Animation([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Flying eye\\1.Attack\\Attack_0{i}.png').convert_alpha(), 2.4) for i in range(1, 8)])
        self.Bat_hit = Animation([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Flying eye\\3.TakeHit\\Take-Hit_0{i}.png').convert_alpha(), 2.4) for i in range(1, 4)])
        self.Bat_death = Animation([pygame.transform.scale_by(pygame.image.load(f'Monsters_Creatures_Fantasy\\Flying eye\\4.Death\\Death_0{i}.png').convert_alpha(), 2.4) for i in range(1, 4)])
        self.current_anim=self.Bat_Flight
        self.anim_index = 0
        self.anim_speed = 0.1  # Adjust the animation speed
        self.direction=1
        self.speed=2
        self.image = self.current_anim.get_img(self.anim_index, self.direction)
        self.rect = self.image.get_rect()
        self.hitbox_rect = self.image.get_bounding_rect()
        self.shoot_timer = 0
        self.shoot_frequency = 120  # Adjust the shoot frequency (every 2 seconds)
        self.distance_to_player = math.sqrt((self.x-player1.x)**2+(self.y-player1.y)**2)     # Calculate the distance between the Bat and the Player
        self.is_attacking=False
        self.is_dead=False
        self.is_hit=False
        self.current_health=15

    def movement(self):
        if not self.is_attacking and not self.is_hit and not self.is_dead:
            self.x_speed=player1.x-self.x
            self.y_speed=player1.y-self.y
            resultant=math.sqrt(self.x_speed**2+self.y_speed**2)

            if resultant>=400:
                self.x_speed*=self.speed/resultant
                self.y_speed*=self.speed/resultant
                self.x+=self.x_speed
                self.y+=self.y_speed

    def turn(self):
        if self.distance_to_player <= 500 and player1.x > self.x:        # Check if the Player is within 500 pixels in front of the Bat
            self.direction = 1  # Set the direction to face the front
        elif self.distance_to_player <= 500 and player1.x < self.x:        # Check if the Player is within 500 pixels behind the Bat
            self.direction = -1  # Set the direction to face behind

    def animation(self):
        if not self.is_hit and not self.is_dead:
            if self.is_attacking:
                if self.current_anim!=self.Bat_attack:
                    self.change_anim(self.Bat_attack,0,0.05)

        if self.is_dead:
            self.x_speed=0
            self.y_speed=0
            self.is_attacking=False
            self.is_hit=False
            if self.current_anim!=self.Bat_death:
                self.change_anim(self.Bat_death,0,0.05)

    def shoot_fireball(self):
        self.distance_to_player = math.sqrt((self.x-player1.x)**2+(self.y-player1.y)**2)
        if self.distance_to_player<=400:
            fireball=Fireball(self.hitbox_rect.x, self.hitbox_rect.y)
            fireball.direction=self.direction
            self.shoot_timer = 0  # Reset the shoot timer after shooting

    def update(self):
        super().update()
        self.animation()
        self.movement()
        self.turn()
        self.anim_index += self.anim_speed        # Update the animation index based on the animation speed
        if self.anim_index >= len(self.current_anim.right):        # Ensure the animation index stays within the valid range
            if self.current_anim == self.Bat_death:
                self.kill()
            self.anim_index = 0
        self.image = self.current_anim.get_img(int(self.anim_index), self.direction)        # Set the current image based on the animation index        
        self.rect.center = (self.x, self.y)
        self.hitbox_rect.center = (self.x, self.y + 25)

        if self.anim_index >= len(self.current_anim.right):
            self.anim_index = 0
        self.image = self.current_anim.get_img(int(self.anim_index), self.direction)

        if self.shoot_timer >= self.shoot_frequency:        # Check if it's time to shoot a fireball
            self.shoot_fireball()
        else:
            self.shoot_timer += 1

class hp_potion(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.image = pygame.image.load("potions\\Health potion.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.used = False


player1=Player(border_rect.width/2,border_rect.height/2)
skeletons=pygame.sprite.Group()
bats=pygame.sprite.Group()

while running:

    if not skeletons.sprites():
        for skeleton in range(NUMBER_OF_SKELETONS):
            xby1=int(player1.x)+(1280/2*random.choice([1,-1]))
            yby1=int(player1.y)+random.randint(-1,1)*720/2
            
            xby2=int(player1.x)+random.randint(-1,1)*1280/2
            yby2=int(player1.y)+(720/2*random.choice([1,-1]))

            xby= random.choice([xby1,yby1])
            if xby==xby1:
                yby=yby1
            else:
                yby=yby2
            skeletons.add(Enemy(random.randint(int(xby),int(xby)),random.randint(int(yby),int(yby))))
            
    if not bats.sprites():
        for bat in range(NUMBER_OF_BATS):
            xby1=int(player1.x)+(1280/2*random.choice([1,-1]))
            yby1=int(player1.y)+random.randint(-1,1)*720/2
            
            xby2=int(player1.x)+random.randint(-1,1)*1280/2
            yby2=int(player1.y)+(720/2*random.choice([1,-1]))

            xby= random.choice([xby1,yby1])
            if xby==xby1:
                yby=yby1
            else:
                yby=yby2
            bats.add(Bat(random.randint(int(xby),int(xby)),random.randint(int(yby),int(yby))))        
                
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not player1.is_dead and not player1.is_hit:
                if not player1.is_healing and not player1.is_attacking and not player1.is_rolling and player1.healing_flask>0 and not player1.current_health>=player1.max_health:
                    player1.x_speed=0
                    player1.y_speed=0
                    player1.is_healing=True

            if event.key == pygame.K_RIGHTBRACKET:
                player1.current_health+=50
            if event.key == pygame.K_LEFTBRACKET:
                player1.current_health-=50

            if event.key == pygame.K_SPACE:
                if not player1.is_rolling and not player1.is_hit and not player1.is_attacking and not player1.is_healing and not player1.is_dead or (player1.is_attacking and player1.anim_index>=player1.current_anim.length-1):
                    if not player1.y<=border_rect.y and not player1.y+160>=border_rect.y+border_rect.height and not player1.x-60<=border_rect.x and not player1.x+80>=border_rect.x+border_rect.width:
                        player1.x_speed=7.5*player1.direction 
                    
                    player1.is_rolling=True
                    player1.is_attacking=False
                    player1.attack_count=2
                    player1.attack_timer=-50

            if event.key == pygame.K_q:
                Dagger(player1.hitbox_rect.x+player1.hitbox_rect.width/2, player1.hitbox_rect.y+player1.hitbox_rect.height/2)


        if player1.y<=border_rect.y or player1.y+160>=border_rect.y+border_rect.height or player1.x-60<=border_rect.x or player1.x+80>=border_rect.x+border_rect.width:
            player1.x_speed=0
            player1.y_speed=0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((137,207,240)) #fill the screen with a color to wipe away anything from last frame
    screen.blit(floor_image,(-xoffset,-yoffset)) #grass ground
    screen.blit(border_image,(-xoffset,-yoffset)) #borders of map
    screen.blit(mapobjects_image,(-xoffset,-yoffset)) #house,graves,etc on map


    screen.blit(player1.hpflaskimg_image,player1.flask_rect) #Health potion counter
    screen.blit(player1.text,player1.text_rect) #Health potion counter

    #pygame.draw.rect(screen,"green",border_rect.move(-xoffset,-yoffset),2) # Border hitbox
    #pygame.draw.rect(screen,"green",player1.hitbox_rect.move(-xoffset,-yoffset),2) # Player hitbox
    #pygame.draw.rect(screen,"red",player1.rect) #hitboxes
    #pygame.draw.circle(screen,"green",(xoffset-xoffset,yoffset-yoffset),5,2) #hitboxes

    entities.update()


    for skeleton in skeletons:                
        if player1.atkbox_rect.colliderect(skeleton.enemybox_rect) and player1.atk:
            skeleton.current_health-=1
            skeleton.is_hit=True
            skeleton.is_attacking=False
            skeleton.x_speed+=0.2*player1.direction
            if skeleton.current_health <= 0:
                skeleton.is_dead=True

        if skeleton.atkbox_rect.colliderect(player1.hitbox_rect) and not player1.is_invincible:
            if not player1.is_dead:
                player1.x_speed+=10*skeleton.direction
            player1.is_attacking=False
            player1.is_healing=False
            player1.is_hit=True
            player1.current_health-=10

    for bat in bats:
        if player1.atkbox_rect.colliderect(bat.hitbox_rect) and player1.atk:
            bat.current_health-=1
            bat.is_attacking=False
            if bat.current_health <= 0:
                bat.is_dead=True
    
    for sprite in entities:
        sprite.rect.move_ip(-xoffset,-yoffset)
    entities.draw(screen)
    


    pygame.display.flip() # flip() the display to put your work on screen
    clock.tick(FPS)  # limits FPS to 60
pygame.quit()




# Creating the potion object
# potion_group = pygame.sprite.Group()  # Creating a group for potions

# def inv():    
#     for skeleton in skeletons:
#         if skeleton.is_dead:
#             potx=skeleton.x
#             poty=skeleton.y
#             potion = hp_potion(potx - xoffset, poty - yoffset, 50, 50)
#             potion_group.add(potion)  # Add each potion instance to the group

# # ... rest of your code ...



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

    # inv()
    # potion_group.update()
    # potion_group.draw(screen)