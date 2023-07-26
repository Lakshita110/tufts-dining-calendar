import requests 
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta 
import re 
import pandas as pd 
############

LOCATIONS = {"Carmichael Dining Center" : "09", 
            "Dewick Dining Center" : "11",
            "The Commons Marketplace" : "55",
            "Hodgdon Food On-the-Run" : "14",
            "Pax et Lox Glatt Kosher Deli" : "27",
            "Kindlevan Cafe" : "03"}

def getUrl():
    year = datetime.today().strftime("%y")
    month = datetime.today().strftime("%m")
    day = datetime.today().strftime("%d")
    url = f"http://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&"
    url += f"locationNum=11&locationName=Dewing Dining Center&naFlag=1"
    url += f"&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate={month}%2f{day}%2f{year}"
    return url

print(getUrl())

doc = requests.get(getUrl())
soup = BeautifulSoup(doc.text, features="html.parser")


response = dict()

for div in soup.findAll("div"):
    try:
        curr_div_class = div["class"][0]

        if curr_div_class == "shortmenumeals":
            menu_type = div.text.strip()
            if menu_type not in response:
                response[menu_type] = []

        elif curr_div_class == "shortmenucats":
            category = re.sub(r'[^\w\s]', '', div.text).strip()
            category_dict = {category : []}
            response[menu_type].append(category_dict)

        elif curr_div_class == "shortmenurecipes":
            food_item = [div.text.strip(), False, False, False] #Vegan, Vegetarian, Halal 
            
            image = div.parent.parent.find("img")
            if image != None:
                image = str(image)
                if "Vegan" in image:
                    food_item[1] = True
                elif "Vegetarian" in image:
                    food_item[2] = True
                elif "Halal" in image:
                    food_item[3] = True
            category_dict[category].append(food_item)

    except:
        continue

print(response)