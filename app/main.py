from typing import Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError


from app.core.schemas.schema import Receipt, PostReceiptResponse, GetPointsResponse
from app.core.services.receipt_processor import ReceiptProcessor


app = FastAPI()
receipt_service = ReceiptProcessor()

# Custom exception handler to override FastAPI's default 422 status code
# 'PlainTextResponse' is used to properly handle the ValueError raised in the 'purchaseDate' and 'purchaseTime' field validators since ValueError is not JSON serializable
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_body = exc.errors()
    error_msg = []
    # In the event that multiple field validation/value errors are raised from the same Request, we want to know them all
    for i in range(len(error_body)):
        error_msg.append(error_body[i]["msg"])
    error_msg_str = ", ".join(error_msg)

    return PlainTextResponse(str(error_msg_str), status_code=400)


@app.post("/receipts/process", status_code=200, response_model=PostReceiptResponse)
def process_receipt(receipt: Receipt) -> Dict[str, str]:
    try:
        receipt_id = receipt_service.process_receipt(receipt)
        return {"id": receipt_id}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="The receipt is invalid.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail="The receipt is invalid.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error occurred while processing the receipt.")


@app.get("/receipts/{id}/points", status_code=200, response_model=GetPointsResponse)
def get_points_of_receipt(id: str) -> Dict[str, int]:
    points = receipt_service.get_total_points(id)
    if points is None:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
        
    return {"points": points}
