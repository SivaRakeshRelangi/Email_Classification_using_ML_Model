import pandas as pd
from models import train_model, save_model
from utils import mask_pii

# Read the dataset
df = pd.read_csv("data/combined_emails_with_natural_pii.csv")

# Apply PII masking to the emails
df["masked_email"] = df["email"].apply(lambda x: mask_pii(x)[0])

# Train the model
model = train_model(df["masked_email"], df["type"])

# Save the model as a pickle file
save_model(model, path="models/email_classifier.pkl")
