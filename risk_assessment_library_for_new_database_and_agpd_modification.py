import math
# import pandas as pd
import csv
import numpy as np
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import math
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import datetime,timedelta
from numba import jit, cuda
import numpy as np
import statistics

filename = "agpd_with_days_1.txt"

class risk_assessment:
    alpha = 2/15
    ema_value=30
    price =0
    date =0
    date_14=0
    k_value = 50 
    list_of_date = []
    list_of_ending_price = []
    list_of_opening_price = []
    rsv_list=[]
    d_value = 50 
    k_list= []
    d_list = []
    MFI_list=[]
    list_of_maximum_price = [] 
    list_of_minimum_price = [] 
    sum_of_postive_ema_value =0
    sum_of_negative_ema_value =0
    list_of_volume_of_exchange=[]
    list_of_rate_of_change=[]
    list_after_editing = [] 
    list_of_volume_of_exchange_hand=[]
    list_of_rate_of_change_in_float=[]
    up = []
    down=[]
    ema_list= [] 
    ema_up =0 
    ema_down= 0
    rsi_list = []
    W_list=[]
    W_value = 0 
    a=0
    mfr=0
    comparing_date_purchase = []
    comparing_date_sell_off = []  
    strings=[]
    x=0
    actual_purchase = [] 
    actual_sell_off=[] 
    removal =0
    actual_actual_purchase =[]
    total_cost = []
    total_revenue =[]
    elasped_day = []
    number_of_trade = 0
    total_cost_value= 0
    total_revenue_value =0
    total_elasped_day= 0 
    ag = 0
    agpd=0
    revenue_per_year = 0
    buy_at_ending_price = []
    sell_at_ending_price =[]

    def __init__(self,number,area):
        self.close()
        self.number= number
        self.area=area
        stock_price_database = r"C:\Users\yiuki\Stockid_data\{}.{}.txt".format(self.number,self.area)
        f=open(stock_price_database,'r',encoding="utf8")
        self.strings = f.read().split("\n")
        self.strings = self.strings[:-1]
    def split_string(self):
        for string in self.strings:
            string = string.replace('"','')
            string12 = string.split(",", 5)
            # print(string12)

            self.list_of_date.append(string12[0])
            self.list_of_ending_price.append(string12[1])
            self.list_of_opening_price.append(string12[4])
            self.list_of_maximum_price.append(string12[2])
            self.list_of_minimum_price.append(string12[3])
            self.list_of_volume_of_exchange.append(string12[5])

        if (len(self.list_of_date)<35):
            return 10
        else: 
            return 1



            
            # self.list_of_rate_of_change.append(string12[6]) 
    def removing_million_and_thousands(self):
        for i in self.list_of_volume_of_exchange:
            x = len(i)
            string_remaining = i[0:x-1]
            # print(string_remaining)
            string_remaining=float(string_remaining)
            if (i[-1] == 'M'):
                string_remaining = string_remaining*1000000
            elif (i[-1]=="K"):
                string_remaining=string_remaining*1000000/1000
            # print(string_remaining)
            self.list_of_volume_of_exchange_hand +=[string_remaining]  
    def floating_list_of_volume_of_exchange_hand(self):
        self.list_of_volume_of_exchange_hand= [float(x) for x in self.list_of_volume_of_exchange]
    def reverse(self):
        self.list_of_date.reverse()
        self.list_of_ending_price.reverse()
        self.list_of_maximum_price.reverse()
        self.list_of_minimum_price.reverse()
        self.list_of_rate_of_change.reverse()
        self.list_of_volume_of_exchange_hand.reverse()
        self.list_of_opening_price.reverse()
    def get_date(self):
        x=13
        # date = input("What date")
        # self.date=date
        # print(date)
        # x=int(self.list_of_date.index(date))
        self.x=x
        print(x)
        self.a=x
    def rate_of_range(self):
        for i in self.list_of_rate_of_change:
            x=len(i)
            string_remaining = i[0:x-1]
            string_remaining = float(string_remaining)/100
            # print(string_remaining)
            self.list_of_rate_of_change_in_float+=[string_remaining]

    def MFI(self):
        list_of_ending_price= [float(x) for x in self.list_of_ending_price]
        # list_of_opening_price=[float(x) for x in self.list_of_opening_price]
        # reference_point = list_of_ending_price[self.x-8]
        # postve_flow = []
        money_postive_flow = []
        # negative_flow = []
        money_negative_flow = []
        # max_value = (max((list_of_ending_price))) ## define error => should use maximum price instead
        # min_value = min((list_of_ending_price))
        for i in range(14): ### here is the bug
            max_value= float(self.list_of_maximum_price[i+self.x-13])
            min_value=float(self.list_of_minimum_price[i+self.x-13])
            #print("Maximum value: " + str(max_value))
            #print("Minimum value: " + str(min_value))
            # print("index  : "+ str(self.list_of_volume_of_exchange_hand))
            # print(self.list_of_ending_price[self.x+i-13])
            # print(self.list_of_ending_price[self.x+i-13+1])
            # print(len(list_of_ending_price))
            # print(self.a+i-13)
            if (float(self.list_of_ending_price[self.x+i-13])-float(self.list_of_ending_price[self.x+i-13-1] ) > 0):  ## for some reasons, it cannot detect postive and negative correctly /. should be 14 days // new it is changed 
                # postve_flow.append(list_of_ending_price[x+i])
                # print(len(list_of_ending_price))
                # print(self.x+i-13)
                typical_price = (max_value+min_value+list_of_ending_price[self.x+i-13])/3 ## smae error here 
                #print(typical_price)
                raw_money = typical_price*self.list_of_volume_of_exchange_hand[self.x+i-13]
                # print(list_of_volume_of_exchange_hand[x+i])
                # print("Positive flow: " +str(raw_money))
                money_postive_flow.append(raw_money)
            else:
                # negative_flow.append(list_of_ending_price[x+i])
                # print(self.list_of_ending_price[self.x+i-13])
                typical_price = (max_value+min_value+list_of_ending_price[self.x+i-13])/3
                # print("typical price: " +str(typical_price))
                # print(self.x+i-13)
                # print(self.list_of_volume_of_exchange_hand[self.x+i-13+1])
                raw_money = typical_price*self.list_of_volume_of_exchange_hand[self.x+i-13]
                # print(list_of_volume_of_exchange_hand[x+i])
                # print("negative flow: " + str(raw_money))
                money_negative_flow.append(raw_money)

        total_postive_flow = sum(money_postive_flow)
        # print(total_postive_flow)
        total_negative_flow=sum(money_negative_flow)
            
        if total_negative_flow ==0:
            mfr = 10000000
        else:
            mfr = total_postive_flow/total_negative_flow
            # print("mfr: " +str(mfr))
            # MFR=1/MFR
            # print(mfr)


        MFI_value = 100 *(1-1/(1+mfr))
        # print(MFI_value)
        return MFI_value   
    def MFI_list1(self):
        for i in range(len(self.list_of_ending_price)-self.x):
            y=self.MFI()
            self.MFI_list.append(y)
            self.x+=1 
    # @jit(target_backend='cuda')                         
    def ema(self): ##tick should have no error laters
        list_of_ending_price = [float(x) for x in self.list_of_ending_price]
        # print(list_of_ending_price)
        # print("Maximum: :" +str(list_of_maximum_price[x]))
        # print("Minimum : " + str(list_of_minimum_price[x]))
        # print("Starting: " + str(list_of_opening_price[x]))
        for i in range(len(list_of_ending_price)-self.x): #ofbinzl -14
            if i ==0:
                continue
            else:
                if (list_of_ending_price[self.x-13+i-1] > list_of_ending_price[self.x-13+i+1-1] ):
                    self.down +=[ list_of_ending_price[self.x-13+i-1] - list_of_ending_price[self.x-13+i+1-1] ] # need to minus 1 for some reason
                    # print("1 down: " + str(list_of_ending_price[self.x-13+i-1]))
                    # print("2 down : " + str(list_of_ending_price[self.x-13+i]))
                    # print("result of down: " + str((list_of_ending_price[self.x-13+i-1] - list_of_ending_price[self.x-13+i] )))
                    # # print("down : " + str(down))
                    self.up.append(0)
                elif (list_of_ending_price[self.x-13+i+1-1] > list_of_ending_price[self.x-13+i-1]):
                    self.up += [list_of_ending_price[self.x-13+i+1-1]- list_of_ending_price[self.x-13+i-1]]
                    # print("1 up: " + str(list_of_ending_price[x-13+i]))
                    # print("2 up : " + str(list_of_ending_price[x-13+i-1]))
                    # print("result of up: " + str((list_of_ending_price[x-13+i] - list_of_ending_price[x-13+i-1] )))
                    self.down.append(0)
                    # print("up : " +str(up))
                else: 
                    self.up.append(0)
                    self.down.append(0)
        
        # print("up : "+str(self.up))
        ema_up = 0
        ema_down= 0 
        sum_ema_up_list = []
        sum_ema_down_list=[]
        for i in range(14):
            ema_up += self.up[i]*(1-self.alpha) ** (i)
            sum_ema_up_list.append(ema_up)
            ema_down += self.down[i]*(1-self.alpha) ** (i)
            sum_ema_down_list.append(ema_down)

        ema_up=ema_up/14
        ema_down=ema_down/14
        # print(ema_up)
        # print(ema_down)
        
        for i in range(len(self.up)-self.x-1): #currently, 7 days  => 14 days  len(list_of_ending_price)-14+x
            # print("up value: " + str(up[x+i+1]))
            ema_up = self.alpha*self.up[self.x+i+1] +(1-self.alpha)*ema_up  #orginally i+12
            # print("ema up : "+ str(ema_up))
            ema_down = self.alpha*self.down[self.x+i+1] +(1-self.alpha)*ema_down
            
            # print("ema down : "+ str(ema_down))   
            if ema_down == 0:
                ema_down= 1/1000
                rs =ema_up/ ema_down
            else:
                rs =ema_up/ ema_down
            # print("rs" + str(rs))
            rsi = (1-(1/(1+rs)))*100
            self.rsi_list.append(rsi)
    def RSV(self): ## should have no error --------the value will vary if the date is inputted at a wrong order -- now no error
        list_of_ending_price= [float(x) for x in self.list_of_ending_price]
        list_of_maximum_price= [float(x) for x in self.list_of_maximum_price]  
        list_of_minimum_price= [float(x) for x in self.list_of_minimum_price]  
        for i in range(len(self.list_of_date)): #orginally 7 days 
            if i < 13: 
                continue
            else: 
                max_value = max(list_of_maximum_price[i-13:i+1]) # use the maximum value of stock for today --> index is [x-13+i:x+i+1]
                # print("max value: " + str(max_value))
                min_value = min(list_of_minimum_price[i-13:i+1]) # use the maximum value of the stock for today  --[x-13+i+1:x+i+1]
                # print("min_value: "+str(min_value))
                # print(self.list_of_date[i])
                value = float(list_of_ending_price[i]) # use the stock price at that moment 
                # index out of range at that moment 
                # print("value" + str(value))
                
                if (max_value-min_value) ==0:
                    self.rsv_list.append(-1000000000000000)
                else:
                    self.rsv_list.append((value-min_value)/(max_value-min_value)*100)

        return self.rsv_list
    def K(self): ## should not have error
        for i in range(len(self.rsv_list)):
            self.k_value *=2/3
            # print(k_value)
            self.k_value +=  1/3*self.rsv_list[i]
            self.k_list.append(self.k_value)
    def D(self): # should not have error 
        for i in range(len(self.rsv_list)):
            self.d_value *= 2/3
            self.d_value += 1/3 * self.k_list[i]
            self.d_list.append(self.d_value)
    def W(self):
        print("Hello World")
        # print(len(MFI_list))

        # print(len(rsv_list))
        # print(len(self.d_list))
        # print(len(self.list_of_ending_price)-14-self.a+1)
        for i in range(len(self.list_of_ending_price)-14-self.a-1-14-14):  #len(list_of_ending_price)-14-a-1
            # print(i+a-11)
            # # print(type(MFI_list[i]))
            # print("MFI: " +str(MFI_list[i]))
            # print(rsi_list[i])
            # print(d_list[i+3])
            # print(d_list[i])
            W_value = (self.MFI_list[i]+self.rsi_list[i]+self.d_list[i+3])/3
            # print(W_value)
            self.W_list.append(W_value)
    # @jit(target_backend='cuda')                         
    def W_moderate(self):
        # print("Hello World")
        # print(len(MFI_list))

        # print(len(rsv_list))
        # print(len(self.rsi_list))
        # print(len(self.list_of_ending_price)-1-self.a-3)
        for i in range(len(self.list_of_ending_price)-2*self.a):  #len(list_of_ending_price)-14-a-1 #may cause bug => need to fix some bug arised from there
            # list_2=[]
            # print(i+a-11)
            # # print(type(MFI_list[i]))
            # print("MFI: " +str(MFI_list[i]))
            # print(rsi_list[i-2])
            # print(d_list[i])
            # print(d_list[i])
            list_1= []
            list_1.append(self.MFI_list[i])
            list_1.append(self.rsi_list[i-2])
            list_1.append(self.d_list[i])

            # W_value = (MFI_list[i]+rsi_list[i]+d_list[i+3])/3
            if W_moderate < 17:  #### 25
                # print("Time to purcharse as the W's value hits " + str(W_moderate)+ " Date:" + self.list_of_date[i+self.a] + " Price: " +str(self.list_of_ending_price[self.a+i]))
                self.comparing_date_purchase.append(i+self.a)
                # print("rsi : " +str(rsi_list[i-2]))
                # print("MFI: " +str(MFI_list[i]))
                # print("D value: " + str(d_list[i]))
            if W_sell> 45:
                # print("Time to sell off as W's value hits"+ str(W_moderate)+" Date" +self.list_of_date[i+self.a]+ " Price : " + str(self.list_of_ending_price[self.a+i]))
                self.comparing_date_sell_off.append(i+self.a)
    def convert_weekdays_to_days(self,elapsed_weekdays):
        complete_weeks = elapsed_weekdays // 5
        weekend_days = complete_weeks * 2
        remaining_weekdays = elapsed_weekdays % 5
        total_days = weekend_days + remaining_weekdays
        return total_days
    def calculate_elapsed_days(self,start_date, end_date):
        date_format = "%Y-%m-%d"
        start_datetime = datetime.strptime(start_date, date_format)
        end_datetime = datetime.strptime(end_date, date_format)

        elapsed_days = (end_datetime - start_datetime).days

        return elapsed_days
    # @jit(target_backend='cuda')                         
    def income(self):
        # print(self.comparing_date_purchase)
        # print(self.comparing_date_sell_off)
        buying_date=[]
        selling_date=[]
        for i in self.comparing_date_purchase:
            # print("Now that we are buying at that date:" + str(self.list_of_date[i]) + "at a price of " +str(self.list_of_ending_price[i]))
            self.buy_at_ending_price.append(self.list_of_ending_price[i])
            for j in self.comparing_date_sell_off:
                if j - i>=0:
                    # print("Now we are selling off at that date"+str(self.list_of_date[j])+ " at a price of " +str(self.list_of_ending_price[j]))
                    self.actual_purchase.append(i)
                    self.sell_at_ending_price.append(self.list_of_ending_price[j])
                    # print(self.actual_purchase)
                    # print(self.actual_sell_off)
                    # cost, difference = self.calucation_profit(float(self.list_of_ending_price[i]),float(self.list_of_ending_price[j]))
                    # self.total_cost.append(cost)
                    # self.total_revenue.append(difference)
                    # print(self.list_of_date[i])
                    # print(self.list_of_date[j])
                    buying_date.append(self.list_of_date[i])
                    selling_date.append(self.list_of_date[j])
                    # days = self.calculate_elapsed_days(self.list_of_date[i],self.list_of_date[j])
                    # self.elasped_day.append(days)
                    # self.actual_sell_off.append(j)
                    # self.number_of_trade+=1
                    break

        # print(self.actual_purchase)
        # print("elasped day: " +str((self.elasped_day)))

        # print("Buy now "+ str(buying_date))
        # print("Sell now " +str(selling_date))
        # print(self.buy_at_ending_price)
        # print(self.sell_at_ending_price)
        self.buy_at_ending_price, self.sell_at_ending_price=self.removing_stuff_from_the_list(self.buy_at_ending_price,self.sell_at_ending_price) ## skipping dates
        # print(self.buy_at_ending_price)
        # print(self.sell_at_ending_price)
        ##Have errors still => For some reasons it cannot coordinate with 300003 => need some hotfix => But don't have time => May need to do it later
        result_list_for_selling_dates , indices, unique_indeices_for_buying_list = self.remove_duplicates_with_indices(buying_date,selling_date) ## removing dates

        for i in range(len(unique_indeices_for_buying_list)):
            self.elasped_day.append(self.calculate_elapsed_days(unique_indeices_for_buying_list[i],result_list_for_selling_dates[i]))

        # print(self.elasped_day)
        self.total_elasped_day=sum(self.elasped_day)

        # print(self.sell_at_ending_price)
        # print(len(self.buy_at_ending_price))
        for i in range(len(self.sell_at_ending_price)):
            # print(i)
            cost, difference = self.calucation_profit(float(self.buy_at_ending_price[i]),float(self.sell_at_ending_price[i]))
            self.total_cost.append(cost)
            self.total_revenue.append(difference)

        # for j in range(len(selling_date)):
        #     if (selling_date[j] == selling_date[j-1]):
        # print(self.elasped_day)
        self.total_cost_value=sum(self.total_cost)
        # print(self.total_cost_value)
        # print(self.total_revenue)
        self.total_revenue_value  = sum(self.total_revenue)
        # print(self.total_revenue_value)
        if self.total_cost_value ==0:
            ag= - 0.0001
        else:
            ag = self.total_revenue_value/self.total_cost_value

        print("ag: " + str(ag))
        if len(self.elasped_day) ==0:
            agpd = -0.00001
        else:
            agpd = self.total_elasped_day/len(self.elasped_day)
            agpd = ag/agpd 
            
        print("agpd : " +str(agpd))
        revenue_per_year = (agpd+1)**(261) 
        print("revenue per year"+ str(revenue_per_year))

        if (len(self.elasped_day)>1):
            mean_days = statistics.mean(self.elasped_day)
        else:
            mean_days=0
        ####### elasped day part => if two same day => Will get deleted ##############
        # self.checking(self.elasped_day)
        # print(self.elasped_day)

        ############################

        #Below are modification when the price goes up and we stopped buying ##############################################
        
        # for i in range(len(self.actual_purchase)):
        #     # print("Number that we are doin"+str(self.actual_purchase[i]) + "Id number is: " + str(i))
        #     if i+1 >= len(self.actual_purchase):
        #         continue
        #     else:
        #         # self.removal +=1
        #         if self.actual_purchase[i] - self.actual_purchase[i-1] > 2:
        #             if float(self.list_of_ending_price[self.actual_purchase[i]])-float(self.list_of_ending_price[self.actual_purchase[i-1]]) >0:
        #                 print("Today" + self.list_of_ending_price[self.actual_purchase[i]] )
        #                 # print("Yesterday: "  +self.list_of_ending_price[self.actual_purchase[i-1]])
        #                 # print("difference : " + str(float(self.list_of_ending_price[self.actual_purchase[i]])-float(self.list_of_ending_price[self.actual_purchase[i-1]])))
        #                 # # self.actual_actual_purchase.remove(self.actual_purchase[i])
        #             else:
        #                 self.actual_actual_purchase.append(self.actual_purchase[i])
        #         else:
        #             self.actual_actual_purchase.append(self.actual_purchase[i])


        ##########################################################################################
        
        # print("Ideas" + str(self.actual_actual_purchase))
        # print("Actual purchase price" + str(list))

        # print(self.actual_purchase)
        # print(self.actual_sell_off)

        # for i in self.actual_actual_purchase:
        #     print(self.list_of_ending_price[i])

        if self.elasped_day==[]:
            days= 0
        else:
            days = len(self.elasped_day)

        return agpd,days,mean_days
    def removing_stuff_from_the_list(self,buy_list,sell_list):
        buy_list = [float(x) for x in buy_list]
        sell_list = [float(x) for x in sell_list]
        removal_list_in_buy_list= []
        removal_list_in_sell_list=[]
        for j in range(len(sell_list)): 
    # print("j" +str(j))
    # print("Second index" +str(j))
            if (j) > int(len(buy_list)):
                break
            else:
                if sell_list[j]==sell_list[j-1]:
                    if (buy_list[j]>buy_list[j-1]):
                        # print("index"+str(j))
                        # print("Too high" + str(buy_list[j]))
                        # print("Yesterday " +str(buy_list[j-1]))
                        # print("Where are we selling it to" + str(sell_list[j]))
                        # print("Are you sure about that" + str(sell_list[j-1]))
                        removal_list_in_buy_list.append(buy_list[j])
                        removal_list_in_sell_list.append(sell_list[j])
                        
        for i in removal_list_in_buy_list:
            buy_list.remove(i)
            
        for j in removal_list_in_sell_list:
            sell_list.remove(j)
        
        return buy_list,sell_list
    def remove_duplicates_with_indices(self,buying_date,selling_date):

        unique_list = []
        unique_indices = []
        unique_indices_for_buying_list = [] 
        seen = set()

        for index, item in enumerate(selling_date):
            if item not in seen:
                unique_list.append(item)
                unique_indices.append(index)
                unique_indices_for_buying_list.append(buying_date[index])
                seen.add(item)

        return unique_list, unique_indices, unique_indices_for_buying_list
    def calucation_profit(self,buy_price, sell_price):
        quantity = 10000/buy_price
        quantity = round(quantity,-2)
        # print(quantity)
        cost = quantity * buy_price*1.0028
        # print(cost)
        sell = quantity * sell_price
        # print(sell)
        difference = sell-cost
        return cost,difference
    def checking(self,list):    
        for i,val in enumerate(list):
            if abs(list[i]-list[i-1])<2:
                print(list[i])
                list.remove(list[i])
                self.checking(list)
        return list
    def monitoring_website(self):
        url = "https://quote.eastmoney.com/f1.html?newcode=0.{}".format(self.number)
        browser = webdriver.Chrome()
        browser.get(url)

        now = datetime.now() # current date and time

        list = []
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        print(current_datetime)
        str_current_datetime = current_datetime
        filename = str_current_datetime+"stock_price.txt"
        time.sleep(3)  
        while True:
            now = datetime.now()
            time1 = now.strftime("%H:%M:%S")
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            prices = soup.find_all('div',{'class': 'zxj'})
        
            for price in prices:
                price = price.find('span').get_text()
                print(price)

            with open(filename,'a') as f:
                f.write(str(current_datetime) + " " + time1 + " "+ price+ "\n" + " " ) 

            time.sleep(1)
    def close(self):
        # print("Hello")
        self.alpha = 2/15
        self.ema_value=30
        self.price =0
        self.date =0
        self.date_14=0
        self.k_value = 50 
        self.list_of_date = []
        self.list_of_ending_price = []
        self.list_of_opening_price = []
        self.rsv_list=[]
        self.d_value = 50 
        self.k_list= []
        self.d_list = []
        self.MFI_list=[]
        self.list_of_maximum_price = [] 
        self.list_of_minimum_price = [] 
        self.sum_of_postive_ema_value =0
        self.sum_of_negative_ema_value =0
        self.list_of_volume_of_exchange=[]
        self.list_of_rate_of_change=[]
        self.list_after_editing = [] 
        self.list_of_volume_of_exchange_hand=[]
        self.list_of_rate_of_change_in_float=[]
        self.up = []
        self.down=[]
        self.ema_list= [] 
        self.ema_up =0 
        self.ema_down= 0
        self.rsi_list = []
        self.W_list=[]
        self.W_value = 0 
        self.a=0
        self.mfr=0
        self.comparing_date_purchase = []
        self.comparing_date_sell_off = []  
        self.strings=[]
        self.x=0
        self.actual_purchase = [] 
        self.actual_sell_off=[] 
        self.removal =0
        self.actual_actual_purchase =[]
        self.total_cost = []
        self.total_revenue =[]
        self.elasped_day = []
        self.number_of_trade = 0
        self.total_cost_value= 0
        self.total_revenue_value =0
        self.total_elasped_day= 0 
        self.ag = 0
        self.agpd=0
        self.revenue_per_year = 0
        self.buy_at_ending_price = []
        self.sell_at_ending_price =[]
        self.strings =[]
        # self.number= 0
        # self.area = ""
        # print("clear")
        # self.__init__(self.number,self.area)
        # print(self.list_of_ending_price)
        # cache.clear()


