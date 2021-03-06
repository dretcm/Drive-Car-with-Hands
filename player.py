import pygame
import random, math
from pygame.locals import *
from utils import load_images, load_image
import cv2
import mediapipe as mp
import threading


pygame.init()


class BASE:
        speed = 15

        width = 40
        height = 70
        size = (width,height)

        def __init__(self, window_size, pos_init=None):
                if pos_init:
                        x, y = pos_init
                else:
                        x = window_size[0]//2 - 45
                        y = window_size[1] - 100
                
                self.rect = pygame.Rect(x, y, self.width, self.height)
                
        def get_position(self):
                return self.rect.topleft # (self.rect.x, self.rect.y)
        
        def set_position(self,x,y):
                self.rect.topleft = [x, y]
                
        def get_collider(self):
                return self.rect



def cv2image_to_pygame(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")



class Player(BASE):
        def __init__(self, window_size):
                super().__init__(window_size)

                self.window_size = window_size

                self.death = False
                self.left = False
                self.right = False

                self.sonido_f = pygame.mixer.Sound("music/muerte.mp3")

                self.image = load_image('images/cars/mycar.png', size=self.size)


                self.pos_camera = (10,20)
                self.size_camera = (230,200)
                self.camera_img = None

                self.mp_drawing = mp.solutions.drawing_utils
                self.mp_hands = mp.solutions.hands
                self.cap = cv2.VideoCapture(0)
##                tp = threading.Thread(target=self.camera_activate)
##                tp.start()


        def direction(self, left, right):
                difference = 100
                if difference < abs(left - right):
                        if left > right:
                                self.left = True
                                self.right = False
                                #print("right")
                        else:
                                self.right = True
                                self.left = False
                                # print("left")
                else:
                        self.left = False
                        self.right = False
                        #print("normal")

        def camera_activate(self):
                with self.mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=2,
                    min_detection_confidence=0.5) as hands:
                        ret, frame = self.cap.read()

                        height, width, _ = frame.shape
                        frame = cv2.flip(frame, 1)
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        results = hands.process(frame_rgb)
                        thumbs = []
                        if results.multi_hand_landmarks is not None:
                                for hand_landmarks in results.multi_hand_landmarks:
                                        x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x * width)
                                        y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y * height)
                                        cv2.circle(frame, (x, y), 3,(0,255,0),15)
                                        thumbs.append((x,y))
                                if len(thumbs) == 2:
                                        if (thumbs[0][0] < thumbs[1][0]):
                                                left = thumbs[0][1]
                                                right = thumbs[1][1]
                                        else:
                                                left = thumbs[1][1]
                                                right = thumbs[0][1]
                                        self.direction(left, right)

                        if len(thumbs) < 2:
                                self.left = False
                                self.right = False
                                                

                        frame = cv2.resize(frame, self.size_camera)
                        self.camera_img = cv2image_to_pygame(frame)

##                        if self.death:
##                                self.cap.release()

        def __del__(self):
                self.cap.release()
                
        def down_key(self,key):
                if key == K_LEFT:
                        self.left = True
                if key == K_RIGHT:
                        self.right = True

                        
        def up_key(self,key):
                if key == K_LEFT:
                        self.left = False
                if key == K_RIGHT:
                        self.right = False
                
                        
        def moving(self):
                if self.left:
                        self.rect.x -= self.speed
                if self.right:
                        self.rect.x += self.speed
                        
        def moving_player(self, screen):
                self.camera_activate()
                self.moving()
                screen.blit(self.image, self.get_position())
                if self.camera_img:
                        screen.blit(self.camera_img, self.pos_camera)        
                
                
        def is_death(self):
                return self.death

        def collider_with(self, collider):
                if self.rect.colliderect(collider):
                        self.death = True
                        self.sonido_f.play()

        def refresh(self):
                self.death = False
                self.left = False
                self.right = False
                super().__init__(self.window_size)


class OtherCar(BASE):
        def __init__(self, window_size, speed):
                pos_init = [random.randint(int(window_size[0]*0.25), int(window_size[0]*0.75)- self.width), -50]
                super().__init__(window_size, pos_init)

                self.speed = speed
                cars = ["images/cars/yellowcar.png", "images/cars/redcar.png",
                        "images/cars/purplecar.png", "images/cars/bluecar.png",
                        "images/cars/greencar.png"]

                self.image = load_image(random.choice(cars), size=self.size)
                
        def moving_car(self, screen):
                self.rect.y += self.speed
                screen.blit(self.image, self.get_position())



class GenerateCars:
        def __init__(self, window_size):
                self.t = 0
                self.nt = 15
                self.window_size = window_size

                self.tail_cars = []

                self.speed_cars = [15, 20, 25, 30, 40]
                

        def show_cars(self, screen, player):
                if self.t > self.nt:
                        NewCar = OtherCar(self.window_size, random.choice(self.speed_cars))
                        self.tail_cars.append(NewCar)
                        self.t = 0
                else:
                        self.t += 1

                if self.tail_cars:
                        temporal = []
                        for car in self.tail_cars:
                                car.moving_car(screen)
                                if car.get_position()[1] < self.window_size[1]:
                                        temporal.append(car)

                                player.collider_with(car.get_collider())
                                
                        self.tail_cars = temporal.copy()
                        
        def refresh(self):
                self.t = 0
                self.nt = 15
                self.tail_cars = []
                
class GenerateVia:
        speed_sprite = 1.0
        def __init__(self, window_size):
                self.window_size = window_size

                self.lforest = load_image("images/Lforest.png", size=(window_size[0]//4, window_size[1]))
                self.pos_l = (0,0)
                self.rect_l = pygame.Rect(0, 0, int(window_size[0]*0.25), window_size[1])

                self.rforest = load_image("images/Rforest.png", size=(window_size[0]//4, window_size[1]))
                self.pos_r = (int(window_size[0]*0.75),0)
                self.rect_r = pygame.Rect(self.pos_r[0], 0, int(window_size[0]*0.25), window_size[1])

                self.font = pygame.font.Font(None,40)
                self.km = 0.0
                self.pos_score = (window_size[0]-200, 20)
                self.rect_score = [self.pos_score[0], self.pos_score[1]-10, 150, 50]

                
                size = (window_size[0]//2,window_size[1])
                self.pos_via = (int(window_size[0]*0.25), 0)
                self.images = load_images(['images/via/via1.png', 'images/via/via2.png'], size=size) # 'images/via/via3.png'
                                        
                self.actual = 0
                self.image = self.images[self.actual]
                

        def show_via(self, screen, player):
                self.changues_img(self.images)
                screen.blit(self.image, self.pos_via)
                
                screen.blit(self.lforest, self.pos_l)
                screen.blit(self.rforest, self.pos_r)
                
                pygame.draw.rect(screen, (255, 255, 255), self.rect_score)

                score = self.font.render(" km: " + str(int(self.km)), 1, (0,0,0))
                screen.blit(score, self.pos_score)
                self.km += 0.4
                
                player.collider_with(self.rect_l)
                player.collider_with(self.rect_r)

        def changues_img(self, sprites):
                if self.actual >= len(sprites):
                        self.actual = 0
                self.image = sprites[int(self.actual)]
                self.actual += self.speed_sprite

        def refresh(self):
                self.km = 0
        
