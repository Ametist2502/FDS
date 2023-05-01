import pygame
import image
from settings import *
from hand_tracking import HandTracking
import cv2

class Hand:
    def __init__(self):
        self.orig_image = image.load("Assets/hand.png", size=(HAND_SIZE, HAND_SIZE))
        self.stun_image =  image.load("Assets/stun_hand.png", size=(HAND_SIZE, HAND_SIZE))
        self.image = self.orig_image.copy()
        self.stun = 0
        self.image_smaller = image.load("Assets/hand.png", size=(HAND_SIZE - 50, HAND_SIZE - 50))
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, HAND_HITBOX_SIZE[0], HAND_HITBOX_SIZE[1])
        self.left_click = False
        #self.hand_tracking = HandTracking()


    def follow_mouse(self): # change the hand pos center at the mouse pos
        self.rect.center = pygame.mouse.get_pos()
        #self.hand_tracking.display_hand()

    def follow_mediapipe_hand(self, x, y):
        self.rect.center = (x, y)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (800, 240, 0), self.rect)


    def draw(self, surface):
        image.draw(surface, self.image, self.rect.center, pos_mode="center")

        if DRAW_HITBOX:
            self.draw_hitbox(surface)


    def on_insect(self, insects, onlyNeg=False): # return a list with all insects that collide with the hand hitbox
        # if not onlyNeg:
        #     return [insect for insect in insects if self.rect.colliderect(insect.rect)]
        # else:
        #     return [insect for insect in insects if (insect.name=='bee' and self.rect.colliderect(insect.rect))]
        return [insect for insect in insects if self.rect.colliderect(insect.rect)]


    def kill_insects(self, insects, score, mosquito, bee, sounds): # will kill the insects that collide with the hand when the left mouse button is pressed
        # print(self.stun)
        if self.stun > 0:
            self.stun = 0
        elif self.left_click: # if left click
            for insect in self.on_insect(insects):
                insect_score = insect.kill(insects)
                score += insect_score
                sounds["slap"].play()         
                mosquito += 1
        else:
            self.left_click = False

            for insect in self.on_insect(insects, onlyNeg=True):
                insect_score = insect.kill(insects)
                score += insect_score
                sounds["screaming"].play()
                self.stun = 50
                bee += 1
        return score, mosquito, bee
