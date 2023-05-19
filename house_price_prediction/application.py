#! C:/Python30/python

print("Content-type:text/html\n")
print("hello world")

from scrapping import house_scrape
from house import house_cls
from house_db import house_db
import csv
from flask import Flask, render_template, request
import pandas as pd
import pickle

house_scr = house_scrape()
houseDb = house_db()

result = houseDb.read_data_flag()
if result[0][1]== "No":
    url_lalbaug = "https://www.nobroker.in/property/sale/mumbai/Lal%20Baug/?searchParam=W3sibGF0IjoxOC45OTA4MTc3LCJsb24iOjcyLjgzODI1NDcwMDAwMDAxLCJwbGFjZUlkIjoiQ2hJSjVfX0dKZmpPNXpzUkJ2WEpYOF9NQTJnIiwicGxhY2VOYW1lIjoiTGFsIEJhdWciLCJzaG93TWFwIjpmYWxzZX1d&propType=AP&type=BHK1,BHK2,BHK3,BHK4&locality=Lal%20Baug"
    url_dadar = "https://www.nobroker.in/property/sale/mumbai/Dadar/?searchParam=W3sibGF0IjoxOS4wMTc3OTg5LCJsb24iOjcyLjg0NzgxMTk5OTk5OTk5LCJwbGFjZUlkIjoiQ2hJSkQ4MmdEdHZPNXpzUjBGdVpPVkJHaWtJIiwicGxhY2VOYW1lIjoiRGFkYXIiLCJzaG93TWFwIjpmYWxzZX1d&propType=AP&type=BHK1,BHK2,BHK3,BHK4&locality=Dadar"
    #url_worli = "https://www.nobroker.in/property/sale/mumbai/Worli/?searchParam=W3sibGF0IjoxOC45OTg2NDA2LCJsb24iOjcyLjgxNzM1OTksInBsYWNlSWQiOiJDaElKeFl3ME5KZk81enNSN0FCazRLcXJkeDgiLCJwbGFjZU5hbWUiOiJXb3JsaSIsInNob3dNYXAiOmZhbHNlfV0=&propType=AP&type=BHK1,BHK2,BHK3,BHK4&locality=Worli"
    url_mahim = "https://www.nobroker.in/property/sale/mumbai/Mahim/?searchParam=W3sibGF0IjoxOS4wMzUzODQ5LCJsb24iOjcyLjg0MjMwMzYsInBsYWNlSWQiOiJDaElKWFN2WVdpN0o1enNSRGI2RUsyNEoxS1UiLCJwbGFjZU5hbWUiOiJNYWhpbSIsInNob3dNYXAiOmZhbHNlfV0=&propType=AP&type=BHK1,BHK2,BHK3,BHK4&locality=Mahim"
    #call function from scrapping
    all_houses = []
    houses = house_scr.scrape_houses(url_lalbaug)
    for house in houses:
        all_houses.append(house)

    houses = house_scr.scrape_houses(url_dadar)
    for house in houses:
        all_houses.append(house)

    '''houses = house_scr.scrape_houses(url_worli)
    for house in houses:
        all_houses.append(house)'''

    houses = house_scr.scrape_houses(url_mahim)
    for house in houses:
        all_houses.append(house)
    houseDb.insert_houses(all_houses)

    house_cls = house_cls()
    current_houseData = house_scr.get_pd_table()
    print('printing value')
    for column in current_houseData.columns:
                print(current_houseData[column].value_counts())
    current_houseData.isna().sum

    house_scr.get_median()
    house_scr.get_values()
    new_house_data = house_scr.get_new_price_mean_col()
    newhouses = house_scr.clean_data(new_house_data)
    houseDb.insert_final_houses(newhouses)
    house_scr.get_pd_fin_table()
    house_scr.linear_reg()
    house_scr.lasso_reg()
    house_scr.ridge_reg()
    house_scr.final_model()

houseDb.update_data_flag("Yes")
#making csv
current_houses = houseDb.read_houses()
current_fin_houses = houseDb.read_final_houses()

csv_headers=['Area type','Location','Size','Society','Total Sqrft','Bathroom','Flat facing','Price']
with open("House.csv",'w',encoding='utf-8',newline='')as f:
    writer=csv.writer(f)
    writer.writerow(csv_headers)
    for house in current_houses:
        writer.writerow([house.area_type,house.location,house.size,house.society,house.sqrft,house.bathroom,house.facing,house.price_fin])

#clean csv
csv_headers_fin=['Location','Total Sqrft','Bathroom','Bedroom','Price']
with open("Clean_data.csv",'w',encoding='utf-8',newline='')as f:
    writer=csv.writer(f)
    writer.writerow(csv_headers_fin)
    for house in current_fin_houses:
        writer.writerow([house.location,house.total_sqrft,house.bathroom,house.bhk,house.price])






app = Flask(__name__)
data = pd.read_csv('Clean_data.csv')
pipe = pickle.load(open("Ridgemodel.pkl", 'rb'))

@app.route('/')
def index():
    locations = sorted(data['Location'].unique())
    bhks = sorted(data['Bedroom'].unique())
    bath = sorted(data['Bathroom'].unique())
    sqrfts = sorted(data['Total Sqrft'].unique())
    print(sqrfts)
    return render_template('index.html', locations=locations, bhks=bhks, bath=bath)

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    bhk = request.form.get('bhk')
    bathroom = request.form.get('bathroom')
    sqrft = request.form.get('total_sqrft')

    print(location, bhk, bathroom, sqrft)

    input = pd.DataFrame([[location,bhk,bathroom,sqrft]], columns=['location', 'bhk', 'bathroom', 'total_sqrft'])
    prediction = pipe.predict(input)[0]
    return str(prediction)

if __name__ == "__main__":
    app.run(debug=True, port=80)







#value count for all columns
    #for column in data.columns:
        #print(data[column].value_counts())

# show null value in columns
    #data.isna().sum

#drop some columns to find means and median of bathroom and price
    #data.drop(columns=['area','facing','society','balcony',ect],inplace = True )

#find means and median of bathroom and pric
    #data.describe()

#took only 5 column to predict and show
    #data.info()
#show each valu count seperately
    #data['locaton'].value_counts ()
    #data['size'].value_counts ()

#value of sqrft
 #data['total_sqrft'].unique()

 
