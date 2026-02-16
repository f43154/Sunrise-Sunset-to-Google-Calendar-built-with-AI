# I am building a custom Google Calendar that has two events each day for the sunrise and sunset time of a given city.  

## Initial Features to include (v1):  
* create events in Google Calendar using either of the following in Command Prompt
      * python main.py "Paris, France"
      * python main.py "Paris, France" 2026-02-28  
      * python main.py "Paris, France" 2026-02-28 30
      * python main.py "Paris, France" 30
* by default with no user input of number of days, main.py will create 365 days worth of sunrise and sunset times
* by default with no user input of date in yyyy-mm-dd, main.py will create events starting from today
* events are always in the same time zone as the city of the respective sunrise/sunset times
* the sunrise Google calendar event starts and ends according to that morning's Civil twilight, for example today that will be 07:24 - 07:56 
* the sunrise Google calendar event will have the following name: "☀️Sunrise in Paris" where Paris is the city name that gets substituted when running the file and the user is providing the city, country name 
* the sunrise Google calendar event will have the following in the description: 
      * Astronomical Twilight: start and end time (in the morning)
      * Nautical Twilight: start and end time (in the morning)
      * Civil Twilight: start and end time (in the morning)
      * ☀️Sunrise: time
      * Golden Hour: start and end time 
      * Zenith:  time 
      * Golden Hour: start and end time (in the evening)
      * 🌅Sunset: time
      * Civil Twilight: start time, end time (in the evening)
      * Nautical Twilight (in the evening) start time, end time (in the evening)
      * Astronomical Twilight: start time, end time (in the evening)
      * one blank lines then the Length of day: duration of how long the sun is above the horizon in hours and minutes

## Tech and credentials already installed on my computer: 
* Python 3 installed
* have a virtual environoment named gcal-sunrise-sunset
* already completede Google OAuth authenticaiton and can create events from Python
* installed geopy, astral, dateutil, timezonefinder
* Astral v2 changed its API and the Sun class no longer exists and twilights are computed differently, 
      * so use astral.sun.sun() to get sunrise, sunset, dawn, dusk, etc. 
      * you do not import Sun or twilight.

##**Task**: Prepare the main.py file that I will run on Command Prompt

## Additional Technical Requirements (v1.1)
* **Calendar Management**: The application must not write to the user's primary calendar. It must search for a calendar titled "Sunrise/Sunset in [City]" and create it if it does not exist.
* **Formatting**: The description must use HTML tags (`<b>`) for the Sunrise and Sunset lines to ensure visual emphasis in the Google Calendar UI.
* **Data Accuracy**: Twilights (Astronomical and Nautical) are calculated as 30-minute intervals relative to the Civil Twilight bounds provided by the Astral `sun()` method.

## Additional Technical Requirements (v1.2)
The event description must match the following structural and stylistic requirements based on the provided "gcal sunrise after.PNG":
* **Remove Parentheticals**: Remove the text in parentheses like "(morning)", "(evening)", and the duration strings (e.g., "(0h 30m)") from the twilight and golden hour lines.
* **Sunrise/Sunset Formatting**: Use the format `[Emoji] **[Phase] @ [HH:MM]**`. For example: `☀️ **Sunrise @ 07:35**`.
* **Simplify Twilight Labels**: Labels should simply be "Astronomical Twilight", "Nautical Twilight", and "Civil Twilight" without extra descriptors.
* **Spacing**: Ensure there is exactly one blank line before the "Length of daylight" section.

## Strict Command Line Argument Handling (v1.3)
To prevent the script from generating more days than requested, the argument parsing logic must be modernized:
* **Priority Logic**: The script must strictly identify arguments by their type. If an argument is a valid YYYY-MM-DD string, it is the `start_date`. If an argument is a standalone integer, it MUST override the `num_days` default.
* **Loop Constraint**: The for-loop generating events must strictly iterate exactly `num_days` times, starting from the `start_date`.
* **Validation**: If a user provides `python main.py "City" 2026-02-18 4`, the script must generate exactly 8 events total (4 sunrises, 4 sunsets).

## Leveraging Astral Library's precise solar depression angles (v1.4)
* **Precise Twilight Calculations**: Do not use hardcoded offsets (e.g., +/- 30 minutes). Instead, use the Astral library's `dawn()` and `dusk()` methods with explicit depression angles:
    * **Astronomical Twilight**: 18.0 degrees
    * **Nautical Twilight**: 12.0 degrees
    * **Civil Twilight**: 6.0 degrees (default for `dawn`/`dusk`)
* **Golden Hour**: Calculated as the time period when the sun is between -4.0 degrees and 6.0 degrees elevation.
* **Zenith**: Use the `noon()` method from Astral to identify the point of maximum solar elevation.
* **Structural Stylistic Requirements**:
    * **Remove Parentheticals**: No "(morning)", "(evening)", or duration strings like "(0h 30m)".
    * **Time Format**: Use `[Emoji] **[Phase] @ [HH:MM]**` (e.g., `☀️ **Sunrise @ 07:35**`).
    * **Spacing**: Ensure exactly one blank line exists between the twilight list and the "Length of daylight" section.

## Dependency & Environment Specifications (v1.5)
* **Astral Versioning**: The code must strictly adhere to Astral v2.x or higher syntax.
* **Case Sensitivity**: All class imports (e.g., Observer, LocationInfo) must follow Python's PEP 8 naming conventions (PascalCase for classes) to ensure compatibility across different OS environments.
* **Strict Type Imports**: Explicitly import classes from the top-level package (e.g., from astral import Observer) rather than submodules to avoid internal library path changes.

## Error Handling & Validation (v1.6)

### Robust Astronomical Calculations
* **Handle "Never Occurs" Scenarios**: The script must account for dates and locations where specific solar events (like Astronomical or Nautical twilight) do not occur (e.g., Paris in mid-summer). 
* **Implementation**: Wrap calls to `dawn()` and `dusk()` in a way that catches `ValueError`. 
* **Fallback Behavior**: If a specific twilight phase does not occur on a given day, the description should display "N/A" for that specific time range instead of failing. This ensures the 365-day loop completes even during solstice periods.

### Strict Input Validation
* **Mandatory Location**: The script must strictly require a "City, Country" string as the first argument.
* **Termination Logic**: 
    * If no arguments are provided, or if the first argument does not appear to contain a city and country (e.g., missing a comma or being an empty string), the script must print a clear usage error message and exit immediately.
    * No Google Calendar API calls (searching for or creating calendars) should be performed until the location input is validated and geocoded successfully.
 