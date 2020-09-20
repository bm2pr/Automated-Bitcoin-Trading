from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import Config
import time
 
class Driver():
    def __init__(self):
 
        chrome_options = Options()
        self.driver = webdriver.Chrome(executable_path=Config.PATH, chrome_options=chrome_options)
 
    def login_method(self):
        
        self.driver.get('https://robinhood.com/crypto/btc')
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/header/div/div[2]/div/a[5]/span').click()
        
        user_name = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")
        
        user_name.send_keys(Config.USERNAME)
        password.send_keys(Config.PASSWORD)
    
        #self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/form/footer/div/button').click()
    
        time.sleep(40)
    
 
    def buy(self):
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/header/div/div[1]/div/div[1]/div/h3').click()
        except:
            print('Failed to click buy tab')
 
        amount = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/form/div[1]/footer').text
    
        amount = amount.replace(" Buying Power Available",  "")
        amount = amount.replace("$", "")
        amount = amount.replace(",", "")
    
        amount = 0.99 * float(amount)
        amount = str(amount)
        buyBox = self.driver.find_element_by_name("amount")
        buyBox.send_keys(amount)
        # Hit review order button
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/form/div[1]/div[2]/div/div[2]/div/button').click()
        time.sleep(1)
        # Hit submit order button
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/form/div[1]/div[2]/div/div[2]/div[1]/button').click()
        time.sleep(1)
        # Hit done button
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/footer/div/button').click()
 
    def sell(self):
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/header/div/div[1]/div/div[2]/div/h3/span/div/span').click()
        except:
            print('Failed to click sell tab')
        amount = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/footer').text
        amount = amount.replace("Available",  "")
        amount = amount.replace("$", "")
        amount = amount.replace(",", "")
        amount = 0.99 * float(amount)
        amount = str(amount)
        buyBox = self.driver.find_element_by_name("amount")
        buyBox.send_keys(amount)
        # Review order button
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/div/div[2]/div/button').click()
        time.sleep(1)
        # Yes button
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/div/div[2]/div[1]/button').click()
        # Submit sell button
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/div/div[2]/div[1]/button').click()
        # Hit done button
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/footer/div/button').click()
 
    def bought(self):
        # Get amound in USD from buy tab
        self.driver.get('https://robinhood.com/crypto/btc')
        # find amount in usd
        time.sleep(5)
        amount_usd = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/form/div[1]/footer').text
        amount_usd = amount_usd.replace(" Buying Power Available",  "")
        amount_usd = amount_usd.replace("$", "")
        amount_usd = amount_usd.replace(",", "")
        amount_usd = float(amount_usd)
 
        # Get amount in BTC from sell tab
        amount_btc = 0
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/header/div/div[1]/div/div[2]/div/h3/span/div/span').click()
            amount_btc = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/footer').text
            amount_btc = amount_btc.replace("Available",  "")
            amount_btc = amount_btc.replace("$", "")
            amount_btc = amount_btc.replace(",", "")
            amount_btc = float(amount_btc)
        except:
            print('Failed to click sell tab')
        
        
 
        return amount_btc > amount_usd
    def get_curr_buy_price(self):
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/header/div/div[1]/div/div[1]/div/h3').click()
        except:
            print('Failed to click buy tab')
 
        price_string = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/form/div[1]/div[1]/div[1]/div[2]/div[2]/span').text
        price_string = price_string.replace('$', '')
        price_string = price_string.replace(',', '')

        return float(price_string)

    def get_curr_sell_price(self):
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/header/div/div[1]/div/div[2]/div/h3/span/div/span').click()
        except:
            print('Failed to click sell tab')

        price_string = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[1]/div[1]/div[2]/div[2]/span').text
        price_string = price_string.replace('$', '')
        price_string = price_string.replace(',', '')
        return float(price_string)

    def get_curr_market_price(self):
        thou = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[1]/section[1]/header/div[1]/h1/span/span/div/div[1]/span[2]').text
        hund = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[1]/section[1]/header/div[1]/h1/span/span/div/div[1]/span[4]').text
        tens = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[1]/section[1]/header/div[1]/h1/span/span/div/div[1]/span[5]').text
        ones = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[1]/section[1]/header/div[1]/h1/span/span/div/div[1]/span[6]').text
        dec1 = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[1]/section[1]/header/div[1]/h1/span/span/div/div[1]/span[8]').text
        dec2 = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div/div/div/div/div/div/div[1]/section[1]/header/div[1]/h1/span/span/div/div[1]/span[9]').text
        string = '{th}{hu}{te}{on}.{d1}{d2}'.format(th=thou, hu=hund, te=tens, on=ones, d1=dec1, d2=dec2)
        if thou=='' or hund=='' or tens=='' or ones=='' or dec1=='' or dec2=='':
            return 0
        else:
            return float(string)
        
        