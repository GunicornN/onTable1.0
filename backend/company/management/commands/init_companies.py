# ------------------------------------------
#  Custom Commands that creates Companies Cards, 
#  Products from Webscrapping data
# ------------------------------------------

from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver

from bs4 import BeautifulSoup

import time 

#Simple assignment
from selenium.webdriver import Safari

import json 

from company.models import Company, Card, Product


# ------------------------------------------
#   Web scrapping : Dynamics Sites
#
# ------------------------------------------
# DOCS 
# ------------------------------------------
# Selenium for Web Driver 
# https://www.selenium.dev/documentation/fr/webdriver/driver_requirements/
# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25
# https://kelvinmwinuka.medium.com/running-selenium-on-macos-using-chromedriver-96ef851282b5
#
# BeautifulSoup
# 

MAIN_URL = "https://www.tripadvisor.fr"

def get_categories():
    with Safari() as driver:
        #driver.get("https://www.tripadvisor.fr/Restaurant_Review-g187265-d16813160-Reviews-Le_Coq-Lyon_Rhone_Auvergne_Rhone_Alpes.html")
        driver.set_window_position(0, 0)
        driver.set_window_size(1600, 950)
        driver.get("https://www.tripadvisor.fr/Restaurants-g187265-Lyon_Rhone_Auvergne_Rhone_Alpes.html")

        time.sleep(3)

        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,'html.parser')
        soup.prettify()

        company_categories = []

        for category in soup.find_all('a',{'class':'HL1nJ5sk'}):
            company_categories.append({'name': category.getText() , 'url': category['href'],'companies': []})


        for category in company_categories:
            driver.get("{}{}".format(MAIN_URL,category['url']))
            time.sleep(3)

            # Get the list of restaurants for each category
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,'html.parser')
            soup.prettify()


            more_buttons = driver.find_elements_by_class_name("HL1nJ5sk")
            for x in range(len(more_buttons)):
                if more_buttons[x].is_displayed():
                    driver.execute_script("arguments[0].click();", more_buttons[x])
                    time.sleep(1) # Waiting the end of API calls 


            page_source = driver.page_source
            soup = BeautifulSoup(page_source,'html.parser')
            soup.prettify()
        
            # _15_ydu6b
            for company in soup.find_all('a',{'class':'_15_ydu6b'}):
                category['companies'].append({'name': company.getText(),'url':company['href']})

        with open("companies.json","w") as file :
            json.dump(company_categories,file)
        
        # List of restaurants by category obtained



def get_company_details():
    """Retrieve company address and phone number."""
    with open("companies.json",'r') as f: 
        data = json.loads(f.read())

        with Safari() as driver:
            driver.set_window_position(0, 0)
            driver.set_window_size(1600, 950)
            for indexCat,category in enumerate(data):
                for indexCo,company in enumerate(category['companies']):

                    print("{}{}".format(MAIN_URL,company['url']))
                    driver.get("{}{}".format(MAIN_URL,company['url']))

                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source,'html.parser')
                    soup.prettify()

                    company_details = soup.find('span',{'class':'_2saB_OSe'}).getText()
                    #print(company_details) #20 rue de l Abbaye D Ainay, 69002 Lyon France
                    try:
                        data[indexCat]['companies'][indexCo]['address1'] = company_details.split(',')[0]
                    except IndexError as e :
                        data[indexCat]['companies'][indexCo]['address1'] = ''

                    try:
                        data[indexCat]['companies'][indexCo]['zip_code'] = company_details.split(',')[1].split(' ')[1]
                    except IndexError as e :
                        data[indexCat]['companies'][indexCo]['zip_code'] = ''

                    try:
                        data[indexCat]['companies'][indexCo]['city'] = company_details.split(',')[1].split(' ')[2]
                    except IndexError as e :
                        data[indexCat]['companies'][indexCo]['city'] = ''

                    try:
                        data[indexCat]['companies'][indexCo]['country'] = company_details.split(',')[1].split(' ')[3]
                    except IndexError as e :
                        data[indexCat]['companies'][indexCo]['country'] = 'France'

                    # -----------------------------------
                    #           Menus 
                    # -----------------------------------
                    # Check if the restaurant has menus 
                    # Click on Menus 
                    more_buttons = driver.find_elements_by_class_name("trj1xMpn")

                    if more_buttons :
                        for x in range(len(more_buttons)):
                            if more_buttons[x].is_displayed():
                                driver.execute_script("arguments[0].click();", more_buttons[x])
                                time.sleep(1) # Waiting the end of API calls 
                        
                        # Get menu names
                        page_source = driver.page_source
                        soup = BeautifulSoup(page_source,'html.parser')
                        soup.prettify()

                        # Click on Menu name 
                        more_buttons = driver.find_elements_by_class_name("_3azp1RhW")

                        # Beautiful soup variables 
                        menus_name = []
                        company_cards = []
                        # Menu names are in div labels with class _3nq6E0dI

                        #print(soup.find('div',{'class':'_3nq6E0dI'}))


                        for menu_name in soup.find('div',{'class':'_3nq6E0dI'}) :
                            text = menu_name.getText() # we want text in <div>text </div>
                            if text != '' :
                                menus_name.append(menu_name.getText())
                                
                        # clean array : remove duplicates
                        menus_name = list(dict.fromkeys(menus_name))

                        # Adjust the dict 
                        for name in menus_name:
                            company_cards.append({'name':name})

                        for x in range(len(more_buttons)):
                            if more_buttons[x].is_displayed():
                                driver.execute_script("arguments[0].click();", more_buttons[x])
                                time.sleep(2) # Waiting the end of API calls 

                                # init array for dict 
                                company_cards[x]['products'] = []

                                page_source = driver.page_source

                                #print(page_source)

                                soup = BeautifulSoup(page_source,'html.parser')
                                soup.prettify()

                                raw_meals = soup.find_all('div',{'class':'_3Yhd5Duy'})
                                # Get each dish from a menu
                                for meal_menu in raw_meals :
                                    meals = []
                                    unparsed_meals = meal_menu.find_all('div',{'class':'_2N7zl-v2'})
                                    for unparsed_meal in unparsed_meals :
                                        meals.append(unparsed_meal.getText())
                        
                                    # clean array : remove duplicates
                                    meals = list(dict.fromkeys(meals))           


                                    for meal in meals :  
                                        company_cards[x]['products'].append(meal)

                                    # Get price
                                    prices = soup.find_all('span',{'class':'_2EcgU5Lr'})
                                    if prices :
                                        company_cards[x]['prices'] = []
                                        for price in prices :
                                            if price.getText():
                                                company_cards[x]['prices'].append(price.getText())

                        # Error correction
                        for x1 in range(1,len(company_cards)):
                            for product_test in company_cards[0]['products']: # should correspond 
                                for product_rm in company_cards[x1]['products']:
                                    if product_test == product_rm:
                                        company_cards[x1]['products'].remove(product_test)
                        print(company_cards)
                        data[indexCat]['companies'][indexCo]['cards'] = company_cards


        with open("companiesDetails.json",'w') as f2: 
            data = json.dumps(data, ensure_ascii=False)
            f2.write(data)
