import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

# BACKEND #

#####
# This function is designed to initialize a limit order book before any orders
# are placed. The first two columns correspond to the bid side and the last
# two columns correspond to the ask side. All of the entries are initialized
# to NaN to indicate that there is no data present in the initial limit order
# book. One important distinction to note from a typical limit order book is
# that we are not keeping track of the number of shares for each order. This
# is due to the assumption that an order will either be to buy 1 share or to
# sell 1 share. This function returns a data frame which can be assigned to a
# variable as the limit order book.
#####
def init_lob():
    return pd.DataFrame(np.nan, index=list(range(101)), columns=["Time Bid Side", "Price Bid Side", "Time Ask Side", "Price Ask Side"])

#####
# This helper function processes a datetime object and turns it into a string.
#####
def reformat_lob_helper(x):
    if isinstance(x, datetime):
        return x.strftime("%I:%M:%S %p")
    else:
        return x

#####
# This function prepares the limit order book dataframe for printing on the website.
#####
def reformat_lob(lob):
    lob["Time Bid Side"] = lob["Time Bid Side"].apply(reformat_lob_helper)
    lob["Time Ask Side"] = lob["Time Ask Side"].apply(reformat_lob_helper)
    return lob

#####
# This function prepares the new order dataframe for printing on the website.
#####
def reformat_order(order):
    if isinstance(order["Order Time"][0], datetime):
        order["Order Time"][0] = order["Order Time"][0].strftime("%I:%M:%S %p")

    return order

#####
# This function is designed to randomly generate an order. The order will randomly
# be assigned as either a market or limit order. We will assume that an order has
# a 90% chance of being a limit order and a 10% chance of being a market order. Note
# that if a market buy/sell order is placed and there is no corresponding ask/bid
# order in the limit order book to fulfill the market order immediately, then the
# market order will fail to execute and be dropped. Additionally, the order will
# randomly be assigned as either a buy or sell order with equal probability. The
# order will also be assigned a time stamp that indicates the time that the order
# was placed. Finally, the order will be randomly assigned a price that falls within
# a realistic range of possible prices. For example, it doesn't make much sense to
# create a $1000 order for an asset trading at $100. In this simulation, we will select
# a random price between $70 and $80, with each price being equally likely. Also, note
# that we will assign a price of NaN to an order if it is a market order to indicate that
# the price is not applicable to the market order. This is just for convention. This
# function returns a data frame containing the order attributes. This function is used
# as input to the process_order function that processes the order and (if necessary)
# adds it to the limit order book.
#####
def gen_order():
    time = datetime.now() - timedelta(hours=4)
    type_binary = np.random.choice([0,1], size=1, replace=True, p=[0.9, 0.1])[0]
    type = "Market"
    direction_binary = np.random.choice([1,-1], size=1, replace=True)[0]
    direction = "Sell"
    price = np.nan

    if type_binary == 0:
        price = (np.random.choice(list(range(70,80)), size=1, replace=True) + np.random.choice(list(range(0,101)), size=1, replace=True)/100)[0]
        type = "Limit"

    if direction_binary == 1:
        direction = "Buy"

    return pd.DataFrame(data={"Order Time" : [time], "Order Type" : [type], "Order Direction" : [direction], "Order Price" : [price]})

#####
# This function is designed to compute the bid-ask spread. The bid-ask spread
# is defined as the price difference between the highest bid and the lowest ask.
# A string is returned with the bid-ask spread. If no bid-ask spread exists, then
# we simply return a dash.
#####
def get_spread(book):
    if (np.isnan(book["Price Bid Side"][0]) or np.isnan(book["Price Ask Side"][0])):
        return "-"
    else:
        return "$" + "{:.2f}".format(book["Price Ask Side"][0] - book["Price Bid Side"][0])

