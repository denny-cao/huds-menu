# https://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date=12-15-2023&type=30

import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import os
import sys
import time
import random
import main

# Get the date in mm-dd-yyyy format for the URL 
date = datetime.datetime.now().strftime("%m-%d-%Y")