# ------------------------------------------
#       End scrapping 
# ------------------------------------------


# ------------------------------------------
#  Command that read json w/ scrapped Datas
# And create companies, cards and products
# ------------------------------------------
# DOCS 
# ------------------------------------------
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
# ------------------------------------------

class Command(BaseCommand):
    help = 'Create Companies, cards, products'

    def handle(self, *args, **kwargs):
        with open("companiesDetails.json",'r') as f: 
            data = json.loads(f.read())
            for indexCat,category in enumerate(data):
                for indexCo,company in enumerate(category['companies']):

                    # Company Fields
                    name = data[indexCat]['companies'][indexCo]['name']
                    address1 = data[indexCat]['companies'][indexCo]['address1']
                    zip_code = data[indexCat]['companies'][indexCo]['zip_code']
                    city = data[indexCat]['companies'][indexCo]['city']
                    country = data[indexCat]['companies'][indexCo]['country']

                    check_company = Company.objects.filter(name=name,address1=address1)

                    if check_company :
                        self.stdout.write(self.style.WARNING('Company was already created... Skipping'))
                    else :
                        # Create the company
                        try:
                            company = Company.objects.create(name=name,address1=address1,zip_code=zip_code,city=city,country=country)
                            self.stdout.write(self.style.SUCCESS('Company "%s (%s)" created with success!' % (company.name, company.id)))

                            company = Company.objects.get(name=name,address1=address1)
                            
                            # Cards 
                            if 'cards' in data[indexCat]['companies'][indexCo]:
                                for index,card in enumerate(data[indexCat]['companies'][indexCo]['cards']):
                                    card_name = card['name']
                                    Card.objects.create(name=card_name,company=company)

                                    # Product Fields 
                                    if len(card['prices']) == len(card['products']):
                                            for indexProd, prod in enumerate(data[indexCat]['companies'][indexCo]['cards'][index]['products']):
                                                name = data[indexCat]['companies'][indexCo]['cards'][index]['products'][indexProd]
                                                if 'price' in data[indexCat]['companies'][indexCo]['cards'][index]:
                                                    price = data[indexCat]['companies'][indexCo]['cards'][index]['price'][indexProd]
                                                    Product.objects.create(name=name,price=price,company=company)
                                                else :
                                                    Product.objects.create(name=name,company=company)
                                    else :
                                        self.stdout.write(self.style.WARNING('Error creating card'))
                            
                        except ValueError as error:
                            self.stdout.write(self.style.SUCCESS('Company {} was not created. Invalid Field'.format(name)))



