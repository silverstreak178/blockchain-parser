from datetime import datetime, timedelta, date
import pandas as pd
from bitshares.blockchain import Blockchain
from bitshares.instance import shared_bitshares_instance
from bitsharesbase.operationids import getOperationNameForId

class History(object):
    """This class contains an algorithm to figure out the block numbers in
    the blockchain that the user's dates refer to."""

    def __init__(self):
        """ Initializes the History object. This method will be executed whenever
        we call an instance of the class."""
        self.chain = Blockchain(mode = 'head')
        current_block_num = self.chain.get_current_block_num()

        # The upper bound block number
        self.upper = current_block_num

        # The lower bound block number
        self.lower = 1

    def block_search(self, target_date):
        """ This call returns the block number corresponding to the date
        that was passed in. It uses a recursive loop that quickly searches for the block
        number by cutting the deck of block numbers in half every time and checking which
        half the desired date is in.
        The user is expected to pass in a date input through the user interface."""

        upper = self.upper
        lower = self.lower
        mid = (upper + lower)/2

        while((upper - mid)>=2):
            if target_date > self.chain.block_time(int(mid)):
                lower = int(mid)
                mid = int((upper + lower)/2)
            else:
                upper = int(mid)
                mid = int((upper + lower)/2)

        return mid

    def fees_parser(self, start_date, end_date, csv_file = "Untitled"):
        """ This parses the BitShares blockchain and aggregates historical fee data by type.
        The user is expected to input start and end dates on the user interface,
        which will be passed into this method. The dates need to be in datetime format."""

        # This will pass in the start date and retrieve the block number for the first block to parse
        begin = self.block_search(start_date)

        # This will pass in the end date and retrieve the block number for
        # the last block to parse. As we want to fully capture the transactions
        # of the last day, we will pass in the next day's date and stop at the block just prior.
        stop = self.block_search(end_date + timedelta(days = 1)) - 1

        # List to temporarily hold the dictionaries until we store them in a dataframe
        storage = []

        # We will iterate through the blocks and store relevant block information in a dictionary
        for blocknum in range(begin, stop + 1):

            # Dictionary to store block information
            block_data = dict()

            # To retrieve the blocks from the blockchain
            block = shared_bitshares_instance().rpc.get_block(blocknum)

            # Record the dates
            ts = pd.Timestamp(block["timestamp"])
            block_data["Date"] = datetime.date(ts)

            # Iterating through the data within each block
            for tx in block["transactions"]:
                for op in tx["operations"]:
                    key = getOperationNameForId(op[0])

                    # If the fee was paid in BTS, add the fee amount to the running total for each operation type
                    if op[1]["fee"].get("asset_id") == "1.3.0":
                        block_data[key] = block_data.get(key, 0) + op[1]["fee"].get("amount")

            # Append the dictionaries to the list for each block so that the data won't be lost
            storage.append(block_data)

        # Creating a dataframe to store the fee information
        data = pd.DataFrame(storage)
        data.fillna(0, inplace = True)

        # Aggregating at the daily level
        daily = data.groupby("Date")
        daily = daily.sum()
        daily.to_csv(str(csv_file)+".csv")
