# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from utils import mask_pii
from models import load_model

app = FastAPI()
model = load_model()


class EmailRequest(BaseModel):
    email_body: str


@app.post("/classify_email")
async def classify_email(request: EmailRequest) -> Dict[str, Any]:
    email_text = request.email_body
    masked_email, masked_entities = mask_pii(email_text)
    predicted_category = model.predict([masked_email])[0]

    return {
        "input_email_body": email_text,
        "list_of_masked_entities": masked_entities,
        "masked_email": masked_email,
        "category_of_the_email": predicted_category
    }