#####
# This function processes an order to the limit order book. The function returns the
# modified book which we will assign to the prior book variable in order to reflect
# the change.
#####
def process_order(book, new_order):
    if new_order["Order Type"][0] == "Market":
        if new_order["Order Direction"][0] == "Buy":
            # process a market-buy order

            # this if statement handles the case of when there are no asks
            if np.isnan(book["Price Ask Side"][0]):
                print("market order could not be executed due to 0 entries in ask side of limit order book")
                return book
            else:
                # match the market-buy with the top ask order in the limit order book

                for i in range(100):
                    book["Time Ask Side"][i] = book["Time Ask Side"][i+1]
                    book["Price Ask Side"][i] = book["Price Ask Side"][i+1]

                return book
        else:
            # process a market-sell order

            # this if statement handles the case of when there are no bids
            if np.isnan(book["Price Bid Side"][0]):
                print("market order could not be executed due to 0 entries in bid side of limit order book")
                return book
            else:
                # match the market-sell with the top bid order in the limit order book

                for i in range(100):
                    book["Time Bid Side"][i] = book["Time Bid Side"][i+1]
                    book["Price Bid Side"][i] = book["Price Bid Side"][i+1]

                return book
    else:
        if new_order["Order Direction"][0] == "Buy":
            # process a limit-buy order

            # this checks if there is an ask to match the limit-buy order
            if np.isnan(book["Price Ask Side"][0]) == False and new_order["Order Price"][0] >= book["Price Ask Side"][0]:
                # match the limit-buy with the top ask order in the limit order book

                for i in range(100):
                    book["Time Ask Side"][i] = book["Time Ask Side"][i+1]
                    book["Price Ask Side"][i] = book["Price Ask Side"][i+1]

                return book
            else:
                # the limit-buy order condition is not met so add it to the book

                i = 0
                # this while loop makes sure we don't inspect NaN cells
                while np.isnan(book["Price Bid Side"][i]) == False:
                    # this if statement checks if we have located the necessary place for insertion
                    if new_order["Order Price"][0] < book["Price Bid Side"][i]:
                        # we need to insert lower in the book so we go to the next row
                        i += 1
                    elif new_order["Order Price"][0] > book["Price Bid Side"][i]:
                        # we insert here
                        for j in range(99, i-1, -1):
                            book["Price Bid Side"][j+1] = book["Price Bid Side"][j]
                            book["Time Bid Side"][j+1] = book["Time Bid Side"][j]

                        book["Price Bid Side"][i] = new_order["Order Price"][0]
                        book["Time Bid Side"][i] = new_order["Order Time"][0]

                        return book
                    else:
                        # in this case, the prices are equal so we compare time stamps
                        if new_order["Order Time"][0] < book["Time Bid Side"][i]:
                            # we insert here
                            for j in range(99, i-1, -1):
                                book["Price Bid Side"][j+1] = book["Price Bid Side"][j]
                                book["Time Bid Side"][j+1] = book["Time Bid Side"][j]

                            book["Price Bid Side"][i] = new_order["Price"][0]
                            book["Time Bid Side"][i] = new_order["Order Time"][0]

                            return book
                        else:
                            # we need to insert lower in the book so we go to the next row
                            i += 1

                # if this code is reached then we insert at the very bottom
                book["Time Bid Side"][i] = new_order["Order Time"][0]
                book["Price Bid Side"][i] = new_order["Order Price"][0]

                return book
        else:
            # process a limit-sell order

            # this checks if there is a bid to match the limit-sell order
            if np.isnan(book["Price Bid Side"][0]) == False and new_order["Order Price"][0] <= book["Price Bid Side"][0]:
                # match the limit-sell with the top bid order in the limit order book
                for i in range(100):
                    book["Time Bid Side"][i] = book["Time Bid Side"][i+1]
                    book["Price Bid Side"][i] = book["Price Bid Side"][i+1]

                return book
            else:
                # the limit-sell order condition is not met so add it to the book
                i = 0

                # this while loop makes sure we don't inspect NA cells
                while np.isnan(book["Price Ask Side"][i]) == False:
                    # this if statement checks if we have located the necessary place for insertion
                    if new_order["Order Price"][0] > book["Price Ask Side"][i]:
                        # we need to insert lower in the book so we go to the next row
                        i += 1
                    elif new_order["Order Price"][0] < book["Price Ask Side"][i]:
                        # we insert here
                        for j in range(99, i-1, -1):
                            book["Price Ask Side"][j+1] = book["Price Ask Side"][j]
                            book["Time Ask Side"][j+1] = book["Time Ask Side"][j]

                        book["Price Ask Side"][i] = new_order["Order Price"][0]
                        book["Time Ask Side"][i] = new_order["Order Time"][0]

                        return book
                    else:
                        # in this case, the prices are equal so we compare time stamps
                        if new_order["Order Time"][0] < book["Time Ask Side"][i]:
                            # we insert here
                            for j in range(99, i-1, -1):
                                book["Price Ask Side"][j+1] = book["Price Ask Side"][j]
                                book["Time Ask Side"][j+1] = book["Time Ask Side"][j]

                            book["Price Ask Side"][i] = new_order["Order Price"][0]
                            book["Time Ask Side"][i] = new_order["Order Time"][0]

                            return book
                        else:
                            # we need to insert lower in the book so we go to the next row
                            i += 1

                # if this code is reached then we insert at the very bottom
                book["Time Ask Side"][i] = new_order["Order Time"][0]
                book["Price Ask Side"][i] = new_order["Order Price"][0]

                return book