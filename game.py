#Thu vien
import pygame
from pygame.locals import *
import random
pygame.init()
#Cua so game
width=500
height=500
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption('Game Dua Xe')
#Mau nen
gray=(100,100,100)
white=(255,255,255)
red=(200,0,0)
yellow=(255,232,0)
green=(76,208,56)
#Khoi tao bien
gameover=False
speed=2
speed_increase=False
score=0
hiscore=0
#Kich thuoc duong
road_width=300
street_width=10
street_height=50
#Lane duong
lane_left=150
lane_mid=250
lane_right=350
lanes=[lane_left,lane_mid,lane_right]
lane_move_y=0
#Duong va le duong
road=(100,0,road_width,height)
left_edge=(95,0,street_width,height)
right_edge=(395,0,street_width,height)
#Vi tri xe ban dau
player_x=250
player_y=400
#Cac phuong tien khac
class Vehicle(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Kich thuoc anh
        image_scale= 45 / image.get_rect().width
        new_width=image.get_rect().width *image_scale
        new_height=image.get_rect().height *image_scale
        self.image=pygame.transform.scale(image,(new_width,new_height))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
#Phuong tien cua Player
class PlayerVehicle(Vehicle):
    def __init__(self,x,y):
        image=pygame.image.load('assets/images/car.png')
        super().__init__(image,x,y)
#Chia nhom Sprite 
Player_group=pygame.sprite.Group()
Vehicle_group=pygame.sprite.Group()
#Tao phuong tien Player
player= PlayerVehicle(player_x,player_y)
Player_group.add(player)
#Load phuong tien khac
image_name=['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
Vehicle_images=[]
for name in image_name:
    image=pygame.image.load('assets/images/'+name)
    Vehicle_images.append(image)
#Load hieu ung va cham
crash=pygame.image.load('assets/images/crash.png')
crash_rect=crash.get_rect()
#FPS
clock=pygame.time.Clock()
fps=120
#Vong lap game
running=True
while running:
    clock.tick(fps) #so fps
    for event in pygame.event.get():
        if event.type==QUIT:
            running=False
        #Dieu khien xe
        if event.type==KEYDOWN:
            if event.key==K_LEFT and player.rect.center[0]>lane_left:
                player.rect.x -=100
            if event.key==K_RIGHT and player.rect.center[0]<lane_right:
                player.rect.x +=100   
        #Kiem tra va cham
        for vehicle in Vehicle_group:
            if pygame.sprite.collide_rect(player,vehicle):
                gameover=True
    #Kiem tra va cham khi xe dung yen
    if pygame.sprite.spritecollide(player,Vehicle_group,True):
        gameover=True
        crash_rect.center=[player.rect.center[0],player.rect.top]
    #Ve mau
    screen.fill(green)       
    pygame.draw.rect(screen,gray,road) 
    pygame.draw.rect(screen,yellow,left_edge)
    pygame.draw.rect(screen,yellow,right_edge)
    #Lane duong chuyen dong
    lane_move_y+=speed *2
    if lane_move_y >= street_height *2: 
        lane_move_y=0
    for y in range(street_height*-2,height,street_height*2):
        pygame.draw.rect(screen,white,(lane_left + 45,y + lane_move_y,street_width,street_height))
        pygame.draw.rect(screen,white,(lane_right - 45,y + lane_move_y,street_width,street_height))
    #Ve phuong tien player
    Player_group.draw(screen)
    #Ve phuong tien khac
    if len(Vehicle_group) < 2:
        add_vehicle = True
        for vehicle in Vehicle_group:
            if vehicle.rect.top < vehicle.rect.height *1.5:
                add_vehicle = False
        if add_vehicle:
            lane= random.choice(lanes)
            image= random.choice(Vehicle_images)
            vehicle=Vehicle(image,lane,height/-2)
            Vehicle_group.add(vehicle)
    #Cho phuong tien chuyen dong
    for vehicle in Vehicle_group:
        vehicle.rect.y +=speed

        #Loai bo xe ngoai man hinh
        if vehicle.rect.top >=height:
            vehicle.kill()
            score +=1
        #Tang toc do xe
    if score>0 and score %5 ==0:
        if not speed_increase:
            speed += 1
            speed_increase=True
    else:
        speed_increase=False
    #Ve nhom phuong tien khac
    Vehicle_group.draw(screen) 
    #Hien so diem
    font=pygame.font.Font(pygame.font.get_default_font(),14)
    text=font.render(f'Score: {score}',True,white)
    text_rect=text.get_rect()
    text_rect.center=(50,40)
    screen.blit(text,text_rect)  
    #Hien Diem cao
    font=pygame.font.Font(pygame.font.get_default_font(),14)
    text=font.render(f'High Score: {hiscore}',True,white)
    text_rect=text.get_rect()
    text_rect.center=(50,60)
    screen.blit(text,text_rect) 
    if score>hiscore: hiscore=score  
    if gameover:
        screen.blit(crash,crash_rect)    
        pygame.draw.rect(screen,red,(0,50,width,100))
        font=pygame.font.Font(pygame.font.get_default_font(),16)
        text=font.render(f'Game Over! Retry? (Y/N)',True,white)
        text_rect=text.get_rect()
        text_rect.center=(width/2,100) 
        screen.blit(text,text_rect)   
    pygame.display.update()
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==QUIT:
                gameover=False
                running=False
            if event.type==KEYDOWN:
                if event.key == K_y:
                    gameover=False
                    score=0
                    speed=2
                    Vehicle_group.empty()
                    player.rect.center=[player_x,player_y]
                elif event.key == K_n:
                    gameover=False
                    running=False

pygame.quit()