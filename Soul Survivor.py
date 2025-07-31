import pygame
import subprocess

pygame.init()
FPS=60 
SCREENWIDTH=1280
SCREENHEIGHT=720
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) #Set Resolution
clock = pygame.time.Clock()


good_head = pygame.image.load("head.png").convert()
good_head.set_colorkey((255, 255, 255))  # Set white as transparent
bg_image = pygame.image.load('bg.png').convert()

good_head = pygame.transform.scale(good_head, (500, 124)) 
good_bg = pygame.transform.scale(bg_image, (1280,720))

class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, images):

        self.images = images  # List of images for animation frames
        self.index = 0  # Current frame index
        self.image = self.images[self.index]  # Set initial image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hovered = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)



    def update(self):
        pos = pygame.mouse.get_pos()  # track current mouse position
        self.hovered = self.rect.collidepoint(pos)  # Check if the mouse is over the button

        if self.hovered:  # If the mouse is over the button
                            
            self.image = self.images[1] # Set the image to the second index image
        else:
            
            self.image = self.images[0] # If not hovered, display default button image (first index)

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and self.rect.collidepoint(pos) :  # Check for left mouse button click
                self.image = self.images[2]





play_button_images = [pygame.transform.scale(pygame.image.load(f'buttons\\start but\\start_01{i}.png').convert_alpha(), (150, 50)) for i in range(1, 4)]
play_button = Button(300, 200, play_button_images)

continue_button_images = [pygame.transform.scale(pygame.image.load(f'buttons\\continue\\continue_01{i}.png').convert_alpha(), (150, 50)) for i in range(1, 4)]
continue_button = Button(500, 198, continue_button_images)

image_list = [
    pygame.image.load('tut\\welcome.png').convert_alpha(),
    pygame.image.load('tut\\controls.png').convert_alpha(),
    pygame.image.load('tut\\remember.png').convert_alpha(),
    
]

current_image_index = 0
current_image = image_list[current_image_index] 
    


x_pos = 650
y_pos = 200

hx_pos = 300
hy_pos = 50

continue_button_on = True


def is_clicked():
    global current_image_index, continue_button_on, current_image, going, menusong
    if event.type == pygame.MOUSEBUTTONUP:
            if play_button.rect.collidepoint(event.pos):
                subprocess.run(["python", "-c", "from Soul_Survivors import *"])
                going = False
                play_button.image = play_button.images[2]  # Change the play_button image
                continue_button.image = continue_button_images[2]  # Change the continue_button image
                
            if continue_button.rect.collidepoint(event.pos) :
                current_image_index += 1
                if current_image_index < len(image_list):
                    current_image = image_list[current_image_index]
                    
                    
            if current_image_index == len(image_list) - 1:
                
                continue_button_on = False   
                image_list.clear()



going = True
# Main loop
while going:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                going = False
                
        if event.type == pygame.QUIT:
            going = False
        is_clicked()


                    
                
                 

    screen.blit(good_bg, (0, 0))
    screen.fill(0)
    screen.blit(good_bg, (0, 0))  # Draw the background 
    screen.blit(good_head, (hx_pos, hy_pos))  # Draw the title



    if continue_button_on:
        continue_button.update()  # Update continue button appearance
        continue_button.draw(screen)

    
    play_button.update()  # Update play button appearance
    play_button.draw(screen)  # Draw play button on the screen
              

    screen.blit(current_image, (x_pos, y_pos))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()    
     