from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime, time

"""
Some relevant Notes:
. Regex validation is covered using the 'pattern' parameter in the 'Field' class. Pydantic's built-in Error message is returned in the response
. Although an example formatting value was provided for the 'purchaseDate' field in the API spec, I wanted to cover other common and potentially possible formats for this field especially because it is coming in as a string value
    - The same logic does NOT apply to the explicitly specified 24-hour 'purchaseTime' field
"""

class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$", description="The Short Product Description for the item") # Allows alphanumeric, space, and hyphen values
    price: str = Field(..., pattern=r"^\d+\.\d{2}$", description="The total price paid for this item") # Constricts a decimal number to exactly 2 decimal places

    def get_price_as_float(self) -> float:
        """Convert string price to float for further processing. Handle negative dollar values"""
        price_as_float = float(self.price)
        if price_as_float < 0:
            return 0.00
        return price_as_float


class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$", description="The name of the retailer or store the receipt is from") # Allows alphanumeric, space, hyphen, and ampersand values
    purchaseDate: str = Field(..., description="The date of the purchase printed on the receipt")
    purchaseTime: str = Field(..., description="The time of the purchase printed on the receipt. 24-hour time expected")
    items: List[Item] = Field(..., min_length=1, description="The list of item(s) purchased")
    total: str = Field(..., pattern=r"^\d+\.\d{2}$", description="The total amount paid on the receipt")

    @field_validator("purchaseDate")
    def validate_purchase_date(cls, val):
        # List of common date formats in the US according to https://en.wikipedia.org/wiki/Date_and_time_notation_in_the_United_States
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
                datetime.strptime(val, fmt)
                return val # Return the original value for further processing if it's in an accepted format
            except ValueError:
                continue

        raise ValueError(
            "Invalid purchaseDate format. Examples of accepted formats: "
            "January 1, 2022 | 1 February 2022 | 01/01/2022 | 2022-01-01 | 01 01 22 | 01 01 2022"
        )

    @field_validator("purchaseTime")
    def validate_purchase_time(cls, val):
        try:
            datetime.strptime(val, "%H:%M")
            return val
        except ValueError:
            raise ValueError("Invalid purchaseTime format. Must be HH:MM in 24-hour format")

    def get_total_as_float(self) -> float:
        """Convert string total to float for further processing. Handle negative dollar values"""
        total_as_float = float(self.total)
        if total_as_float < 0:
            return 0.00
        return total_as_float

    
class PostReceiptResponse(BaseModel):
    id: str = Field(..., pattern=r"^\S+$") # No space characters allowed


class GetPointsResponse(BaseModel):
    points: int = Field(..., ge=0) # Greater-than-or-equal-to 0. We can't have negative points!


