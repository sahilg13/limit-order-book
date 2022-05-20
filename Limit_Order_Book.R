# setting a random seed
set.seed(123)

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
init_lob <- function() {
  Time_Bid_Side <- replicate(101, NA)
  Price_Bid_Side <- replicate(101, NA)
  Time_Ask_Side <- replicate(101, NA)
  Price_Ask_Side <- replicate(101, NA)
  
  return(data.frame(Time_Bid_Side, Price_Bid_Side, Time_Ask_Side, Price_Ask_Side))
}

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
gen_order <- function(i) {
  order_time_stamp <- i
  order_m_flag <- sample(c(0,1), size = 1, replace = TRUE, prob = c(0.90, 0.10))
  order_trading_direction <- sample(c(1,-1), size = 1, replace = TRUE)
  order_price <- NA
  if (order_m_flag == 0) {
    order_price <- sample(70:79, size = 1, replace = TRUE) + sample(0:100, size = 1, replace = TRUE)/100
  }
  
  return(data.frame(order_time_stamp, order_m_flag, order_trading_direction, order_price))
}

#####
# This function is designed to compute the bid-ask spread. It is called for each
# t between 1 and 100. If there is no bid-ask spread, then we return NA.
#####
get_spread <- function(book) {
  if (is.na(book$Time_Bid_Side[1]) || is.na(book$Time_Ask_Side[1])) {
    return(NA)
  } else {
    return(book$Price_Ask_Side[1] - book$Price_Bid_Side[1])
  }
}

#####
# This function generates and submits 100 orders to the limit order book.
# The function returns the modified book which we will assign to the prior 
# book variable in order to reflect the change.
#####
process_order <- function(book, new_order) {
  if (new_order$order_m_flag == 1) {
    if (new_order$order_trading_direction == 1) {
      # process a market-buy order
      
      # this if statement handles the case of when there are no asks
      if (is.na(book$Price_Ask_Side[1])) {
        print("market order could not be executed due to 0 entries in ask side of limit order book")
        return (book)
      } else {
        # match the market-buy with the top ask order in the limit order book
        
        for (i in 1:100) {
          book$Time_Ask_Side[i] <- book$Time_Ask_Side[i+1]
          book$Price_Ask_Side[i] <- book$Price_Ask_Side[i+1]
        }
        
        return(book)
      }
    } else {
      # process a market-sell order
      
      # this if statement handles the case of when there are no bids
      if (is.na(book$Price_Bid_Side[1])) {
        print("market order could not be executed due to 0 entries in bid side of limit order book")
        return (book)
      } else {
        # match the market-sell with the top bid order in the limit order book
        
        for (i in 1:100) {
          book$Time_Bid_Side[i] <- book$Time_Bid_Side[i+1]
          book$Price_Bid_Side[i] <- book$Price_Bid_Side[i+1]
        }
        
        return(book)
      }
    }
  } else {
    if (new_order$order_trading_direction == 1) {
      # process a limit-buy order
      
      # this checks if there is an ask to match the limit-buy order
      if (is.na(book$Price_Ask_Side[1]) == FALSE && new_order$order_price >= book$Price_Ask_Side[1]) {
        # match the limit-buy with the top ask order in the limit order book
        
        for (i in 1:100) {
          book$Time_Ask_Side[i] <- book$Time_Ask_Side[i+1]
          book$Price_Ask_Side[i] <- book$Price_Ask_Side[i+1]
        }
        
        return(book)
      } else {
        # the limit-buy order condition is not met so add it to the book
        
        i <- 1
        # this while loop makes sure we don't inspect NA cells
        while (is.na(book$Time_Bid_Side[i]) == FALSE) {
          # this if statement checks if we have located the necessary place for insertion
          if (new_order$order_price < book$Price_Bid_Side[i]) {
            # we need to insert lower in the book so we go to the next row
            i <- i + 1
          } else if (new_order$order_price > book$Price_Bid_Side[i]) {
            # we insert here
            for (j in 100:i) {
              book$Price_Bid_Side[j + 1] <- book$Price_Bid_Side[j]  
              book$Time_Bid_Side[j + 1] <- book$Time_Bid_Side[j]
            }
            
            book$Price_Bid_Side[i] <- new_order$order_price
            book$Time_Bid_Side[i] <- new_order$order_time_stamp
            
            return(book)
          } else {
            # in this case, the prices are equal so we compare time stamps
            if (new_order$order_time_stamp < book$Time_Bid_Side[i]) {
              # we insert here
              for (j in 100:i) {
                book$Price_Bid_Side[j + 1] <- book$Price_Bid_Side[j]  
                book$Time_Bid_Side[j + 1] <- book$Time_Bid_Side[j]
              }
              
              book$Price_Bid_Side[i] <- new_order$order_price
              book$Time_Bid_Side[i] <- new_order$order_time_stamp
              
              return(book)
            } else {
              # we need to insert lower in the book so we go to the next row
              i <- i + 1
            }
          }
        }
        
        # if this code is reached then we insert at the very bottom
        book$Time_Bid_Side[i] <- new_order$order_time_stamp
        book$Price_Bid_Side[i] <- new_order$order_price
        
        return(book)
      }
      
      
      
    } else {
      # process a limit-sell order
      
      # this checks if there is a bid to match the limit-sell order
      if (is.na(book$Price_Bid_Side[1]) == FALSE && new_order$order_price <= book$Price_Bid_Side[1]) {
        # match the limit-sell with the top bid order in the limit order book
        for (i in 1:100) {
          book$Time_Bid_Side[i] <- book$Time_Bid_Side[i+1]
          book$Price_Bid_Side[i] <- book$Price_Bid_Side[i+1]
        }
        
        return(book)
      } else {
        # the limit-sell order condition is not met so add it to the book
        i <- 1
        
        # this while loop makes sure we don't inspect NA cells
        while (is.na(book$Time_Ask_Side[i]) == FALSE) {
          # this if statement checks if we have located the necessary place for insertion
          if (new_order$order_price > book$Price_Ask_Side[i]) {
            # we need to insert lower in the book so we go to the next row
            i <- i + 1
          } else if (new_order$order_price < book$Price_Ask_Side[i]) {
            # we insert here
            for (j in 100:i) {
              book$Price_Ask_Side[j + 1] <- book$Price_Ask_Side[j]  
              book$Time_Ask_Side[j + 1] <- book$Time_Ask_Side[j]
            }
            
            book$Price_Ask_Side[i] <- new_order$order_price
            book$Time_Ask_Side[i] <- new_order$order_time_stamp
            
            return(book)
          } else {
            # in this case, the prices are equal so we compare time stamps
            if (new_order$order_time_stamp < book$Time_Ask_Side[i]) {
              # we insert here
              for (j in 100:i) {
                book$Price_Ask_Side[j + 1] <- book$Price_Ask_Side[j]  
                book$Time_Ask_Side[j + 1] <- book$Time_Ask_Side[j]
              }
              
              book$Price_Ask_Side[i] <- new_order$order_price
              book$Time_Ask_Side[i] <- new_order$order_time_stamp
              
              return(book)
            } else {
              # we need to insert lower in the book so we go to the next row
              i <- i + 1
            } 
          }
        }
        
        # if this code is reached then we insert at the very bottom
        book$Time_Ask_Side[i] <- new_order$order_time_stamp
        book$Price_Ask_Side[i] <- new_order$order_price
        return(book)
      }
    }  
  }
}

