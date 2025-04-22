# utils.py
import re
import spacy

nlp = spacy.load("en_core_web_sm")

PII_PATTERNS = {
    "email": r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+",
    "phone_number": r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "aadhar_num": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/\d{2,4}\b",
    "dob": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
}


def mask_pii(text):
    entities = []
    masked_text = text

    # Regex-based masking
    for key, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, masked_text):
            start, end = match.start(), match.end()
            entity_value = match.group()
            masked_entity = f"[{key}]"
            entities.append({
                "position": [start, start + len(masked_entity)],
                "classification": key,
                "entity": entity_value
            })
            masked_text = masked_text[:start] + masked_entity + masked_text[end:]

    # Named Entity Recognition for names
    doc = nlp(masked_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char
            original_text = masked_text[start:end]
            masked_text = masked_text[:start] + "[full_name]" + masked_text[end:]
            entities.append({
                "position": [start, start + len("[full_name]")],
                "classification": "full_name",
                "entity": original_text
            })

    return masked_text, entities
