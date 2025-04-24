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
    offset = 0  # Keeps track of how much the positions have shifted

    # Step 1: NER for names (before modifying the text)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char
            entity_value = text[start:end]
            placeholder = "[full_name]"
            masked_text = masked_text[:start + offset] + placeholder + masked_text[end + offset:]
            entities.append({
                "position": [start + offset, start + offset + len(placeholder)],
                "classification": "full_name",
                "entity": entity_value
            })
            offset += len(placeholder) - (end - start)

    # Step 2: Regex-based PII (on already masked text)
    for key, pattern in PII_PATTERNS.items():
        # Fresh offset tracking for each pattern run
        new_text = masked_text
        offset = 0
        local_entities = []

        for match in re.finditer(pattern, masked_text):
            start, end = match.start(), match.end()
            entity_value = match.group()
            placeholder = f"[{key}]"

            # Insert mask and update positions
            new_text = new_text[:start + offset] + placeholder + new_text[end + offset:]
            local_entities.append({
                "position": [start + offset, start + offset + len(placeholder)],
                "classification": key,
                "entity": entity_value
            })
            offset += len(placeholder) - (end - start)

        # Apply all changes after each pattern to avoid overlap
        masked_text = new_text
        entities.extend(local_entities)

    return masked_text, entities


