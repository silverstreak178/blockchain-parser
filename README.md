# BitShares Blockchain Fees Parser
---
![alt text](https://user-images.githubusercontent.com/35355919/36348990-680b4e46-144a-11e8-9c4b-3e6072d8ea01.jpg "User Interface for the BitShares Blockchain Fees Parser")

The BitShares Blockchain Fees Parser is a tool, written in Python, with a desktop user interface that allows the user to select the start and end dates that he wants to aggregate the historical fee data for. Python's Tkinter library was used to create the desktop GUI for the application. 

## Motivation
While BitShares has multiple APIs and interfaces that users can use to access *current* market data and account information, there isn't an effective way to see historical data on the blockchain apart from just historical BTS market prices and volume. Although there are reports with historical data in graphical form that the BitShares community publishes, there doesn't appear to be a good way to access that historical data stored on the blockchain in spreadsheet form, where it is readily available for data analysis. This project attempts to rectify this, allowing the user to begin parsing the blockchain himself for the information.

## User Interface (user-interface.py)
This is the main script and includes the code for the front-end user interface. The user inputs the Start and End Dates for the time period to conduct his analysis. 

![alt text](https://user-images.githubusercontent.com/35355919/36349016-082856c6-144b-11e8-9f2d-a1d4dd4527e7.jpg "Using the BitShares Blockchain Fees Parser")

The output will be a saved CSV file with the aggregate fee information by date.

## Blockchain Parser (bts-blockchain-parser.py)
This contains the backend algorithms that:
* Figure out the block number in the blockchain based on the given date
* Parses the BitShares blockchain and aggregates the historical fees by operation type
