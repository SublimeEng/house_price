import pymysql
from scrapping import house_cls

class house_db:
    def __init__(self):
        self.mydb = pymysql.connect(host="localhost",
                                    user="root",
                                    password="",
                                    database="house_price")

    def insert_house_data(self,house_data):
        cursor = self.mydb.cursor()
        sql="INSERT INTO scrape_data(area_type,location,size,society,sqrft,bathroom,facing,price_fin) Values('"
        sql += house_data.get_area_type()+"','"
        sql += house_data.get_location()+"','"
        sql += house_data.get_size()+"','"
        sql += house_data.get_society()+"','"
        sql += house_data.get_sqrft()+"','"
        sql += house_data.get_bathroom()+"','"
        sql += house_data.get_facing()+"','"
        sql += house_data.get_price_fin()+"'"
        sql+=");"
        print(sql)
        cursor.execute(sql)
        self.mydb.commit()
        #self.mydb.close()

    def insert_houses(self,house_list):
        for house_data in house_list:
            self.insert_house_data(house_data)
        

    def read_houses(self):
        cursor = self.mydb.cursor()
        sql='''SELECT * from scrape_data'''
        
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        current_houses = []
        for row in result:
            current_house = house_cls()
            current_house.set_area_type(row[2])
            current_house.set_location(row[3])
            current_house.set_size(row[4])
            current_house.set_society(row[5])
            current_house.set_sqrft(row[6])
            current_house.set_bathroom(row[7])
            current_house.set_facing(row[8])
            current_house.set_price_fin(row[9])
            
            current_houses.append(current_house)
        self.mydb.commit()
        return current_houses
    



    #to insert clean final data
    def insert_final_data(self,chouse_data):
        cursor = self.mydb.cursor()
        sql="INSERT INTO final_data(location,total_sqrft,bathroom,bhk,price) Values('"
        sql += chouse_data.get_location()+"',"
        sql += str(chouse_data.get_total_sqrft())+",'"
        sql += str(chouse_data.get_bathroom())+"','"
        sql += str(chouse_data.get_bhk())+"','"
        sql += str(chouse_data.get_price())+"'"
        sql+=");"
        print(sql)
        cursor.execute(sql)
        self.mydb.commit()
        #self.mydb.close()

    def insert_final_houses(self,house_list):
        for L_house_data in house_list:
            self.insert_final_data(L_house_data)
        

    def read_final_houses(self):
        cursor = self.mydb.cursor()
        sql='''SELECT * from final_data'''
        
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        current_houses = []
        for row in result:
            current_house = house_cls()
            current_house.set_location(row[0])
            current_house.set_total_sqrft(row[1])
            current_house.set_bathroom(row[2])
            current_house.set_bhk(row[3])
            current_house.set_price(row[4])
            
            current_houses.append(current_house)
        self.mydb.commit()
        return current_houses
    

    #to insert data flag
    def update_data_flag(self,status):
        cursor = self.mydb.cursor()
        sql="UPDATE data_flag SET is_data_updated = '"+status+"' WHERE id = 1"
        print(sql)
        cursor.execute(sql)
        self.mydb.commit()
        #self.mydb.close()

    
    def read_data_flag(self):
        cursor = self.mydb.cursor()
        sql='''SELECT * from data_flag'''
        
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        self.mydb.commit()
        return result
