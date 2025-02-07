import math
import uuid
from datetime import datetime

from app.core.schemas.schema import Receipt


class ReceiptProcessor:
    def __init__(self):
        # In-memory data store
        self._receipts = {}

        # Receipt_id-to-points cache
        self._points = {}

    ## Methods for each points addition scenario
     
    def calculate_points_from_retailer(self, receipt: Receipt) -> int:
        """Add 1 point for every alphanumeric character in the Retailer name"""
        points = 0
        for char in receipt.retailer:
            if char.isalnum():
                points += 1

        return points

    def calculate_points_from_total(self, receipt: Receipt) -> int:
        """
        Add 50 points if the total is a round dollar amount with no cents
        Add 25 points if the total is a multiple of 0.25
        """
        points = 0
        if receipt.get_total_as_float().is_integer():
            points += 50
        if (receipt.get_total_as_float() * 100) % 25 == 0:
            points += 25

        return points

    def calculate_points_from_num_items(self, receipt: Receipt) -> int:
        """Add 5 points for every TWO items"""

        return (len(receipt.items) // 2) * 5

    def calculate_points_from_item_description(self, receipt: Receipt, multiplier: float=0.2) -> int:
        """
        If the trimmed length of the item description is a multiple of 3, multiply the associated price by the multiplier (0.2 for this use-case) and round up to the nearest integer. The result is the points earned for each item
        NOTE that "trimmed length" implies the removal of trailing & leading space characters BUT counts in-between space characters
        """
        points = 0
        for item in receipt.items:
            if len(item.shortDescription.strip()) % 3 == 0:
                points += math.ceil((item.get_price_as_float() * multiplier))

        return points

    def calculate_points_from_purchase_date(self, receipt: Receipt) -> int:
        """Add 6 points if the day in purchaseDate is ODD"""
        points = 0
        accepted_date_formats = [
            "%B %d, %Y", # January 1, 2022
            "%d %B %Y", # 1 January 2022
            "%m/%d/%Y", # 01/01/2022
            "%Y-%m-%d", # 2022-01-01 (example provided in API spec)
            "%d %m %y", # 01 01 22
            "%d %m %Y", # 01 01 2022
        ]
        for fmt in accepted_date_formats:
            try:
                day = datetime.strptime(receipt.purchaseDate, fmt).day
                if day % 2 == 1:
                    points += 6
                    break
            except ValueError:
                continue

        return points

    def calculate_points_from_purchase_time(self, receipt: Receipt) -> int:
        """Add 10 points if purchaseTime is between 2-4pm exclusive"""
        points = 0
        purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M").time()
        start_time = datetime.strptime("14:00", "%H:%M").time()
        end_time = datetime.strptime("16:00", "%H:%M").time()

        if start_time < purchase_time < end_time:
            points += 10

        return points


    ## Methods called in API Endpoints

    def sum_of_points(self, receipt: Receipt) -> int:
        """Sum of all earned points for a given Receipt"""
        return sum([
            self.calculate_points_from_retailer(receipt),
            self.calculate_points_from_total(receipt),
            self.calculate_points_from_num_items(receipt),
            self.calculate_points_from_item_description(receipt),
            self.calculate_points_from_purchase_date(receipt),
            self.calculate_points_from_purchase_time(receipt),
        ])

    def process_receipt(self, receipt: Receipt) -> str:
        """Process a given Receipt, generate a uniqueID, and return it"""
        receipt_id = str(uuid.uuid4()) # .uuid4 creates a random UUID value
        self._receipts[receipt_id] = receipt # Store k-v pair in in-memory data store
        
        return receipt_id

    def get_total_points(self, receipt_id: str) -> int:
        """Get points for a given Receipt by its uniqueID"""
        points = self._points.get(receipt_id) # First check the points cache
        if not points:
            receipt = self._receipts.get(receipt_id)
            if not receipt: # If the Receipt_id is not in the points cache AND does not exist in the receipts cache, then this is an invalid request
                return None
            else:
                total_points = self.sum_of_points(receipt)
                self._points[receipt_id] = total_points # If the Receipt exists but does not live in the points cache, then this the first GET request for the given receipt_id. Add it to the cache
                return total_points

        return points


