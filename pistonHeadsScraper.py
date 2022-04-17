# Importing required libraries
import requests
import bs4
import pandas as pd
from random import randint
from time import sleep 
import re



url = 'https://www.pistonheads.com/classifieds?Category=used-cars&Page='

# Properties needed initalised as arrays
car = []
make = []
makes = []
model = []
year = []
milage = []
fuel = []
power = []
transmission = []
price = []


# range set to loop through function 40 times, for results from 40 pages. 
for page in range(1,500):
    x = randint(3,5)
    sleep(x)

    # Fetch the URL data using requests.get(url),
    # store it in a variable, request_result.
    request_result = requests.get(url + str(page) + '&SortOptions=NewestWithImages')
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")

    # find listings seperately, parses data into properties reqiured for our dataset
    def findHeader():
        for item in soup.find_all('div', attrs={'class': 'ad-listing'}):

            name = item.find('h3').getText().strip()
            specs = (item.find('ul', class_='specs').find_all('li'))
            price1 = item.find('div', attrs={'class': 'price'}).getText().strip().replace(',','')
            price2 = (re.findall('[0-9]+',(price1[1:])))
            price2 = ''.join(price2)
            
            # Only takes data that is complete 
            if (len(specs)) == 4 and (price2 != ''):
                milage.append(int((specs[0].getText().strip()[:-5]).replace(',','')))
                fuel.append(specs[1].getText().strip())
                power.append(int(specs[2].getText().strip()[:-3]))
                #power.append(pow[:-3])
                transmission.append(specs[3].getText().strip())
                car.append(name[:-6])
                make.append(str(car[-1].split()[0]).strip())
                model.append(str(car[-1].split()[1]).strip())
                
                print(price2)
                price.append(int(price2))
                year.append(int(name[-5:-1]))

    findHeader()

    makes = soup.find('div', class_='makemodels-chooser')

    #print(makes)

    def findMakes():
        for make in makes.find_all('option', attrs={'data-gtm-event-category':'srp'}):
            makes.append(make.text)


    
    #findMakes()
    #print('z')

    

# building a Data Frame with Pandas to store the data 
cars = pd.DataFrame({
'make' : make,
'model': model,
'year': year,
'mileage': milage,
'fuel': fuel,
'power': power,
'transmission': transmission,
'price': price,
})

print(len(car), len(make), len(year), len(milage), len(fuel), len(power), len(transmission), len(price))

# Exporting the data to a CSV file
cars.to_csv('cars.csv')

