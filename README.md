# Limit Order Book: Simulating the Role of a Stock Broker

## Project Link
http://sahilg13.pythonanywhere.com

## About
This project is meant to be a simplified version of how stock brokers (ex: Charles Schwab, Fidelity, Robinhood, etc.) handle the process of matching the buyers and sellers of a particular stock. After reading the information below and running through the simulation, I hope that you leave with a better understanding of the types of orders that you can place for a stock and how these different types of orders are processed by the stock brokerage!

## Finance Crash Course
**Q:** What is a stock broker?  
**A:** A stock broker is a firm that acts as an intermediary between investors by connecting buyers with sellers.

**Q:** What is a limit order book?  
**A:** A limit order book is a record for a particular stock of all the existing buy and sell orders that have not yet been fulfilled. The "limit" part of the name comes from the fact that all of the orders in the book are limit orders. A limit order book is divided into two sides: the "bid" side and the "ask" side. The bid side keeps track of orders to buy the stock, whereas the ask side keeps track of orders to sell the stock. The bid side is sorted by price in descending order whereas the ask side is sorted by price in ascending order.

**Q:** What are the different types of orders that can be placed for a stock?  
**A:** The two main types of orders that can be placed are called limit orders and market orders. Both limit and market orders can be placed when buying a stock and when selling a stock. This gives us 4 different scenarios:  
1. Limit Buy Order: In this case, the person who placed the order is looking to buy the stock at the lowest available price on the ask side. However, they are not willing to spend more than X amount to obtain the stock. This price, denoted X, is the limit price. This order will not be executed unless a seller is offering to sell the stock at a price less than or equal to X.
2. Limit Sell Order: In this case, the person who placed the order is looking to sell the stock at the highest available price on the bid side. However, they are not willing to sell the stock for less than X amount. Again, we call this price X the limit price. This order will not be executed unless a buyer is offering to buy the stock at a price greater than or equal to X.
3. Market Buy Order: In this case, the person who placed the order is looking to buy the stock IMMEDIATELY at the lowest available price on the ask side. This type of buyer values speed and therefore wants their order to be processed at the best available price at that point in time.
4. Market Sell Order: In this case, the person who placed the order is looking to sell the stock IMMEDIATELY at the highest price available on the bid side. Again, this type of buyer values speed and therefore wants their order to be processed at the best available price at that point in time.

**Q:** Is a market order better than a limit order?  
**A:** There are advantages to each type of order. The main advantage of a market order is that it is always executed immediately. Since market orders are executed immediately, they never appear on the limit order book. The main advantage of a limit order is that the price is guaranteed to meet the constraint of the limit price. By utilizing a limit order, you can ensure that you don't pay too much to buy a stock or receive too little to sell a stock.

## Instructions
Once you have gone through the finance crash course, you are ready to simulate the processing of different orders! Once you click the project link, you will see two tables. The first table represents a randomly generated order. The second table represents the limit order book in its current state. When you are ready, you can click "Process Order" to see how the order is handled by the broker. Once you click "Process Order", the limit order book will be updated. If the order was able to be executed immediately, then you will see the matching order from the limit order book disappear. On the other hand, if the order was not able to be executed immediately, then it will be added to the limit order book. Once this processing takes place, then you will see that a new random order will generate. You can then continue the simulation by clicking "Process Order" each time to process each new order that comes in. When you are done or if you want to start over, feel free to click the "Clear Book" button to reset the book.

## Contributors
This project was completed individually by me, Sahil Goel.
