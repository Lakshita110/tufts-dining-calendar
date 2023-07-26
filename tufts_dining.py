import requests 
from bs4 import BeautifulSoup 
from datetime import datetime

class TuftsDining():

    def __init__(self):
        self.url = "" 
        self.date = datetime.today().strftime("%y-%m-%d") #Defaults to today
        self.location = None
        self.data = None

    def set_location(self):
        # List of lists where first is the name of location and second is id
        LOCATIONS = [["Carmichael Dining Center" , "09"], 
            ["Dewick Dining Center" , "11"],
            ["The Commons Marketplace" , "55"],
            ["Hodgdon Food On-the-Run" , "14"],
            ["Pax et Lox Glatt Kosher Deli" , "27"],
            ["Kindlevan Cafe" , "03"]]
        
        for i in range(len(LOCATIONS)):
            print(f"({i+1}): {LOCATIONS[i][0]}")
        
        print("Please select a location by indicating an index 1 through 7: ")
        index = int(input()) - 1
        
        if index >= 0 and index < 7:
            self.location = LOCATIONS[index]
            print(f"Location successfuly set to {LOCATIONS[index][0]}!")
            return self.location
        else: 
            print("Invalid location!")

    def __set_url(self):
        if self.location != None:
            date = self.date.split('-')
            url = f"http://menus.tufts.edu/FoodPro%203.1.NET/shortmenu.aspx?sName=TUFTS+DINING&"
            url += f"locationNum={self.location[1]}&locationName={self.location[0]}&naFlag=1"
            url += f"&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate={date[1]}%2f{date[2]}%2f{date[0]}"
            self.url = url
            print("Successfully set URL!")

        else: 
            print("No location set!")
        
    def __scrape(self):
        if self.url != "":
            doc = requests.get(self.url)
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
            if response == {}:
                print("No food there today!")
            else:
                self.data=response
        else:
            print("No URL set!")
            return None

    def __format_data(self):
        text = ""
        if self.data != None:
            for meal in self.data:
                text += meal.upper() + "\n"
                for item in self.data[meal]:
                    text += item[0] + "\n"
        else:
            print("No data obtained yet!")
            return text
        
    def get_data(self, date):
        self.date = date
        self.__set_url()
        self.__scrape()
        data = self.__format_data()
        if data:
            return data
        else: 
            return False