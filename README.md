# Sunrise Sunset to Google Calendar, built with AI
As part-plant part-human, I wanted to plan my days with the sunrise and sunset times in mind to make the most out of the time the sun is in the sky. The  options are…
1. WebCal Guru (starting at 7,95€ per year), or 
2. ask AI to generate a CSV with the sunrise and sunset time of your location then import it into you Google Calendar. 


Rather than pay or have to deal with the manual/clunky CSV approach, I took this opportunity to learn
- how to build and refine my code with AI
- how to set up and use Google Calendar API

## What I did
It took ~3 hours to go from installing Python onto my computer to successfully running the script that created the sunrise and sunset Google Calendar events for the first time. I spent another 20 minutes debugging and I'm ecstatic to share the final result. 

I started with Lovable Base Prompt in Voice Mode and dicated what I wanted. Then with Voice Mode running in the background, I navigated to Google Cloud Project, followed Lovable's Voice Mode to click and fill out fields as required. Then Lovable Voice walked me through installing Python, the virtual environment, understanding and setting up Google OAuth, then generated a script that creates Google Calendar events!

I ran out ouf Lovable credits so I moved to regular ChatGPT and then Gemini. From previous attempts at building a mobile app and listening to Lenny's Podcast featuring Lazar Jovanovic and Zevi Arnovitz, I knew I had to build my Product Requirements Document (PRD). For every error, I asked Gemini to tell me what broke, how to fix it, and what to append to my PRD so that I instruct the LLM-software-developer to update my `main.py` file. After each update, I copied and pasted the whole script into the file — no manual coding required. 

# How to use

Download the `main.py` file, download Python, set up Google OAuth and any missing dependencies, then run the script! 

## Dependencies

You'll need:
* google-api-python-client
* google-auth-oauthlib
* google-auth-httplib2
* astral>=2.2
* geopy
* python-dateutil
* timezonefinder
* pytz

## Command

In Command Prompt, navigate to the directory where main.py is saved and run any four of the following commands:

```
python main.py “City, Country”  
python main.py “City, Country” yyyy-mm-dd  
python main.py “City, Country” ## 
python main.py “City, Country” yyyy-mm-dd ##
```

Where…\
         `“City, Country”` = mandatory because it creates the sub-calendar\
    `yyyy-mm-dd` = is the date that the events begin, default is today\  
    `##` = is the number of days worth of events to create, default is 365
