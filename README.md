## Overview

This is my first real pygame project. I spent a day following a 3-4 hour game tutorial previously, but this is the first time I went completely on my own, read documentation like a real dev and tried out whatever I wanted.
    
The original idea was extremely simple and could not even be considered a game. I wanted to simulate thunder in a rainy day when the user clicked the screen. However, since that seemed very lacking so I started by adding ambience, menus and a bunch of other stuff while hoping I could add something to it. Yes, I know I could have gone with a simple cliché, but I just could not get the thunder effect out of my head, it calls out to me...I must implement it! ...but somehow I ended up with a lo-fi music player XD. 

Feel free to use the code however you want, as a first year C# programmer I just wanted to see how different game development is, if I could do it and try to learn python along the way. 
To be honest, game development is hard. keeping everything in one loop is really complicated and forces you into tough positions, I implemented some code in ways I wish I did not have to. Also, python...python was a pain. The lack of types is great when you want to do something risky, not recommended or outside the norm but before I discovered Type hints it was a royal pain to find out methods and keep track of what objects are what types.

Anyways, thanks for reading my rant. Be sure to check out the [Credits](#Credits) bellow for the amazing artists whose art made helped me keep going when I was losing motivation.
Neo

## Original Idea
- Thunder simulation on click, use math function (pathfinding?)
- Normal rainy city in the background, people walking by, looking at the ground, subtle music playing, rain soundtrack.
- When you click mighty thunder strikes. The world freezes for a second, cut the music, people stop. they look into the distance (away from you).
- Ambience is key.


## Current Direction/To-do
- Five days max must be done by Sunday 05-07-2027.
- ~~More setting options (always on top, borderless, resizable?); learned lots from implementing new features.~~
- Learn Markdown tips.
- Make own widgets lib.
- Rain soundtracks credits


### Main Loop (Mix of 2):
- Lo-fi Player, Vertical window, Chill out.
- ~~Thunder or other visual effect on tap, add gameplay.~~
- Productivity app features? A timer maybe? Pomodoro style

## Conclusion
In the end I ran out of features to implement as well as steam. Its only Thursday but I believe the App is great as it is. I could polish it but then I would never be finished, and I would rather work on something more interesting. As for the Thunder idea as much as I would love to add it feels like it would ruin the app. 

This app is good enough for now, I learned a lot more than I expected and I would rather move on to a new project where I can _finally_ implement __MIGHTY PROCEDURAL THUNDER__ 

## Simple Guide
The app does not have a tutorial or explanation so here is a simple guide:
(This will only work if you have Python)
- Download the code from github, unzip it and open the resulting folder
- Open a terminal in that folder and run `pip install -r requirements.txt`
- Run `python main.py`
- Tapping `Esc` or right clicking with a mouse will bring you to the Pause Menu, doing this will pause the Timer.
- Here you can select Settings to edit them or return by tapping `Esc` or right clicking.
- In Settings you can choose your Rain Soundtrack, Music and adjust Volume of each independently.
- Once you are done you can return to the Pause Menu and from there to the Main screen.
- In the main screen you will see a timer going up every second.
- By left clicking it you will be able to type in an amount of time to set your timer.
- The input most be formatted as `00:00:00` as hours : minutes : seconds. Providing just a number `00` or two `00:00` will result in adding only seconds or minutes and seconds, respectively.
- All numbers will be counted. If you input `01:70:70` the timer will be `02:11:10`. Have fun with that, I know I did :P
- When the timer ends the message will change a new timer will start which you can also edit the same way
- These are the _Focus Timer_ and _Break Timer_, they come from the Pomodoro technique. Their defaults are 25min and 5min, respectively.
- Do not worry though, your settings will be saved and automatically loaded. This includes volume, soundtrack, music, background, and timer length.

And how to add your own backgrounds (animated or not), music and soundtracks:
- __Music__ - Add it to the `audio/music` folder, it must be an `.mp3` file and have no `.` in the name
- __Soundtrack__ - Add it to the `audio/soundtrack` folder, it must also be an `.mp3` file and also have no `.` in the name
- __Backgrounds__ - Since I wanted to have animated backgrounds this one is a bit more complicated. First create a folder with the name of your background in `graphics/backgrounds`. E.g. `graphics/backgrounds/night_sky` (it can contain spaces, I simply prefer them like this). Then inside you must have all the frames of your Bg. If its a static image simply name it `frame_0.gif`, yes it must be a `.gif` format. If you have more frames name them `frame_1.gif`, `frame_2.gif`, etc. As many as you want. If you use an online tool like [this one](https://ezgif.com/split) you can easily split your gifs into frames, convert them, resize them and more.



## Credits
- Icon from <a href="https://icons8.com/icon/bGr7rgstoSns/chillhop-music">Icons8.com</a>
- Music from Pixibay:
    - Coffee Chill Out by <a href="https://pixabay.com/users/romanbelov-25347333/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=15283">Roman Belov</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=15283">Pixabay</a>
    - Abstract Fashion Pop by <a href="https://pixabay.com/users/qubesounds-24397640/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=131283">Yurii Semchyshyn</a> from <a href="https://pixabay.com/music//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=131283">Pixabay</a>
    - Order by <a href="https://pixabay.com/users/comastudio-26079283/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=99518">Yurii Semchyshyn</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=99518">Pixabay</a>
- Background Art:
    - Rainy Day by <a href="https://www.deviantart.com/pixeljeff/art/Rainy-Day-640373144">pixeljeff</a>
    - Rainy Castle by <a href="https://steamcommunity.com/sharedfiles/filedetails/?id=803160112">Nathan</a>
- Rain Sountracks from Pixibay:
    - Light Rain by <a href="https://pixabay.com/users/liecio-3298866/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=109591">LIECIO</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=109591">Pixabay</a>
    - Rain by <a href="https://pixabay.com/users/donrain-26735743/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=110508">Franco Gonzalez</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=110508">Pixabay</a>
    - Rain on the window by <a href="https://pixabay.com/users/donrain-26735743/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=114709">Franco Gonzalez</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=114709">Pixabay</a>
    - Indoor Hard Rain by <a href="https://pixabay.com/users/u_m17uwtnjmh-42333415/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=190883">u_m17uwtnjmh</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=190883">Pixabay</a>
    - Rain Sound by <a href="https://pixabay.com/users/avion_mood-39857343/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=188158">Vladislav Kim</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=188158">Pixabay</a>