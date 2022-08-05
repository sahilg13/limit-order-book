from hashlib import new
import random
from statistics import mean
import numpy as np
import pandas as pd

# setting a random seed
random.seed(123)

##### 
# This function is designed to initialize a limit order book before any orders 
# are placed. The first two columns correspond to the bid side and the last 
# two columns correspond to the ask side. All of the entries are initialized 
# to NA to indicate that there is no data present in the initial limit order book.
# One important distinction to note from a typical limit order book is that we
# are not keeping track of the number of shares for each order. This is due to
# the assumption that an order will either be to buy 1 share or to sell 1 share. 
# This function returns a data frame which can be assigned to a variable as the 
# limit order book.
#####
def init_lob():
    return pd.DataFrame(np.nan, index=list(range(101)), columns=["Time_Bid_Side", "Price_Bid_Side", "Time_Ask_Side", "Price_Ask_Side"])

##### 
# This function is designed to randomly generate an order. The order will randomly
# be assigned as either a market or limit order. We will assume that an order has 
# a 90% chance of being a limit order and a 10% chance of being a market order. Note 
# that if a market buy/sell order is placed and there is no corresponding ask/bid 
# order in the limit order book to fulfill the market order immediately, then the 
# market order will fail to execute and be dropped. Additionally, the order will 
# randomly be assigned as either a buy or sell order with equal probability. The 
# order will also be sequentially assigned a time stamp that indicates the time 
# that the order was placed. For simplicity of the code, we will assume that the 
# orders are sent in increments of 1 unit of time. As a result, our 100 order simulation 
# will have time stamps ranging from 1-100. The key property of the time stamps is
# that for any given order, its time stamp is GREATER than the time stamp assigned 
# to the previous order but LESS than the time stamp assigned to the next order. 
# This maintains a sense of order when it comes to time stamps. Finally, the order 
# will be randomly assigned a price that falls within a realistic range of possible 
# prices. For example, it doesn't make much sense to create a $1000 order for an 
# asset trading at $100. In this simulation, we will select a random price between 
# $70 and $80, with each price being equally likely. Also, note that we will assign 
# a price of NA to an order if it is a market order to indicate that the price is not
# applicable to the market order. This is just for convention. This function returns 
# a data frame containing the order attributes. This function is used as input to the 
# process_order function that processes the order and (if necessary) adds it to the 
# limit order book.
#####
def gen_order(i):
    order_time_stamp = i
    order_m_flag = np.random.choice([0,1], size=1, replace=True, p=[0.9, 0.1])[0]
    order_trading_direction = np.random.choice([1,-1], size=1, replace=True)[0]
    order_price = np.nan

    if order_m_flag == 0:
        order_price = (np.random.choice(list(range(70,80)), size=1, replace=True) + np.random.choice(list(range(0,101)), size=1, replace=True)/100)[0]

    return pd.DataFrame(data={"order_time_stamp" : [order_time_stamp], "order_m_flag" : [order_m_flag], "order_trading_direction" : [order_trading_direction], "order_price" : [order_price]})

#####
# This function is designed to compute the bid-ask spread. It is called for each
# t between 1 and 100. If there is no bid-ask spread, then we return NA.
#####
def get_spread(book):
    if (np.isnan(book["Time_Bid_Side"][0]) or np.isnan(book["Time_Ask_Side"][0])):
        return np.nan
    else:
        return book["Price_Ask_Side"][0] - book["Price_Bid_Side"][0]

