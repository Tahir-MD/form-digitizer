import re
def extract_form_fields(text_results):

    # Combine all detected text
    full_text = ' '.join([item[1] for item in text_results])

    form_data = {
        'name': None,
        'date': None,
        'phone': None,
        'email': None,
        'address': None,
        'city': None,
        'age': None,
        'gender': None,
        'school_name': None,
        'patient_name': None,
        'diagnosis': None,
        'medication': None,
        'symptoms': None,
        'full_text': full_text[:500]
    }

    # Name patterns
    name_patterns = [
        r'(?:Name|Full Name|Patient Name|Student Name|Applicant Name)[:\s]+([A-Za-z\s\.]+?)(?:\n|$)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+)'
    ]

    for pattern in name_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            potential_name = match.group(1).strip()
            if re.match(r'^[A-Za-z\s\.]+$', potential_name):
                form_data['name'] = potential_name[:50]
                break

    # Date patterns
    date_patterns = [
        r'(?:Date|DOB|Birth Date|Submission Date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    ]

    for pattern in date_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            form_data['date'] = match.group(1)
            break

    # Phone
    phone_match = re.search(r'(\+?1?[\s-]?\(?[0-9]{3}\)?[\s-]?[0-9]{3}[\s-]?[0-9]{4})', full_text)
    if phone_match:
        form_data['phone'] = phone_match.group(1)

    # Email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', full_text)
    if email_match:
        form_data['email'] = email_match.group()

    # Age
    age_match = re.search(r'(?:Age|AGE)[:\s]+(\d{1,3})', full_text, re.IGNORECASE)
    if age_match:
        form_data['age'] = age_match.group(1)

    # Gender
    gender_match = re.search(r'(?:Gender|SEX)[:\s]+(M|F|Male|Female|Other)', full_text, re.IGNORECASE)
    if gender_match:
        form_data['gender'] = gender_match.group(1)

    # School Name
    school_patterns = [
        r'(?:School|School Name|Institution)[:\s]+([A-Za-z\s\.]+?)(?:\n|$)',
        r'([A-Za-z\s]+(?:School|Academy|College|University))'
    ]

    for pattern in school_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            form_data['school_name'] = match.group(1).strip()[:50]
            break

    # Patient Name
    patient_match = re.search(r'(?:Patient Name|Patient)[:\s]+([A-Za-z\s\.]+?)(?:\n|$)', full_text, re.IGNORECASE)
    if patient_match:
        form_data['patient_name'] = patient_match.group(1).strip()[:50]

    # Diagnosis
    diagnosis_match = re.search(r'(?:Diagnosis|Diagnosis)[:\s]+([A-Za-z\s\.]+?)(?:\n|$)', full_text, re.IGNORECASE)
    if diagnosis_match:
        form_data['diagnosis'] = diagnosis_match.group(1).strip()[:100]

    # Medication
    medication_match = re.search(r'(?:Medication|Medicine|Drug)[:\s]+([A-Za-z\s\.]+?)(?:\n|$)', full_text,
                                 re.IGNORECASE)
    if medication_match:
        form_data['medication'] = medication_match.group(1).strip()[:100]

    # Symptoms
    symptoms_match = re.search(r'(?:Symptoms|Symptom)[:\s]+([A-Za-z\s\.]+?)(?:\n|$)', full_text, re.IGNORECASE)
    if symptoms_match:
        form_data['symptoms'] = symptoms_match.group(1).strip()[:100]

    # Address
    address_match = re.search(r'(?:Address|Addr)[:\s]+(.{10,100}?)(?:\n|$)', full_text, re.IGNORECASE)
    if address_match:
        form_data['address'] = address_match.group(1).strip()[:100]

    return form_data