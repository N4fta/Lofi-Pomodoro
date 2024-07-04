import sys, os, csv
from ast import literal_eval as make_tuple
import pygame as pg
import pygame_widgets as pgw
from pygame_widgets.slider import Slider
from pygame_widgets.dropdown import Dropdown
#from pygame_widgets.widget import WidgetBase
from myCustomClasses import BasicMenu, SettingsMenu, PomodoroTimer, blit_Text

pg.init()
size = width, height = 600, 900
screen = pg.display.set_mode(size)
pg.display.set_caption("Lo-fi Player")
# Taken from "https://icons8.com/icon/bGr7rgstoSns/chillhop-music"
icon = pg.image.load("graphics/icons8-chillhop-music-64.png").convert_alpha()
pg.display.set_icon(icon)
clock = pg.time.Clock()

# Determines events, collisions, logic and rendering that is happening. Rest are ignored
gameState = 3 # Settings = 1, PauseMenu = 2, Running = 3
timerRunning = True
timerState = 1 # Focus = 1, Break = 0
exitMainLoop = False

# Background & Foreground
pg.time.set_timer(pg.USEREVENT+1,100,-1) # Timer for gif, runs at 10 frames per second
animationFrame = 0 # For Gifs
pg.time.set_timer(pg.USEREVENT+2,1000,-1) # Timer for pomodoro clock, creates an event every 1 second => we update the clock every second
mainTextRenderer = pg.font.Font('fonts/Pixeltype.ttf',80)

# Integrated fadeout to keep background dynamic
newScene = None
fadeoutAlpha = 0
MAX_FADEOUT_ALPHA = 130  # Determines how transparent menus are
maxFadeoutAlpha = MAX_FADEOUT_ALPHA
newGameState = 3

