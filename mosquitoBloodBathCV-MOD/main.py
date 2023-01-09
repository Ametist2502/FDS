# Setup Python ----------------------------------------------- #
import pygame
import argparse
import sys
import os
import pandas as pd
from settings import *
from game import Game   
from menu import Menu


parser = argparse.ArgumentParser("Args parser for game options")
parser.add_argument("--playerName", default="Do Quang Manh", help="Player Name")
parser.add_argument("--playerYear", default="K15")
parser.add_argument("--playerMajor", default="AI", type=str)
parser.add_argument("--MSSV", default="HE153129", type=str)
parser.add_argument("--main_csv_file", default="data/dataTrack.csv")
opt = parser.parse_args()

dataIndividualDict = {
    'HoTen': [],
    'Khoa': [],
    'Nganh': [],
    'MSSV': [],
    'Mosquito': [],
    'Bee': [],
    'Score': [],
    'Option': [],
}

dataDict = pd.read_csv(opt.main_csv_file).to_dict('list')


# Setup pygame/window --------------------------------------------- #
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,32) # windows position
pygame.init()
pygame.display.set_caption(WINDOW_NAME)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

mainClock = pygame.time.Clock()

# Fonts ----------------------------------------------------------- #
fps_font = pygame.font.SysFont("coopbl", 22)

# Music ----------------------------------------------------------- #
pygame.mixer.music.load("Assets/Sounds/Komiku_-_12_-_Bicycle.mp3")
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)
# Variables ------------------------------------------------------- #
state = "menu"

# Creation -------------------------------------------------------- #
game = Game(SCREEN)
menu = Menu(SCREEN)



# Functions ------------------------------------------------------ #
def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def update():
    global state
    if state == "menu":
        if menu.update() == "game":
            game.reset() # reset the game to start a new game
            state = "game"
        elif menu.update() == "test":
            game.reset() # reset the game to start a new game
            state = "test"
    elif state == "game" or state == "test":
        if game.update() == "menu":
            dataDict['HoTen'].append(opt.playerName)
            dataDict['Khoa'].append(opt.playerYear)
            dataDict['Nganh'].append(opt.playerMajor)
            dataDict['MSSV'].append(opt.MSSV)
            dataDict['Score'].append(game.score)
            dataDict['Mosquito'].append(game.mosquito)
            dataDict['Bee'].append(game.bee)
            dataDict['Option'].append("play" if state=="game" else "test")
            df = pd.DataFrame(dataDict,)
            os.makedirs('data', exist_ok=True)
            df.to_csv(opt.main_csv_file, index=False)

            dataIndividualDict['HoTen'].append(opt.playerName)
            dataIndividualDict['Khoa'].append(opt.playerYear)
            dataIndividualDict['Nganh'].append(opt.playerMajor)
            dataIndividualDict['MSSV'].append(opt.MSSV)
            dataIndividualDict['Score'].append(game.score)
            dataIndividualDict['Mosquito'].append(game.mosquito)
            dataIndividualDict['Bee'].append(game.bee)
            dataIndividualDict['Option'].append("play" if state=="game" else "test")
            df = pd.DataFrame(dataIndividualDict,)
            os.makedirs('data/individuals', exist_ok=True)
            save_file = f"data/individuals/{opt.playerMajor}_{opt.playerYear}_{opt.playerName}_{opt.MSSV}.csv"
            df.to_csv(save_file, index=False)
            state = "menu"
    pygame.display.update()
    mainClock.tick(FPS)



# Loop ------------------------------------------------------------ #
while True:

    # Buttons ----------------------------------------------------- #
    user_events()

    # Update ------------------------------------------------------ #
    update()

    # FPS
    if DRAW_FPS:
        fps_label = fps_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255,200,20))
        SCREEN.blit(fps_label, (5,5))

