import pygame as pg
from pygame_widgets.widget import WidgetBase

class BasicMenuSprite(pg.sprite.Sprite):
    def __init__(self, image: pg.surface.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.hidden = False
    
    def get_heigth(self) -> int:
        return self.rect.height

    def get_rect(self) -> pg.Rect:
        return self.rect

    def updateRect(self, rect: pg.Rect):
        self.rect = rect

    def hideme(self):
        self.hidden = True
    
    def unhideme(self):
        self.hidden = False

    def blitme(self, screen: pg.Surface):
        if not self.hidden:
            screen.blit(self.image, self.rect)

    def collidepoint(self, points: tuple[float, float]) -> bool:
        return self.rect.collidepoint(points[0],points[1])


# Modular, spaced based on amount of lines
class BasicMenu():
    def __init__(self, screen: pg.Surface, MenuElements: list[pg.Surface]):
        self.mainScreen = screen
        self.menuSprites: list[BasicMenuSprite] = []
        for element in MenuElements:
            sprite = BasicMenuSprite(element)
            self.menuSprites.append(sprite)

    def display(self, color = (20, 101, 173)) -> pg.Surface:
        pauseScreen = self.mainScreen.copy()
        pauseScreen.fill(color) # Default is Blue

        padding = (pauseScreen.get_height() / len(self.menuSprites))/2
        # Trying to center menu better 
        #if padding > self.menuSprites[0].get_heigth(): padding = self.menuSprites[0].get_heigth()

        for i in range(0,len(self.menuSprites)):
            sprite = self.menuSprites[i]
            rect = sprite.get_rect()
            rect.centerx = pauseScreen.get_width()/2
            if i==0:  rect.centery = padding*1
            else: rect.centery = padding*(2*i+1)

            sprite.blitme(pauseScreen)
        return pauseScreen
        
# Too complex & different to account for all parameters, menu elements are declared in class
class SettingsMenu():
    def __init__(self, settingsScene: pg.Surface, MenuElements: list[pg.Surface | WidgetBase]):
        self.settingsScene = settingsScene
        self.menuElements: list[BasicMenuSprite | WidgetBase] = []
        for element in MenuElements:
            if type(element) is pg.Surface:
                self.menuElements.append(BasicMenuSprite(element))
            else: self.menuElements.append(element)

    def display(self, color = (20, 101, 173)) -> pg.Surface:
        self.settingsScene.fill(color) # Default is Blue

        padding = (self.settingsScene.get_height() / len(self.menuElements))/2

        for y in range(0,len(self.menuElements)):
            # Reversing order to see it dropdown shows up on top
            # IT WORKEEDD!! LEZZ GOOO
            i = len(self.menuElements)-y-1
            element = self.menuElements[i]

            # If element is a widget, adjust differently
            if type(element) is BasicMenuSprite:
                rect = element.get_rect()
                if i==0: 
                    rect.centery = padding*1
                else:
                    rect.centery = padding*(2*i+1)

                rect.centerx = self.settingsScene.get_width()/2
                element.blitme(self.settingsScene)
            else:
                if i==0: 
                    element.setY(int(padding*1))
                else:
                    element.setY(int(padding*(2*i)))

                # Since widgets are aligned at the top-left corner only x is set at start-up
                element.draw()

        return self.settingsScene
        
class PomodoroTimer():
    # Tuble in form [seconds, minutes, hours]
    def __init__(self, focusTime: tuple[int, int, int], breakTime: tuple[int, int, int]):
        
        self.focusLimit = [0,0,0]
        focusTime1 = self.standardize(focusTime)
        for i in range(0,3): self.focusLimit[i] += focusTime1[i]

        self.breakLimit = [0,0,0]
        breakTime1 = self.standardize(breakTime)
        for i in range(0,3): self.breakLimit[i] += breakTime1[i]

        self.activeLimit = self.focusLimit

        self.timer = [0,0,0]

    def changeActiveLimit(self):
        if self.activeLimit == self.focusLimit: self.activeLimit = self.breakLimit
        else: self.activeLimit = self.focusLimit

    def activeLimitDisplay(self) -> str:
        if self.activeLimit[2] != 0:
            timeDisplay =  f"{self.activeLimit[2]}:{self.activeLimit[1]}:"
            if self.activeLimit[0]<10: timeDisplay += f"0{self.activeLimit[0]}"
            else: timeDisplay += self.activeLimit[0]
            return timeDisplay
        else:
            timeDisplay = f"{self.activeLimit[1]}:"
            if self.activeLimit[0]<10: timeDisplay += f"0{self.activeLimit[0]}"
            else: timeDisplay += f"{self.activeLimit[0]}"
            return timeDisplay

    # Increases timer by x and returns a bool indicating if time has exceeded limit
    def increaseTimer(self, timeAdd:tuple[int, int, int]) -> bool:

        timeAdd1 = self.standardize(timeAdd)
        for i in range(0,3): self.timer[i] += timeAdd1[i]
        self.timer = self.standardize(self.timer)
        # Check if time exceeds limit
        timerOver = True
        for i in range(0, len(self.timer)):
            if self.timer[i] < self.activeLimit[i]:
                timerOver = False
                break
        return timerOver

    def timeLeft(self) -> tuple[int, int, int]:
        return [self.activeLimit[0] - self.timer[0], self.activeLimit[1] - self.timer[1], self.activeLimit[2] - self.timer[2]]
    
    def timerDisplay(self) -> str:
        if self.timer[2] != 0:
            timeDisplay =  f"{self.timer[2]}:{self.timer[1]}:"
            if self.timer[0]<10: timeDisplay += f"0{self.timer[0]}"
            else: timeDisplay += self.timer[0]
            return timeDisplay
        else:
            timeDisplay = f"{self.timer[1]}:"
            if self.timer[0]<10: timeDisplay += f"0{self.timer[0]}"
            else: timeDisplay += f"{self.timer[0]}"
            return timeDisplay
    
    def resetTimer(self):
        self.timer = [0,0,0]

    # Converts seconds to minutes and minutes to hours if they exceed 60
    def standardize(self, time: tuple[int, int, int]) -> tuple[int, int, int]:
        time1 = [0,0,0]
        for i in range(0,2):
            time1[i] += time[i]%60
            if time[i]/60 >= 1:
                time1[i+1] += int(time[i]/60)
        time1[2] += time[2]
        return time1
    
def blit_Text(screen: pg.Surface, text: str, pos: tuple[int,int], font: pg.font.Font, color=pg.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = screen.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.