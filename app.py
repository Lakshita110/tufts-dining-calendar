from google_calendar import GoogleCalendar
from tufts_dining import TuftsDining
from datetime import datetime

import re 

def main():
    date = datetime.today().strftime("%Y-%m-%d")
    dining = TuftsDining()
    calendar = GoogleCalendar()
    locationIndex = 1

    text = dining.get_data(locationIndex, date) 
    if text: 
        description = dining.LOCATIONS[locationIndex][0].upper()
        description +=  "\n" + "\n" + text
        event = calendar.create_event(summary="Today's Meal", description=description, date=date)
        calendar.insert_event(event)
    else:
        print(f"Not creating event because is not serving food :(")

if __name__ == '__main__':
    main()