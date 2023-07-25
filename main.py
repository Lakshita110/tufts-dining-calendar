import requests 
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta 
import re 
import pandas as pd 

doc = requests.get('https://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&locationNum=11&locationName=Dewick-MacPhie+Dining+Center&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=7%2f27%2f2023')
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
            category_dict[category].append(food_item)

            image = div.parent.parent.find("img")
            print(image)
            if image.contains("Vegan"):
                print("True")
                food_item[1] = True
            elif image.contains("Vegetarian"):
                food_item[2] = True
            elif image.contains("Halal"):
                food_item[3] = True
            print("Why is this not printing?!?!")
    except:
        continue

# print(response)