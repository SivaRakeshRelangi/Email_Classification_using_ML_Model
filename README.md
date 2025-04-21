# Email_Classification_using_ML_Model

email-classification-api/
├── app.py                    # Main FastAPI entry point
├── api.py                    # Routes and API logic
├── models.py                 # Model training, saving, and loading
├── utils.py                  # PII masking and utilities
├── train_classifier.py       # One-time model training script
├── requirements.txt          # Dependencies
├── Dockerfile                # Docker configuration for Hugging Face deployment
├── /data/s.csv  # (Optional) Sample training data
└── /models/email_classifier.pkl  # Trained model (generated after training)
