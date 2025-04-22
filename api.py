# api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import load_model
from utils import mask_pii

# Define FastAPI router
router = APIRouter()

# Load the trained email classifier model
model = load_model("models/email_classifier.pkl")

# Pydantic model to accept email body as input
class EmailRequest(BaseModel):
    email_body: str

# Route to classify email
@router.post("/classify_email")
def classify_email(request: EmailRequest):
    original_email = request.email_body
    # Mask PII from the email
    masked_email, entities = mask_pii(original_email)

    try:
        # Predict email category
        prediction = model.predict([masked_email])[0]
    except Exception:
        raise HTTPException(status_code=500, detail="Model prediction failed.")
    
    # Return email info along with prediction and masked entities
    return {
        "input_email_body": original_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": prediction
    }

# Define the /home GET route (new route)
@router.get("/home")
def home():
    return {"message": "This is the home page"}