# Defaults and preferences
musicName = "coffee-chill-out"
musicVolume = 0.5
soundtrackName = "rain"
soundtrackVolume = 0.3
backgroundName = "rainy_scene"
focusTime = [0,25,0]
breakTime = [0,5,0]
if os.path.exists("settingsPreferences.csv"):
    with open("settingsPreferences.csv", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            if line[0] == "MusicName": musicName = line[1]
            if line[0] == "MusicVolume": musicVolume = float(line[1])
            if line[0] == "SountrackName": soundtrackName = line[1]
            if line[0] == "SountrackVolume": soundtrackVolume = float(line[1])
            if line[0] == "BackgroundName": backgroundName = line[1]
            if line[0] == "TimerFocus": focusTime = make_tuple(line[1])
            if line[0] == "TimerBreak": breakTime = make_tuple(line[1])

# Clock stuff
pomodoroTimer = PomodoroTimer(focusTime, breakTime)
clockDisplay = mainTextRenderer.render(pomodoroTimer.timerDisplay(), False, "white")
user_input: str = None
user_input_rect = clockDisplay.get_rect()

# Music and Soundtrack
music = pg.mixer.Sound(f"audio/music/{musicName}.mp3")
music.set_volume(musicVolume)
music.play(-1, fade_ms=10000)
soundTrack = pg.mixer.music
soundTrack.load(f"audio/soundtrack/{soundtrackName}.mp3") # Rain SoundTrack is loaded as stream since files can be bigger (15 mins long)
soundTrack.set_volume(soundtrackVolume)
soundTrack.play(-1, fade_ms=5000)

# Menus
menuTextRenderer = pg.font.Font('fonts/Pixeltype.ttf',90)
BLUE = (20, 101, 173)

# Pause Menu
pauseMenu_Resume = menuTextRenderer.render("Resume", False, "white")
pauseMenu_Settings = menuTextRenderer.render("Settings", False, "white")
pauseMenu_Quit = menuTextRenderer.render("Quit", False, "white")
pauseMenu = BasicMenu(screen, [pauseMenu_Resume, pauseMenu_Settings, pauseMenu_Quit])

# Settings Menu
settingsMenu_Scene = screen.copy()
# Sliders
SLIDER_HEIGHT = 30
SLIDER_WIDTH = int(screen.get_width()*0.8)
SLIDER_X = (screen.get_width()-SLIDER_WIDTH)/2
settingsMenu_MusicVolume = menuTextRenderer.render("Music Volume", False, "white")
settingsMenu_MusicVolumeSlider = Slider(settingsMenu_Scene, SLIDER_X,0,SLIDER_WIDTH, SLIDER_HEIGHT,
                                         min=0, max=100, step=1, initial=musicVolume*100)
settingsMenu_SountrackVolume = menuTextRenderer.render("Sountrack Volume", False, "white");
settingsMenu_SountrackVolumeSlider = Slider(settingsMenu_Scene, SLIDER_X,0,SLIDER_WIDTH, SLIDER_HEIGHT,
                                             min=0, max=100, step=1, initial=soundtrackVolume*100)
# Dropdowns
DROPDOWN_HEIGHT = 60
DROPDOWN_WIDTH = int(screen.get_width()*0.80)
DROPDOWN_X = (screen.get_width()-DROPDOWN_WIDTH)/2
songs = []
for filename in os.listdir("audio/music"):
    songs.append(filename.split(".")[0])
settingsMenu_MusicDropdown = Dropdown(settingsMenu_Scene, DROPDOWN_X,0,DROPDOWN_WIDTH, DROPDOWN_HEIGHT, name="Music",
                                       choices=songs, font=pg.font.Font('fonts/Pixeltype.ttf',50), textColour=pg.Color("black"),
                                       pressedColour=pg.Color("white"))
soundtracks = []
for filename in os.listdir("audio/soundtrack"):
    soundtracks.append(filename.split(".")[0])
settingsMenu_SoundtrackDropdown = Dropdown(settingsMenu_Scene, DROPDOWN_X,0,DROPDOWN_WIDTH, DROPDOWN_HEIGHT, name="Rain Soundtrack",
                                       choices=soundtracks, font=pg.font.Font('fonts/Pixeltype.ttf',50), textColour=pg.Color("black"),
                                       pressedColour=pg.Color("white"))
backgrounds = []
for filename in os.listdir("graphics/backgrounds"):
    backgrounds.append(filename)
settingsMenu_BackgroundDropdown = Dropdown(settingsMenu_Scene, DROPDOWN_X,0,DROPDOWN_WIDTH, DROPDOWN_HEIGHT, name="Background",
                                       choices=backgrounds, font=pg.font.Font('fonts/Pixeltype.ttf',50), textColour=pg.Color("black"),
                                       pressedColour=pg.Color("white"))
# Regular Text
settingsMenu_Return = menuTextRenderer.render("Return", False, "white");
settingsMenu = SettingsMenu(settingsMenu_Scene, [settingsMenu_MusicDropdown,
                                                settingsMenu_MusicVolume, settingsMenu_MusicVolumeSlider,
                                                settingsMenu_SoundtrackDropdown,
                                                settingsMenu_SountrackVolume, settingsMenu_SountrackVolumeSlider,
                                                settingsMenu_BackgroundDropdown,
                                                settingsMenu_Return])

while not exitMainLoop:
    # Events
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            exitMainLoop = True
        if event.type == pg.USEREVENT+1: # Background
                    animationFrame = animationFrame + 1

        match gameState:
            case 1: # Game Settings
                # Music Settings
                newMusic = None
                if settingsMenu_MusicDropdown.getSelected() and settingsMenu_MusicDropdown.getSelected() != musicName:
                    try:
                        newMusic = pg.mixer.Sound(f"audio/music/{settingsMenu_MusicDropdown.getSelected()}.mp3")
                    except:
                        1
                if newMusic:
                    music.stop()
                    music = newMusic
                    musicName = settingsMenu_MusicDropdown.getSelected()
                    music.set_volume(0.5)
                    music.play(-1, fade_ms=3000)
                    #settingsMenu_MusicDropdown.reset()
                music.set_volume(settingsMenu_MusicVolumeSlider.getValue()/100)

                # Soundtrack Settings
                if settingsMenu_SoundtrackDropdown.getSelected() and settingsMenu_SoundtrackDropdown.getSelected() != soundtrackName:
                    try:
                        soundTrack.stop()
                        soundTrack.load(f"audio/soundtrack/{settingsMenu_SoundtrackDropdown.getSelected()}.mp3")
                        soundtrackName = settingsMenu_SoundtrackDropdown.getSelected()
                        soundTrack.play(-1,fade_ms=2000)
                    except:
                        1
                soundTrack.set_volume(settingsMenu_SountrackVolumeSlider.getValue()/100)

                # Background Settings
                if settingsMenu_BackgroundDropdown.getSelected() and settingsMenu_BackgroundDropdown.getSelected() != backgroundName:
                    backgroundName = settingsMenu_BackgroundDropdown.getSelected()

                # Back
                if event.type == pg.MOUSEBUTTONDOWN:
                    pressed = pg.mouse.get_pressed()
                    mousePoints = pg.mouse.get_pos()
                    if (settingsMenu.menuElements[-1].collidepoint(mousePoints) and pressed[0]) or pressed[2] == True: # Back
                        gameState = 2
                        #newScene = pauseMenu.display() removed fade because of issues with fading between transparent scenes
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        gameState = 2
                        #newScene = pauseMenu.display()

            case 2: # Game Paused
                if event.type == pg.MOUSEBUTTONDOWN:
                    pressed = pg.mouse.get_pressed()
                    mousePoints = pg.mouse.get_pos()
                    if pressed[0]: # Left mouse click
                        if pauseMenu.menuSprites[0].collidepoint(mousePoints): # Resume
                            newGameState = 3
                            newScene = rainy_scene_1
                        elif pauseMenu.menuSprites[1].collidepoint(mousePoints): # Settings
                            gameState = 1
                            #newScene = settingsMenu.display() removed fade because of issues with fading between transparent scenes
                        elif pauseMenu.menuSprites[2].collidepoint(mousePoints): # Quit
                            exitMainLoop = True
                    elif pressed[2] == True: # Right mouse click
                        newGameState = 3
                        newScene = rainy_scene_1
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        newGameState = 3
                        newScene = rainy_scene_1

            case 3: # Game Running
                # User Input Check
                if event.type == pg.MOUSEBUTTONDOWN:
                    pressed = pg.mouse.get_pressed()
                    if pressed[2] == True: # Go to Pause Menu
                        newGameState = 2
                        newScene = pauseMenu.display()
                    if pressed[0] == True:
                        if user_input_rect.collidepoint(pg.mouse.get_pos()) and user_input == None: # Activate input listening
                            user_input = ""
                            timerRunning = False # Pause Timer

                # Clock update
                if event.type == pg.USEREVENT + 2:
                    if timerRunning:
                        if pomodoroTimer.increaseTimer([1,0,0]):
                            timerState = (timerState + 1) % 2
                            pomodoroTimer.changeActiveLimit()
                            pomodoroTimer.resetTimer()
                        clockDisplay = mainTextRenderer.render(pomodoroTimer.timerDisplay(),False,"White")

                # Pause Menu
                if event.type == pg.KEYDOWN:
                    if user_input != None: # If user clicked on textbox
                        # This mess exists because I want to characters the program picks up 
                        if event.key == pg.K_BACKSPACE:
                            user_input = user_input[:-1]
                        elif event.key == pg.K_0 or event.key == pg.K_KP0:
                            user_input += "0"
                        elif event.key == pg.K_1 or event.key == pg.K_KP1:
                            user_input += "1"
                        elif event.key == pg.K_2 or event.key == pg.K_KP2:
                            user_input += "2"
                        elif event.key == pg.K_3 or event.key == pg.K_KP3:
                            user_input += "3"
                        elif event.key == pg.K_4 or event.key == pg.K_KP4:
                            user_input += "4"
                        elif event.key == pg.K_5 or event.key == pg.K_KP5:
                            user_input += "5"
                        elif event.key == pg.K_6 or event.key == pg.K_KP6:
                            user_input += "6"
                        elif event.key == pg.K_7 or event.key == pg.K_KP7:
                            user_input += "7"
                        elif event.key == pg.K_8 or event.key == pg.K_KP8:
                            user_input += "8"
                        elif event.key == pg.K_9 or event.key == pg.K_KP9:
                            user_input += "9"
                        elif event.key == pg.K_COLON or event.key == pg.K_SEMICOLON:
                            user_input += ":"
                        elif event.key == pg.K_ESCAPE:
                            # Returns to previous state
                            user_input = None
                            timerRunning = True
                        elif event.key == pg.K_RETURN:
                            # Parses and Saves timer
                            newTimer = [0,0,0]
                            listInput = user_input.split(':')
                            if len(listInput) > 3 or listInput[0] == '': break
                            listInput.reverse()
                            for i in range(0,len(listInput)):
                                if listInput[i] == '': newTimer[i] = 0
                                else: newTimer[i] = int(listInput[i])
                            newTimer = pomodoroTimer.standardize(newTimer)
                            pomodoroTimer.activeLimit[0] = newTimer[0]
                            pomodoroTimer.activeLimit[1] = newTimer[1]
                            pomodoroTimer.activeLimit[2] = newTimer[2]
                            # Returns to previous state
                            user_input = None
                            pomodoroTimer.resetTimer()
                            timerRunning = True

                    elif event.key == pg.K_ESCAPE: # Only if not in text input mode
                        newGameState = 2
                        newScene = pauseMenu.display()


    # Logic
    match gameState:
        case 1: # Game Settings
            1
        case 2: # Game Paused
            1
        case 3: # Game Running
            1

    # Background
    try:
        rainy_scene_1 = pg.image.load(f"graphics/backgrounds/{backgroundName}/frame_{animationFrame}.gif").convert() # Try to load frame
    except:
        # If it fails there are no more frames, reset to beginning
        # This makes it work with any number of frames but seems inefficient
        animationFrame = 0 
        rainy_scene_1 = pg.image.load(f"graphics/backgrounds/{backgroundName}/frame_{animationFrame}.gif").convert()
    rainy_scene_1 = pg.transform.scale(rainy_scene_1, (width,height), screen)


    # Additional Rendering
    match gameState:
        case 1: # Game Settings
            settingsMenu_Scene = settingsMenu.display()
            settingsMenu_Scene.set_alpha(maxFadeoutAlpha)
            screen.blit(settingsMenu_Scene, (0, 0))
        case 2: # Game Paused
            pauseMenu_Scene = pauseMenu.display()
            pauseMenu_Scene.set_alpha(maxFadeoutAlpha)
            screen.blit(pauseMenu_Scene, (0, 0))
        case 3: # Game Running
            
            # Clock
            if user_input == None:
                clockRect = clockDisplay.get_rect()
                clockRect.centerx = width/2
                clockRect.centery = height/4
                screen.blit(clockDisplay, clockRect)
                user_input_rect = clockRect

            # User Input
            else:
                user_text = mainTextRenderer.render(user_input,False,"White")
                user_input_rect = user_text.get_rect()
                user_input_rect.centerx = width/2
                user_input_rect.centery = height/4
                screen.blit(user_text, user_input_rect)

            # Messages
            if timerState == 1: # Focus
                blit_Text(screen, "Focus, you're \n almost there", (width*0.25,height*0.60), mainTextRenderer)
            if timerState == 0: # Break
                blit_Text(screen, "Take a break\n You deserve it", (width*0.22,height*0.60), mainTextRenderer)

    # Fade overwrites current scene
    if newScene:
        if newScene == rainy_scene_1: # Fadein if we are returning to main scene
            timerRunning = True
            maxFadeoutAlpha -= 2 # Increase transparency of other displayed scene
            if maxFadeoutAlpha <= 0: # End of fadeout
                maxFadeoutAlpha = MAX_FADEOUT_ALPHA # Resets maxFadeoutAlpha
                newScene = None
                gameState = newGameState
        else: # Fadeout
            timerRunning = False
            fadeoutAlpha += 2
            newScene.set_alpha(fadeoutAlpha)
            screen.blit(newScene, (0, 0))
            if fadeoutAlpha >= maxFadeoutAlpha: # End of fadeout
                fadeoutAlpha = 0
                newScene = None
                gameState = newGameState

    pgw.update(events)
    pg.display.flip()
    clock.tick(60) # Limits speed to 60 frames per second

# Write preferences to a file
with open("settingsPreferences.csv", "w", newline='') as csvfile:
    csvWrite = csv.writer(csvfile)
    csvWrite.writerow(["MusicName", musicName])
    csvWrite.writerow(["MusicVolume", settingsMenu_MusicVolumeSlider.getValue()/100])
    csvWrite.writerow(["SountrackName", soundtrackName])
    csvWrite.writerow(["SountrackVolume", settingsMenu_SountrackVolumeSlider.getValue()/100])
    csvWrite.writerow(["BackgroundName", backgroundName])
    csvWrite.writerow(["TimerFocus", pomodoroTimer.focusLimit])
    csvWrite.writerow(["TimerBreak", pomodoroTimer.breakLimit])
                
pg.quit()
sys.exit()