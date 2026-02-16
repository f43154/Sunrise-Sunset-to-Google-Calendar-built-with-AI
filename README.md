# Sunrise Sunset to Google Calendar, built with AI
As part-plant part-human, I wanted to plan my days around the sun. I needed my calendar to reflect exactly when the sun rises and sets in my location, and have the option to add different locations. 

To do this, I could have used
1. WebCal Guru which costs 7,95€ per year, or 
2. manual AI generation like asking an LLM for a CSV and manually importing it (clunky, repetitive)


Rather than paying or settle for a manual approach, I used this opportunity to learn
- how to build and refine my code with AI
- how to set up and use Google Calendar API

## How It Works

This script takes in the city and country then populates the sunset and sunrise times as Google Calendar events.

![gif of demo](https://github.com/f43154/Sunrise-Sunset-to-Google-Calendar-built-with-AI/blob/main/demo-gif-compressed.gif)

## Build Journey
It took approximately 3 hours to go from installing Python onto my computer to the first successful script execution. I spent another 20 minutes debugging and I'm ecstatic to share the final result. 

I built this using a "human-in-the-loop" AI approach: 

1. Ideation: Dictated (aka braindump) the initial concept using Lovable Voice Mode, a la Lazar Jovanovic.
2. Infrastructure: Followed AI-voice-guided instructions to set up a Google Cloud Project and configure Google OAuth.
3. Refinement: When I ran out of credits, I moved to Gemini. I maintained a Product Requirements Document (PRD) to continuously improve the context I provide to the LLM.
4. Debugging: For every error, I asked the AI to explain the break, provide a fix, and update the PRD to ensure the `main.py` remained robust.

**The best part?** I didn't write a single line of manual code. I orchestrated the logic, and the AI handled the syntax.

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
`yyyy-mm-dd` = is the date that the events begin, default is today  
`##` = is the number of days worth of events to create, default is 365
