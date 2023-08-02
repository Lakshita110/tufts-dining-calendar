from google_calendar import GoogleCalendar
from tufts_dining import TuftsDining
from datetime import datetime, timedelta

import re 

def main():
    date = datetime.today()
    date_text = date.strftime("%Y-%m-%d")
    dining = TuftsDining()
    calendar = GoogleCalendar()
    locations = [0,1]

    for i in range(0,7):
        for index in locations:
            text = dining.get_data(index, date_text) 
            if text: 
                location = dining.LOCATIONS[index]
                summary = f"{location[0].split()[0]} Menu"
                event = calendar.create_event(summary=summary, description=text, date=date_text)
                calendar.insert_event(event)
            else:
                print(f"Not creating event because is not serving food :(")

        #Update for next day        
        date = date + timedelta(days=1)
        date_text = date.strftime("%Y-%m-%d")

if __name__ == '__main__':
    main()