#####
# This function returns the updated book after clearing the market at the computed 
# equilibrium price. This function prints the equilibrium price for the call market. 
# If the equilibrium price does not exist, then the equilibrium price is printed as -1.
#####
clear_market <- function(book) {
  
  # this if-statement checks if an equilibrium price exists
  if (book$Price_Bid_Side[1] < book$Price_Ask_Side[1]) {
    # an equilibrium price does not exist because there's no overlap in bid/ask prices
    
    # we print -1 to indicate no equilibrium and return the unmodified book
    print(-1)
    return(book)
  } else {
    # we compute the equilibrium price
    
    price_bid <- -1
    price_ask <- -1
    
    # we match buyers and sellers (overlapped prices) until we hit the equilibrium
    while (book$Price_Bid_Side[1] >= book$Price_Ask_Side[1]) {
      # we record both sides of the overlapping orders (these eventually reach equilibrium)
      price_bid <- book$Price_Bid_Side[1]
      price_ask <- book$Price_Ask_Side[1]
      
      # we remove the top entry on both sides since they are overlapping prices
      for (i in 1:100) {
        book$Price_Bid_Side[i] <- book$Price_Bid_Side[i + 1]
        book$Time_Bid_Side[i] <- book$Time_Bid_Side[i + 1]
        book$Price_Ask_Side[i] <- book$Price_Ask_Side[i + 1]
        book$Time_Ask_Side[i] <- book$Time_Ask_Side[i + 1]
      }
      book$Price_Bid_Side[101] <- NA
      book$Time_Bid_Side[101] <- NA
      book$Price_Ask_Side[101] <- NA
      book$Time_Ask_Side[101] <- NA
    }
    
    # we print the equilibrium price and return the updated book
    print(mean(price_bid, price_ask))
    return(book)
  }
}

## SIMULATION

# we initialize an empty limit order book
lob1 <- init_lob()

#####
# We generate and submit 100 orders to the limit order book. After each order,
# the bid-ask spread is printed. Note that if you want to print each order, uncomment
# line 299. If you want to print the limit order book (lob1) after each order, 
# uncomment line 301.
#####
for (i in 1:100) {
  order <- gen_order(i)
  ##print(order)
  lob1 <- process_order(lob1, order)
  ##print(lob1)
  cat(cat(cat(cat("At t =", i), ", the bid-ask spread is"), get_spread(lob1)), "\n")
}

# we clear the market at the clearing price, returning -1 if no such price exists
lob1 <- clear_market(lob1)