#####
# This function generates and submits 100 orders to the limit order book.
# The function returns the modified book which we will assign to the prior 
# book variable in order to reflect the change.
#####
def process_order(book, new_order):
    if new_order["order_m_flag"][0] == 1:
        if new_order["order_trading_direction"][0] == 1:
            # process a market-buy order

            # this if statement handles the case of when there are no asks
            if np.isnan(book["Price_Ask_Side"][0]):
                print("market order could not be executed due to 0 entries in ask side of limit order book")
                return book
            else:
                # match the market-buy with the top ask order in the limit order book
                
                for i in range(100):
                    book["Time_Ask_Side"][i] = book["Time_Ask_Side"][i+1]
                    book["Price_Ask_Side"][i] = book["Price_Ask_Side"][i+1]

                return book    
        else:
            # process a market-sell order

            # this if statement handles the case of when there are no bids
            if np.isnan(book["Price_Bid_Side"][0]):
                print("market order could not be executed due to 0 entries in bid side of limit order book")
                return book
            else:
                # match the market-sell with the top bid order in the limit order book

                for i in range(100):
                    book["Time_Bid_Side"][i] = book["Time_Bid_Side"][i+1]
                    book["Price_Bid_Side"][i] = book["Price_Bid_Side"][i+1]

                return book
    else:
        if new_order["order_trading_direction"][0] == 1:
            # process a limit-buy order

            # this checks if there is an ask to match the limit-buy order
            if np.isnan(book["Price_Ask_Side"][0]) == False and new_order["order_price"][0] >= book["Price_Ask_Side"][0]:
                # match the limit-buy with the top ask order in the limit order book

                for i in range(100):
                    book["Time_Ask_Side"][i] = book["Time_Ask_Side"][i+1]
                    book["Price_Ask_Side"][i] = book["Price_Ask_Side"][i+1]

                return book
            else:
                # the limit-buy order condition is not met so add it to the book
                
                i = 0
                # this while loop makes sure we don't inspect NaN cells
                while np.isnan(book["Time_Bid_Side"][i]) == False:
                    # this if statement checks if we have located the necessary place for insertion
                    if new_order["order_price"][0] < book["Price_Bid_Side"][i]:
                        # we need to insert lower in the book so we go to the next row
                        i += 1
                    elif new_order["order_price"][0] > book["Price_Bid_Side"][i]:
                        # we insert here
                        for j in range(99, i-1, -1):
                            book["Price_Bid_Side"][j+1] = book["Price_Bid_Side"][j]
                            book["Time_Bid_Side"][j+1] = book["Time_Bid_Side"][j]
                        
                        book["Price_Bid_Side"][i] = new_order["order_price"][0]
                        book["Time_Bid_Side"][i] = new_order["order_time_stamp"][0]

                        return book
                    else:
                        # in this case, the prices are equal so we compare time stamps
                        if new_order["order_time_stamp"][0] < book["Time_Bid_Side"][i]:
                            # we insert here
                            for j in range(99, i-1, -1):
                                book["Price_Bid_Side"][j+1] = book["Price_Bid_Side"][j]
                                book["Time_Bid_Side"][j+1] = book["Time_Bid_Side"][j]
                        
                            book["Price_Bid_Side"][i] = new_order["order_price"][0]
                            book["Time_Bid_Side"][i] = new_order["order_time_stamp"][0]

                            return book
                        else:
                            # we need to insert lower in the book so we go to the next row
                            i += 1

                # if this code is reached then we insert at the very bottom
                book["Time_Bid_Side"][i] = new_order["order_time_stamp"][0]
                book["Price_Bid_Side"][i] = new_order["order_price"][0]

                return book
        else:
            # process a limit-sell order

            # this checks if there is a bid to match the limit-sell order
            if np.isnan(book["Price_Bid_Side"][0]) == False and new_order["order_price"][0] <= book["Price_Bid_Side"][0]:
                # match the limit-sell with the top bid order in the limit order book
                for i in range(100):
                    book["Time_Bid_Side"][i] = book["Time_Bid_Side"][i+1]
                    book["Price_Bid_Side"][i] = book["Price_Bid_Side"][i+1]
                
                return book
            else:
                # the limit-sell order condition is not met so add it to the book
                i = 0

                # this while loop makes sure we don't inspect NA cells
                while np.isnan(book["Time_Ask_Side"][i]) == False:
                    # this if statement checks if we have located the necessary place for insertion
                    if new_order["order_price"][0] > book["Price_Ask_Side"][i]:
                        # we need to insert lower in the book so we go to the next row
                        i += 1
                    elif new_order["order_price"][0] < book["Price_Ask_Side"][i]:
                        # we insert here
                        for j in range(99, i-1, -1):
                            book["Price_Ask_Side"][j+1] = book["Price_Ask_Side"][j]
                            book["Time_Ask_Side"][j+1] = book["Time_Ask_Side"][j]
                        
                        book["Price_Ask_Side"][i] = new_order["order_price"][0]
                        book["Time_Ask_Side"][i] = new_order["order_time_stamp"][0]

                        return book
                    else:
                        # in this case, the prices are equal so we compare time stamps
                        if new_order["order_time_stamp"][0] < book["Time_Ask_Side"][i]:
                            # we insert here
                            for j in range(99, i-1, -1):
                                book["Price_Ask_Side"][j+1] = book["Price_Ask_Side"][j]
                                book["Time_Ask_Side"][j+1] = book["Time_Ask_Side"][j]
                        
                            book["Price_Ask_Side"][i] = new_order["order_price"][0]
                            book["Time_Ask_Side"][i] = new_order["order_time_stamp"][0]

                            return book
                        else:
                            # we need to insert lower in the book so we go to the next row
                            i += 1

                # if this code is reached then we insert at the very bottom
                book["Time_Ask_Side"][i] = new_order["order_time_stamp"][0]
                book["Price_Ask_Side"][i] = new_order["order_price"][0]
                
                return book                            

