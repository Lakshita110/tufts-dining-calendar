import requests 
from bs4 import BeautifulSoup 
from datetime import datetime

class TuftsDining():

    def __init__(self):
        self.LOCATIONS = [["Carmichael Dining Center" , "09"], 
            ["Dewick Dining Center" , "11"],
            ["The Commons Marketplace" , "55"],
            ["Hodgdon Food On-the-Run" , "14"],
            ["Pax et Lox Glatt Kosher Deli" , "27"],
            ["Kindlevan Cafe" , "03"]]     

    def create_url(self, location, date):
        try:
            date = date.split('-')
            url = f"http://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&"
            url += f"locationNum={location[1]}&locationName={location[0].replace(' ', '+')}&naFlag=1"
            url += f"&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate={date[1]}%2f{date[2]}%2f{date[0]}"
            url = url
            return url
        except: 
            print("Could not create URL!")
        
    def __scrape(self, url):
        doc = requests.get(url)
        soup = BeautifulSoup(doc.text, features="html.parser")
        response = dict()

        for div in soup.findAll("div"):
            try:
                curr_div_class = div["class"][0]

                if curr_div_class == "shortmenumeals":
                    menu_type = div.text.strip()
                    if menu_type not in response:
                        response[menu_type] = []

                # elif curr_div_class == "shortmenucats":
                #     category = re.sub(r'[^\w\s]', '', div.text).strip()
                #     category_dict = {category : []}
                #     response[menu_type].append(category_dict)

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
                    response[menu_type].append(food_item)
            except:
                continue

        print(response)
        return response

    def __format_data(self, data):
        text = ""
        for meal in data:
            text += meal.upper() + "\n"
            for item in data[meal]:
                if item[1] == True or item[2] == True:
                    text += item[0] + "\n"
        return text
        
    def get_data(self, locationIndex, date):
        url = self.create_url(self.LOCATIONS[locationIndex], date)
        return self.__format_data(self.__scrape(url))