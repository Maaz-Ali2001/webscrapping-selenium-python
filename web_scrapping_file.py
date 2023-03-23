import os.path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
import mysql.connector


class web_scrapping:
    def __init__(self):
        PATH = r"google_chrome\chromedriver.exe"
        self.website = str(input("Enter website url :"))
        # example website: "https://www.doordash.com/store/mcdonald's-ogdensburg-1657725/?cursor=eyJzdG9yZV92ZXJ0aWNhbF9pZCI6bnVsbCwic2VhcmNoX2l0ZW1fY2Fyb3VzZWxfY3Vyc29yIjp7InF1ZXJ5IjoiIiwiaXRlbV9pZHMiOltdLCJzZWFyY2hfdGVybSI6IiIsInZlcnRpY2FsX2lkIjpudWxsLCJ2ZXJ0aWNhbF9uYW1lIjoiIn0sImlzX3NpYmxpbmciOmZhbHNlLCJmb3JjZV9zdG9yZV9hdmFpbGFiaWxpdHlfdjIiOmZhbHNlfQ==&pickup=false"
        self.product_names = {}
        self.driver = webdriver.Chrome(PATH)
        self.driver.get(self.website)
    def check_index(self,xpath, index):
        try:
            lst = xpath.split(")")
            index = "[" + str(index) + "]"
            xpath = (")" + index).join(lst)
            elem = self.driver.find_element(By.XPATH, xpath)
            return elem
        except:
            return False

    def wait(self,xpath):
        try:
            y = 200
            for timer in range(0, 70):
                self.driver.execute_script("window.scrollTo(0, " + str(y) + ")")
                y += 300
                time.sleep(0.5)

            time.sleep(3)
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            print('wait')
            time.sleep(2)
            return False



    def scrapper(self):

        try:
            self.driver.find_element(By.ID, "cassie_reject_all_pre_banner").click()
        except:
            print("End 1")

        try:
            self.driver.find_element(By.XPATH, "//span[text()='Continue to store']").click()
        except:
            time.sleep(5)
            print("End 2")



        name = True
        index = 1
        flag = False



        while flag != True:
            flag = self.wait("(//h3[@data-telemetry-id='storeMenuItem.title'])[1]")

        resturant= self.driver.find_element(By.XPATH,"//*[@class='styles__TextElement-sc-3qedjx-0 jofHBq sc-25a927ea-0 gIMjqE']").text
        menu_category= self.driver.find_element(By.XPATH,"//*[@class='styles__TextElement-sc-3qedjx-0 iTbFCG']").text

        self.product_names['website'] = self.website
        self.product_names['resturant_name'] = resturant
        self.product_names['menu_category'] = menu_category
        products={}

        while name != False:
            name = self.check_index("(//h3[@data-telemetry-id='storeMenuItem.title'])", index)

            if name != False:
                name = name.text
                price = self.check_index(
                    "(//h3[@data-telemetry-id='storeMenuItem.title'])/parent::div/parent::div/following-sibling::div/descendant::span[@data-anchor-id='StoreMenuItemPrice']",
                    index)
                description = self.check_index(
                    "(//h3[@data-telemetry-id='storeMenuItem.title'])/parent::div/parent::div/following-sibling::div/child::span[@data-telemetry-id='storeMenuItem.subtitle']"
                    , index)
                img_src= self.check_index(
                    "(//h3[@data-telemetry-id='storeMenuItem.title'])/parent::div/parent::div/parent::div/following-sibling::div/descendant::img"
                    ,index)

                if price != False:
                    price = price.text
                else:
                    price = None

                if description != False:
                    description = description.text
                else:
                    description = None

                if img_src != False:
                    img_src = img_src.get_attribute("src")
                else:
                    img_src = None

                products[name]= {'price': price, 'description': description,'img_src':img_src}
            index += 1

        self.product_names['products'] = products


    def mysql(self):

        conn = mysql.connector.connect(
            user='root', password='maazali786', host='127.0.0.1', database='scrapping_database')
        cursor = conn.cursor()
        try:
            create_query = "CREATE TABLE IF NOT EXISTS website_products (website_url VARCHAR(1000) ,resturant_name VARCHAR(1000),menu_category VARCHAR(1000),product_name VARCHAR(1000),product_price VARCHAR(1000),product_description VARCHAR(1000),image_src VARCHAR(1000) );"
            cursor.execute(create_query)
        except:
            pass
        sql = "INSERT INTO website_products(website_url, resturant_name,menu_category,product_name ,product_price ,product_description ,image_src)VALUES (%s,%s,%s,%s,%s,%s,%s)"



        for item in self.product_names['products']:
            data= (self.product_names['website'],self.product_names['resturant_name'],self.product_names['menu_category'],item,self.product_names['products'][item]['price'],self.product_names['products'][item]['description'],self.product_names['products'][item]['img_src'])

            try:
                cursor.execute(sql,data)
                conn.commit()

            except:
                conn.rollback()

        conn.close()

obj = web_scrapping()
obj.scrapper()
obj.mysql()