# a= risk_assessment("600600","SS")
# # a= risk_assessment("300002","SZ")
# risk_assessment.split_string(a)
# # risk_assessment.removing_million_and_thousands(a)
# risk_assessment.floating_list_of_volume_of_exchange_hand(a)
# # risk_assessment.reverse(a)
# risk_assessment.get_date(a)
# # risk_assessment.rate_of_range(a)
# risk_assessment.RSV(a)
# risk_assessment.ema(a)
# risk_assessment.K(a)
# risk_assessment.D(a)
# risk_assessment.MFI_list1(a)
# risk_assessment.W_moderate(a)
# agpd = risk_assessment.income(a)
# risk_assessment.close(a)



a= risk_assessment("603077","SS")
# a= risk_assessment("300002","SZ")
risk_assessment.split_string(a)
# risk_assessment.removing_million_and_thousands(a)
risk_assessment.floating_list_of_volume_of_exchange_hand(a)
# risk_assessment.reverse(a)
risk_assessment.get_date(a)
# risk_assessment.rate_of_range(a)
risk_assessment.RSV(a)
risk_assessment.ema(a)
risk_assessment.K(a)
risk_assessment.D(a)
risk_assessment.MFI_list1(a)
risk_assessment.W_moderate(a)
agpd,day,mean_value = risk_assessment.income(a)
print(agpd)
print(day)
print(mean_value)
#301418 have errors too few datas