#####
# This function returns the updated book after clearing the market at the computed 
# equilibrium price. This function prints the equilibrium price for the call market. 
# If the equilibrium price does not exist, then the equilibrium price is printed as -1.
#####
def clear_market(book):
    # this if-statement checks if an equilibrium price exists
    if book["Price_Bid_Side"][0] < book["Price_Ask_Side"][0]:
        # an equilibrium price does not exist because there's no overlap in bid/ask prices

        # we print -1 to indicate no equilibrium and return the unmodified book
        print(-1)
        return book
    else:
        # we compute the equilibrium price

        price_bid = -1
        price_ask = -1

        # we match buyers and sellers (overlapped prices) until we hit the equilibrium
        while book["Price_Bid_Side"][0] >= book["Price_Ask_Side"][0]:
            # we record both sides of the overlapping orders (these eventually reach equilibrium)
            price_bid = book["Price_Bid_Side"][0]
            price_ask = book["Price_Ask_Side"][0]

            # we remove the top entry on both sides since they are overlapping prices
            for i in range(100):
                book["Price_Bid_Side"][i] = book["Price_Bid_Side"][i+1]
                book["Time_Bid_Side"][i] = book["Time_Bid_Side"][i+1]
                book["Price_Ask_Side"][i] = book["Price_Ask_Side"][i+1]
                book["Time_Ask_Side"][i] = book["Time_Ask_Side"][i+1]
            
            book["Price_Bid_Side"][100] = np.nan
            book["Time_Bid_Side"][100] = np.nan
            book["Price_Ask_Side"][100] = np.nan
            book["Time_Ask_Side"][100] = np.nan

        # we print the equilibrium price and return the updated book
        print(mean([price_bid, price_ask]))
        return book

## SIMULATION

# we initialize an empty limit order book
lob1 = init_lob()

#####
# We generate and submit 100 orders to the limit order book. After each order,
# the bid-ask spread is printed. Note that if you want to print each order, uncomment
# line 269. If you want to print the limit order book (lob1) after each order, 
# uncomment line 271.
#####

for i in range(1, 101):
    order = gen_order(i)
    print(order)
    lob1 = process_order(lob1, order)
    print(lob1)
    print("At t = " + str(i) + ", the bid-ask spread is " + str(get_spread(lob1)) + "\n")

# we clear the market at the clearing price, returning -1 if no such price exists
lob1 = clear_market(lob1)
