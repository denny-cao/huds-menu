import requests
import json
import datetime
from bs4 import BeautifulSoup

HUDS_ENDPOINT = "https://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?"

class Meal:
    def __init__(self, name: str, id: int, interval: tuple):
        self.name = name
        self.id = id # ID of the meal. Used to make requests to HUDS.
        self.interval = interval

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> int:
        return self.id

    def get_items(self) -> list:
        return self.items 

    def get_interval(self) -> tuple:
        return self.interval

    def is_in_interval(self, time: datetime.time) -> bool:
        "Returns true if the time is in the interval of the meal. Used to determine if the meal is currently being served."
        return time >= self.interval[0] and time <= self.interval[1]

    def is_before_interval(self, time: datetime.time) -> bool:
        "Returns true if the time is before the interval of the meal. Used to determine if the meal is the next meal."
        return time < self.interval[0]

    def get_menu(self, type: int, next_day=False) -> dict:
        "Returns the menu for the given meal."
        date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m-%d-%Y") if next_day else datetime.datetime.now().strftime("%m-%d-%Y")
        endpoint = HUDS_ENDPOINT + f"date={date}&type={type}&meal={self.get_id()}"
        # Get HTML of page with requests
        page = requests.get(endpoint).text
        soup = BeautifulSoup(page, 'html.parser')
    
        meal = {}
    
        # Find all categories and dishes
        categories = soup.find_all(class_='category')
        for category in categories:
            category_name = category.td.text.strip()
            dishes = []
            next_element = category.find_next_sibling()
            
            # Extract dishes for each category
            while next_element and 'category' not in next_element.get('class', []):
                dish_name = next_element.find('a').text.strip()
                dishes.append(dish_name)
                next_element = next_element.find_next_sibling()
            
            # Add category and dishes to meal dictionary
            meal[category_name] = dishes
    
        return meal

MEALS = [
    Meal("Breakfast", 0, (datetime.time(7, 30), datetime.time(10, 30))),
    Meal("Lunch", 1, (datetime.time(11, 30), datetime.time(14, 0))),
    Meal("Dinner", 2, (datetime.time(16, 30), datetime.time(19, 30)))
]

def get_current_next_meal() -> (Meal, bool):
    "Returns the current meal if it is being served, else returns the next meal."
    now = datetime.datetime.now().time()
    # Check if current meal is being served
    for meal in MEALS:
        if meal.is_in_interval(now):
            return meal, False
    # If not, return next meal 
    for meal in MEALS:
        if meal.is_before_interval(now):
            return meal, False
    # Return breakfast for the next day 
    return MEALS[0], True

if __name__ == "__main__":
    meal, next_day = get_current_next_meal()
    if meal:
        items = meal.get_menu(30, next_day)
        try:
            entrees = items['Entrees']
            veg_entrees = items['Veg,Vegan']
            starch = items['Starch And Potatoes']
            vegetables = items['Vegetables']
            plant_protein = items['Plant protein']
            halal = items['Halal']
            desserts = items['Desserts']
            grill = items['From the Grill']
        except KeyError:
            print("No menu currently available.")
            exit()
    else:
        print("No meal currently being served.")
