import requests
from datetime import datetime, timedelta
import ephem
import unicodedata

def get_country_list():
    return [
        'AL', 'AD', 'AT', 'BY', 'BE', 'BG', 'HR', 'CZ', 'EE', 'FR', 'DE',
        'HU', 'IE', 'IT', 'LV', 'LI', 'LT', 'LU', 'MT', 'MD', 'MC',
        'NL', 'PL', 'PT', 'RO', 'SM', 'RS', 'SK', 'SI', 'ES', 'CH', 'VA',
    ]

# Mapping from country codes to country names
country_names = {
    'AL': 'Albania',
    'AD': 'Andorra',
    'AT': 'Austria',
    'BY': 'Belarus',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'HR': 'Croatia',
    'CZ': 'Czechia',
    'EE': 'Estonia',
    'FR': 'France',
    'DE': 'Germany',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LV': 'Latvia',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'MT': 'Malta',
    'MD': 'Moldova',
    'MC': 'Monaco',
    'NL': 'Netherlands',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SM': 'San Marino',
    'RS': 'Serbia',
    'SK': 'Slovakia',
    'SI': 'Slovenia',
    'ES': 'Spain',
    'CH': 'Switzerland',
    'VA': 'Vatican City',
}

def normalize_event_name(name):
    # Remove accents and convert to lowercase
    nfkd_form = unicodedata.normalize('NFKD', name)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('ASCII')
    return only_ascii.lower().strip()

def get_holidays_for_country(country_code, year):
    url = 'https://openholidaysapi.org/PublicHolidays'
    valid_from = f'{year}-01-01'
    valid_to = f'{year}-12-31'
    params = {
        'countryIsoCode': country_code,
        'validFrom': valid_from,
        'validTo': valid_to,
        'languageIsoCode': 'EN',
    }
    headers = {
        'accept': 'application/json',
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"No holidays found for {country_code} in {year}.")
            return []
    except Exception as e:
        print(f"Error fetching data for {country_code}: {e}")
        return []

def get_moon_phases(year):
    moon_events = []
    date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    while date <= end_date:
        next_full_moon = ephem.next_full_moon(date).datetime()
        if next_full_moon.year == year and next_full_moon <= end_date:
            event = {
                'name': 'Full Moon',
                'date': next_full_moon.strftime('%Y-%m-%d'),
                'description': 'Astronomical Event',
            }
            moon_events.append(event)
        date = next_full_moon + timedelta(days=1)
    return moon_events

def regenerate_calendar_for_year(year):
    country_list = get_country_list()
    all_events = []
    event_counter = 0
    event_set = {}  # Dictionary to track unique events

    for country_code in country_list:
        print(f"Fetching holidays for {country_code} in {year}...")
        holidays = get_holidays_for_country(country_code, year)
        for holiday in holidays:
            event_date = holiday.get('startDate', '')  # 'YYYY-MM-DD'
            event_name = holiday.get('name', '')
            # Process event_name to extract the string
            if isinstance(event_name, str):
                # event_name is a string, use it as is
                pass
            elif isinstance(event_name, dict):
                # event_name is a dict, extract the 'text' field
                event_name = event_name.get('text', '')
            elif isinstance(event_name, list):
                # event_name is a list, extract 'text' fields from dicts or use strings
                names = []
                for item in event_name:
                    if isinstance(item, str):
                        names.append(item)
                    elif isinstance(item, dict):
                        names.append(item.get('text', ''))
                    else:
                        names.append(str(item))
                event_name = ' '.join(names)
            else:
                # event_name is of unknown type, convert to string
                event_name = str(event_name)
            # Normalize event name for comparison
            norm_event_name = normalize_event_name(event_name)
            # Create a key for the event
            event_key = (event_date, norm_event_name)
            if event_key not in event_set:
                event_set[event_key] = {
                    'countries': [country_code],
                    'name': event_name,
                    'date': event_date,
                }
            else:
                # If the event is already in the set, add the country code to the list
                event_set[event_key]['countries'].append(country_code)

    # Process events to create iCal entries
    ical_events = []
    event_counter = 0
    for event_key, event_info in event_set.items():
        event_counter += 1
        uid = f'uid-{event_counter}@yourdomain.com'
        event_date = datetime.strptime(event_info['date'], '%Y-%m-%d')
        # Determine if the event is common (in multiple countries)
        if len(event_info['countries']) > 1:
            # Common event
            summary = f"{event_info['name']} [Common]"
        else:
            # Country-specific event
            country_code = event_info['countries'][0]
            # Get the full country name
            country_name = country_names.get(country_code, country_code)
            summary = f"{event_info['name']} [{country_name}]"
        # Create iCal event
        event_text = f"""BEGIN:VEVENT
UID:{uid}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}
SUMMARY:{summary}
END:VEVENT"""
        ical_events.append(event_text)

    # Include moon phases (optional)
    moon_phases = get_moon_phases(year)
    for moon_event in moon_phases:
        event_counter += 1
        uid = f'uid-moon-{event_counter}@yourdomain.com'
        event_date = datetime.strptime(moon_event['date'], '%Y-%m-%d')
        summary = f"{moon_event['name']} [Astronomical]"
        event_text = f"""BEGIN:VEVENT
UID:{uid}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}
SUMMARY:{summary}
DESCRIPTION:{moon_event['description']}
END:VEVENT"""
        ical_events.append(event_text)

    # Create our own calendar header and footer
    calendar_header = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Product Name//Your Version//EN\nCALSCALE:GREGORIAN'
    calendar_footer = 'END:VCALENDAR'

    # Now we have all_events
    combined_ical = calendar_header + '\n'
    combined_ical += '\n'.join(ical_events) + '\n'
    combined_ical += calendar_footer

    # Save the combined ical data to a file
    filename = f'holidays_combined_{year}.ics'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(combined_ical)
    print(f"Combined iCal file saved: {filename}")

if __name__ == "__main__":
    year = 2025  # Change this to any year you want to regenerate
    regenerate_calendar_for_year(year)
