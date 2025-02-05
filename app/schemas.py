from pydantic import BaseModel, Field, constr
from typing import List
from datetime import datetime, time

"""
Some relevant Notes:
. The 'constr' class is used to implement the necessary Regex validation for the relevant fields
. Although an example formatting value was provided for the 'purchaseDate' field in the API spec, I wanted to cover other common and potentially possible formats for this field especially because it is coming in as a string value
    - The same logic does NOT apply to the 24-hour constricted 'purchaseTime' field
"""

class Item(BaseModel):
    shortDescription: constr(regex=r"^[\w\s\-]+$") = Field(..., description="The Short Product Description for the item")
    price: constr(regex=r"^\d+\.\d{2}$") = Field(..., description="The total price paid for this item")

    def get_price_as_float(self) -> float:
        """Convert string price to float for further processing"""
        return float(self.price)



class Receipt(BaseModel):
    retailer: constr(regex=r"^[\w\s\-&]+$") = Field(..., description="The name of the retailer or store the receipt is from")
    purchaseDate: str = Field(..., description="The date of the purchase printed on the receipt")
    purchaseTime: str = Field(..., description="The time of the purchase printed on the receipt. 24-hour time expected")
    items: List[Item] = Field(..., min_length=1, description="The list of item(s) purchased")
    total: constr(regex=r"^\d+\.\d{2}$") = Field(..., description="The total amount paid on the receipt")

    @validator("purchaseDate")
    def validate_purchase_date(cls, val):
        # List of common date formats in the US according to https://en.wikipedia.org/wiki/Date_and_time_notation_in_the_United_States
        date_formats = [
            "%B %-d, %Y", # January 1, 2022
            "%-d %B %Y", # 1 January 2022
            "%m/%d/%Y", # 01/01/2022
            "%Y-%m-%d", # 2022-01-01 (example provided in API spec)
            "%d %m %y", # 01 01 22
            "%d %m %Y", # 01 01 2022
        ]
        for fmt in date_formats:
            try:
                datetime.strptime(val, fmt)
                return val # return the original value for further processing if it's in an accepted format
            except ValueError:
                continue

        raise ValueError(
            "Invalid purchaseDate format. Examples of accepted formats: "
            "January 1, 2022 | 1 February 2022 | 01/01/2022 | 2022-01-01 | 01 01 22 | 01 01 2022"
        )

    @validator("purchaseTime")
    def validate_purchase_time(cls, val):
        try:
            datetime.strptime(val, "%H:%M")
            return val
        except ValueError:
            raise ValueError("Invalid purchaseTime format. Must be HH:MM in 24-hour format")

    def get_total_as_float(self) -> float:
        """Convert string total to float for further processing"""
        return float(self.total)

    
class ReceiptPostResponse(BaseModel):
    id: constr(regex=r"^\S+$")


class PointsGetResponse(BaseModel):
    points: int = Field(..., ge=0) # Greater-than-or-equal-to 0. We can't have negative points!


