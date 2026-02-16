import sys
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from astral import Observer
from astral.sun import sun, dawn, dusk, noon
from timezonefinder import TimezoneFinder
import pytz
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from geopy.geocoders import Nominatim

# ---- Google Calendar Setup ----
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('calendar', 'v3', credentials=creds)

service = get_service()

def get_or_create_calendar(city_name):
    city_short = city_name.split(',')[0].strip()
    calendar_name = f"Sunrise/Sunset in {city_short}"
    calendar_list = service.calendarList().list().execute()
    
    for entry in calendar_list.get('items', []):
        if entry['summary'] == calendar_name:
            return entry['id']
    
    new_calendar = {'summary': calendar_name}
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    return created_calendar['id']

def create_event(calendar_id, start_dt, end_dt, summary, description, tz):
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': tz},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': tz},
    }
    try:
        service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {summary} on {start_dt.date()}")
    except Exception as e:
        print(f"Error creating event: {e}")

def format_timedelta(td):
    hours, remainder = divmod(int(td.total_seconds()), 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes}m"

def safe_solar_time(func, obs, date, depression, tzinfo):
    """Handles cases where sun never reaches a certain depression (v1.6)."""
    try:
        dt = func(obs, date=date, depression=depression)
        return dt.astimezone(tzinfo)
    except (ValueError, TypeError):
        return None

def generate_description(obs, date, tzinfo):
    fmt = lambda dt: dt.strftime('%H:%M') if dt else "N/A"
    
    # Precise Twilight Calculations (v1.4)
    astro_m = safe_solar_time(dawn, obs, date, 18.0, tzinfo)
    naut_m  = safe_solar_time(dawn, obs, date, 12.0, tzinfo)
    civil_m = safe_solar_time(dawn, obs, date, 6.0, tzinfo)
    
    s = sun(obs, date=date)
    sunrise_dt = s['sunrise'].astimezone(tzinfo)
    sunset_dt = s['sunset'].astimezone(tzinfo)
    noon_dt = noon(obs, date=date).astimezone(tzinfo)
    
    civil_e = safe_solar_time(dusk, obs, date, 6.0, tzinfo)
    naut_e  = safe_solar_time(dusk, obs, date, 12.0, tzinfo)
    astro_e = safe_solar_time(dusk, obs, date, 18.0, tzinfo)
    
    # Golden Hour (-4.0 to 6.0 elevation)
    gh_m_s = safe_solar_time(dawn, obs, date, 4.0, tzinfo)
    gh_m_e = safe_solar_time(dawn, obs, date, -6.0, tzinfo)
    gh_e_s = safe_solar_time(dusk, obs, date, -6.0, tzinfo)
    gh_e_e = safe_solar_time(dusk, obs, date, 4.0, tzinfo)

    lines = [
        f"Astronomical Twilight: {fmt(astro_m)} - {fmt(naut_m)}",
        f"Nautical Twilight: {fmt(naut_m)} - {fmt(civil_m)}",
        f"Civil Twilight: {fmt(civil_m)} - {fmt(sunrise_dt)}",
        f"☀️ <b>Sunrise @ {fmt(sunrise_dt)}</b>",
        f"Golden Hour: {fmt(gh_m_s)} - {fmt(gh_m_e)}",
        f"Zenith: {fmt(noon_dt)}",
        f"Golden Hour: {fmt(gh_e_s)} - {fmt(gh_e_e)}",
        f"🌅 <b>Sunset @ {fmt(sunset_dt)}</b>",
        f"Civil Twilight: {fmt(sunset_dt)} - {fmt(civil_e)}",
        f"Nautical Twilight: {fmt(civil_e)} - {fmt(naut_e)}",
        f"Astronomical Twilight: {fmt(naut_e)} - {fmt(astro_e)}",
        "", 
        f"Length of daylight: {format_timedelta(s['sunset'] - s['sunrise'])}"
    ]
    return "\n".join(lines)

def main():
    # v1.6 Strict Input Validation
    args = sys.argv[1:]
    if not args or "," not in args[0]:
        print("Usage Error: Please provide location in 'City, Country' format.")
        print("Example: python main.py 'Paris, France' [start_date] [num_days]")
        sys.exit(1)

    city_input = args[0]
    start_date = datetime.today().date()
    num_days = 365

    # Priority Logic for Args (v1.3)
    for arg in args[1:]:
        if "-" in arg:
            try:
                start_date = parse_date(arg).date()
            except ValueError:
                pass
        elif arg.isdigit():
            num_days = int(arg)

    # Geocoding before any Calendar API calls (v1.6)
    geolocator = Nominatim(user_agent="sun_cal_app")
    location = geolocator.geocode(city_input)
    if not location:
        print(f"Error: Could not find location for '{city_input}'.")
        sys.exit(1)
    
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
    tzinfo = pytz.timezone(tz_str)
    
    # API calls only happen after successful validation
    calendar_id = get_or_create_calendar(city_input)
    city_short = city_input.split(',')[0].strip()
    obs = Observer(latitude=location.latitude, longitude=location.longitude)

    for i in range(num_days):
        current_date = start_date + timedelta(days=i)
        
        # Calculate base sun events
        s = sun(obs, date=current_date)
        
        # Define event bounds (Civil Twilight)
        # Using 6.0 depression for Civil Twilight start/end
        civil_m_start = dawn(obs, date=current_date, depression=6.0).astimezone(tzinfo)
        civil_e_end = dusk(obs, date=current_date, depression=6.0).astimezone(tzinfo)
        
        sunrise_time = s['sunrise'].astimezone(tzinfo)
        sunset_time = s['sunset'].astimezone(tzinfo)

        desc = generate_description(obs, current_date, tzinfo)

        # Create Sunrise Event (Civil Dawn to Sunrise)
        create_event(
            calendar_id,
            civil_m_start,
            sunrise_time,
            f"☀️Sunrise in {city_short}",
            desc,
            tz_str
        )

        # Create Sunset Event (Sunset to Civil Dusk)
        create_event(
            calendar_id,
            sunset_time,
            civil_e_end,
            f"🌅Sunset in {city_short}",
            desc,
            tz_str
        )

if __name__ == "__main__":
    main()