from google_calendar import GoogleCalendar
from tufts_dining import TuftsDining

import re 

def pick_date():
    print("Pick a date in the format YYYY-MM-DD: ")
    date = input()
    date_pattern = re.compile(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$")

    while not re.fullmatch(date_pattern, date):
        print("Pick a date in the format YYYY-MM-DD: ")
        date = input()

    return date


def main():
    date = pick_date()
    dining = TuftsDining()
    calendar = GoogleCalendar()
    calendar.set_calendar_id()
    location = dining.set_location()
    text = dining.get_data(date)
    if text: 
        event = calendar.create_event(summary="Today's Meal", description=text, date=date)
        calendar.insert_event(event)
    else:
        print(f"Not creating event because {location[0]} is not serving food :(")

if __name__ == '__main__':
    main()