def convert_to_six_digit_string(number):
    return '{:06d}'.format(number)

list1 = ['SS']
agpd_list = []
# date = "2019-01-21"
agpd_1  = 0
stock_id_list = []
number_of_trade_list = []
mean_day_list=[]

for list in list1:
    for i in range(600050,603078):
        try:
            # i = str(i).zfill(6)
            i = convert_to_six_digit_string(i)
            # i =str(i)
            # y = len(i)
            # print(y)
            # i = str(i).zfill(7-y)
            print(i)
            print(list)
            # instance = risk_assessment()
            # instance.close()
            # a=a+str(i)
            a= risk_assessment(i,list)

        except IndexError: 
            print("Index Error")
            # time.sleep(0.5)
            # risk_assessment.close(a)
            pass
        except FileNotFoundError:
            print("File Not found error")
            # time.sleep(0.5)
            # risk_assessment.close(a)
            pass

        except ZeroDivisionError:
            print("Zero ")

        else:
            # print("Hello world")
            digit = risk_assessment.split_string(a)
            # risk_assessment.removing_million_and_thousands(a)
            # print(list_of_ending_price)
            if digit ==10:
                agpd_1 =-100
                print(agpd_1)
                agpd_list.append(agpd_1)
            else:
                risk_assessment.floating_list_of_volume_of_exchange_hand(a)
                # risk_assessment.reverse(a)
                risk_assessment.get_date(a)
                # risk_assessment.rate_of_range(a)
                risk_assessment.RSV(a)
                risk_assessment.ema(a)
                risk_assessment.K(a)
                risk_assessment.D(a)
                risk_assessment.MFI_list1(a)
                risk_assessment.W_moderate(a)
                agpd_1,day,mean_value = risk_assessment.income(a)
                number_of_trade_list.append(day)
                print(agpd_1)
                agpd_list.append(agpd_1)
                mean_day_list.append(mean_value)
                stock_id_list.append(i)
                risk_assessment.close(a)
                # time.sleep(1)

# #         # except:
# #         #     print("pass")

# # print(agpd_list)
# print(len(agpd_list))
# print(len(number_of_trade_list))
# for i in range(len(agpd_list)):
#     if (agpd_list[i] > 0.004 ):
#         if (number_of_trade_list[i]>=4):
#             with open(filename,'a+') as f:
#                 f.write(str(stock_id_list[i]) + " " + str(agpd_list[i]) + " "+ str(number_of_trade_list[i])+ " " + str(mean_day_list[i])+"\n") 
#             print("Stock id: " + str(stock_id_list[i]))
#             print("agpd: " +str(agpd_list[i]))
 


