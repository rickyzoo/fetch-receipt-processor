from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

## (Good) Example data

good_receipt_1 = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        },
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        },
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        },
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        }
    ],
    "total": "9.00"
}

good_receipt_2 = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        },
        {
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
        },
        {
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
        },
        {
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
        },
        {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
        }
    ],
    "total": "35.35"
}

good_receipt_3 = {
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
        {"shortDescription": "Dasani", "price": "1.40"}
    ]
}

good_receipt_4 = {
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "13:13",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}


def test_good_receipt_1(data: dict=good_receipt_1):
    post_response = client.post("/receipts/process", json=data)
    receipt_id = post_response.json()["id"]

    get_response = client.get(f"/receipts/{receipt_id}/points")

    assert post_response.status_code == 200
    assert post_response.json() == {"id": receipt_id}
    assert get_response.json() == {"points": 109}

def test_good_receipt_2(data: dict=good_receipt_2):
    post_response = client.post("/receipts/process", json=data)
    receipt_id = post_response.json()["id"]

    get_response = client.get(f"/receipts/{receipt_id}/points")

    assert post_response.status_code == 200
    assert post_response.json() == {"id": receipt_id}
    assert get_response.json() == {"points": 28}

def test_good_receipt_3(data: dict=good_receipt_3):
    post_response = client.post("/receipts/process", json=data)
    receipt_id = post_response.json()["id"]

    get_response = client.get(f"/receipts/{receipt_id}/points")

    assert post_response.status_code == 200
    assert post_response.json() == {"id": receipt_id}
    assert get_response.json() == {"points": 15}

def test_good_receipt_4(data: dict=good_receipt_4):
    post_response = client.post("/receipts/process", json=data)
    receipt_id = post_response.json()["id"]

    get_response = client.get(f"/receipts/{receipt_id}/points")

    assert post_response.status_code == 200
    assert post_response.json() == {"id": receipt_id}
    assert get_response.json() == {"points": 31}


## (Bad) Example data

bad_receipt_1 = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2", # Invalid purchase date
    "purchaseTime": "14:33",
    "items": [
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        },
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        },
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        },
        {
            "shortDescription": "Gatorade",
            "price": "2.25"
        }
    ],
    "total": "9.00"
}

bad_receipt_2 = {
    "retailer": "Target^^", # Invalid Retailer value
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        },
        {
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
        },
        {
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
        },
        {
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
        },
        {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
        }
    ],
    "total": "35.35"
}


def test_bad_receipt_1(data: dict=bad_receipt_1):
    post_response = client.post("/receipts/process", json=data)
    receipt_id = None

    get_response = client.get(f"/receipts/{receipt_id}/points")

    assert post_response.status_code == 400
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "No receipt found for that ID."}

def test_bad_receipt_2(data: dict=bad_receipt_2):
    post_response = client.post("/receipts/process", json=data)
    receipt_id = None

    get_response = client.get(f"/receipts/{receipt_id}/points")

    assert post_response.status_code == 400
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "No receipt found for that ID."}
