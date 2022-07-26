import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
import math

"""
==============================================================================
This Script stores all the search items along with price into a CSV File.
==============================================================================
PRE-REQUISITE :
PYTHON VERSION : 3.x
Chrome Driver
------------------------------------------------------------------------------
Input : 
UserName : Enter Flipkart UserName
Password : Enter Flipkart password
Search_Product : Enter a Product to search
Output: 
A CSV Files contains all the products along with price to that search
Variables :
chromedriverurl --> Enter the path of the chromedriver.
"""


class Flipkart_Search:
    
    #Initializing all the variables
    def __init__(self):
        self.products=[]
        self.prices=[]


    #Login to Flipkart portal
    def Flipkart_Login(self):
        
        Username=input("Enter User Name - ")
        Password=getpass.getpass("Enter Password - ")
        print("Please wait............ logging into Flipkart account")
        options.add_argument("start-maximized")
        options.add_argument('disable-infobars')
        driver.get('https://www.flipkart.com/account/login?ret/')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Enter Email/Mobile number')]//preceding::input[1]"))).send_keys(Username)
        driver.find_element_by_xpath("//span[contains(.,'Enter Password')]//preceding::input[1]").send_keys(Password)
        driver.find_element_by_xpath("//button[@type='submit']//span[contains(.,'Login')]").click()
        time.sleep(5)

        login_url='https://www.flipkart.com/account/login?ret/'
        present_url = driver.current_url;
        if(login_url==present_url):
            return ("Login Failed")
        else:
            return ("Login Successful")
    
	
    #Open Web Pages
    def Extract_Page(self,Search_Product):
        if " " in Search_Product:
            Search_Product=Search_Product.replace(" ","+")
        Search_Product="https://www.flipkart.com/search?q="+Search_Product+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        url=Search_Product+"&page="+str(page)
        print(url)
        return driver.get(url)
    
    #Extract the class names of the product name and price
    def Extract_Product_Info(self,init_search):
        
        flag_prod=0
        flag_pri=0
        
        Product_Class=["_3wU53n","_2B_pmu","_2mylT6","_2cLu-l"]
        Price_Class=['_1vC4OE','_1vC4OE _1DTbR5']
        
        #Extract price class name
        for pri_var in Price_Class:
            product_price=driver.find_elements_by_class_name(pri_var)
            if(len(product_price)>0):
                flag_pri=1
                break
                
        #Extract product class name       
        for pro_var in Product_Class:
            product_name=driver.find_elements_by_class_name(pro_var)
            if(len(product_name)>0):
                flag_prod=1
                break
        #If not present in product name list give input
        if flag_prod==0:
            Class_Name = input("Enter Class Name of the Search Product - ")
            product_name=driver.find_elements_by_class_name(Class_Name)
            if(len(product_name)>0):
                Product_Class.append(Class_Name)
                
        #If not present in price name list give input
        if flag_pri==0:
            Class_Name = input("Enter Class Name of the Search Price - ")
            product_price=driver.find_elements_by_class_name(Class_Name)
            if(len(product_price)>0):
                product_price.append(Class_Name)
                
        Flipkart_Search.Getting_Product_Info(self,product_name,product_price)
    
	
    #Extract the product details from the HTML Tags
    def Getting_Product_Info(self,product_name,product_price):
        
        for x in range(0,len(product_name)):
            if len(product_name[x].text) > 0:
                self.products.append(product_name[x].text)
            if len(product_price[x].text) > 0:
                self.prices.append(product_price[x].text)
        Flipkart_Search.Store_Result(self)
         
    
    #Store the search result into Product_List.CSV File
    def Store_Result(self):
        
        CSV_File = pd.DataFrame({'Product Name':self.products,"Product's Price":self.prices}) 
        CSV_File.to_csv('Product_List.csv', index=False, encoding='utf-8',mode="w")
        
    
    #Extracting the number of pages from the given search 
    def Page_Count(self,init_search):
        try:
            pages_text=driver.find_elements_by_class_name('_2yAnYN')
            items=pages_text[0].text
            total_items=(items.split(" ")[5]).replace(",","")
            pages=math.ceil(int(total_items)/int(items.split(" ")[3]))
            no_of_pages=(pages)
            return (no_of_pages)
        except:
            print("Change the valid class name of the page count")
        
        
if __name__ == "__main__":
    
    page=1
    chromedriverurl=r'C:\Users\oruganti.tejaswini\Desktop\chromedriver_win32\chromedriver.exe'

    options = webdriver.ChromeOptions() 
    driver=webdriver.Chrome(chrome_options=options, executable_path=chromedriverurl)

    Flipkart_Search_Obj=Flipkart_Search()
    result=Flipkart_Search_Obj.Flipkart_Login()

    if result=="Login Successful":
        Search_Product=input("Enter Product To Search - ")
        #Search_Product="lenovo laptops"
        init_search=Flipkart_Search_Obj.Extract_Page(Search_Product)
        no_of_pages=Flipkart_Search_Obj.Page_Count(init_search)
        print("page count - "+str(no_of_pages))
    

        while page<2+1:
            init_search=Flipkart_Search_Obj.Extract_Page(Search_Product)
            Flipkart_Search_Obj.Extract_Product_Info(init_search)
            page+=1
    else:
        print("Enter Valid Credentials")

    print("end")
