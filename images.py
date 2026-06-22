from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import random
import os


def create_form_image(data, template_type='clinic', output_path='sample_form.jpg'):
    """
    Create a realistic form image from data
    """
    # Create image
    img = Image.new('RGB', (900, 700), color='white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 16)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()
        font_bold = font

    # Draw header
    if template_type == 'clinic':
        draw.text((50, 30), "PATIENT INTAKE FORM", fill='black', font=font_bold)
    elif template_type == 'school':
        draw.text((50, 30), "STUDENT REGISTRATION FORM", fill='black', font=font_bold)
    else:
        draw.text((50, 30), "BENEFICIARY ENROLLMENT FORM", fill='black', font=font_bold)

    draw.line([(50, 60), (850, 60)], fill='black', width=2)

    # Draw fields
    y = 100
    for key, value in data.items():
        if key != 'full_text' and value:
            draw.text((50, y), f"{key.replace('_', ' ').title()}: {value}", fill='black', font=font)
            y += 35

    # Draw border
    draw.rectangle([(20, 20), (880, y + 20)], outline='black', width=2)

    # Add form number
    draw.text((750, y + 30), f"Form #: {random.randint(1000, 9999)}", fill='gray', font=font)

    # Save
    img.save(output_path)
    print(f"✅ Created: {output_path}")
    return output_path


# Generate sample images
def generate_sample_forms():
    """
    Generate all sample form images
    """
    os.makedirs('data/sample_forms', exist_ok=True)

    # Sample data
    forms = [
        {
            'name': 'Muhammad Ahmed',
            'date': '15/06/2026',
            'phone': '0312-3456789',
            'email': 'ahmed@email.com',
            'address': 'House #42, Street 5, Lahore',
            'city': 'Lahore',
            'age': '45',
            'gender': 'Male',
            'diagnosis': 'Hypertension',
            'medication': 'Lisinopril 10mg',
            'symptoms': 'Headache, Dizziness',
            'type': 'clinic'
        },
        {
            'name': 'Fatima Ali',
            'date': '16/06/2026',
            'phone': '0333-9876543',
            'email': 'fatima@email.com',
            'address': 'House #15, Street 8, Karachi',
            'city': 'Karachi',
            'age': '32',
            'gender': 'Female',
            'diagnosis': 'Diabetes Type 2',
            'medication': 'Metformin 500mg',
            'symptoms': 'Fatigue, Increased Thirst',
            'type': 'clinic'
        },
        {
            'name': 'Usman Khan',
            'date': '17/06/2026',
            'phone': '0321-4567890',
            'email': 'usman@email.com',
            'address': 'House #78, Street 3, Islamabad',
            'city': 'Islamabad',
            'age': '28',
            'gender': 'Male',
            'diagnosis': 'Asthma',
            'medication': 'Salbutamol Inhaler',
            'symptoms': 'Wheezing, Shortness of Breath',
            'type': 'clinic'
        },
        {
            'name': 'Ayesha Malik',
            'date': '18/06/2026',
            'phone': '0345-6789012',
            'email': 'ayesha@email.com',
            'address': 'House #23, Street 12, Rawalpindi',
            'city': 'Rawalpindi',
            'age': '55',
            'gender': 'Female',
            'diagnosis': 'Tuberculosis',
            'medication': 'Rifampicin 150mg',
            'symptoms': 'Cough, Weight Loss',
            'type': 'clinic'
        },
        {
            'name': 'Hassan Shah',
            'date': '19/06/2026',
            'phone': '0332-7890123',
            'email': 'hassan@email.com',
            'address': 'House #91, Street 7, Faisalabad',
            'city': 'Faisalabad',
            'age': '38',
            'gender': 'Male',
            'diagnosis': 'Malaria',
            'medication': 'Chloroquine 250mg',
            'symptoms': 'Fever, Chills',
            'type': 'clinic'
        },
        {
            'name': 'Zara Hussain',
            'date': '20/06/2026',
            'phone': '0316-8901234',
            'email': 'zara@email.com',
            'address': 'House #67, Street 15, Multan',
            'city': 'Multan',
            'age': '42',
            'gender': 'Female',
            'diagnosis': 'Typhoid',
            'medication': 'Azithromycin 500mg',
            'symptoms': 'Fever, Abdominal Pain',
            'type': 'clinic'
        },
        {
            'name': 'Bilal Ahmed',
            'date': '21/06/2026',
            'phone': '0346-9012345',
            'email': 'bilal@email.com',
            'address': 'House #34, Street 22, Peshawar',
            'city': 'Peshawar',
            'age': '50',
            'gender': 'Male',
            'diagnosis': 'Dengue Fever',
            'medication': 'Paracetamol 500mg',
            'symptoms': 'High Fever, Joint Pain',
            'type': 'clinic'
        },
        {
            'name': 'Sana Tariq',
            'date': '22/06/2026',
            'phone': '0301-2345678',
            'email': 'sana@email.com',
            'address': 'House #56, Street 9, Quetta',
            'city': 'Quetta',
            'age': '29',
            'gender': 'Female',
            'diagnosis': 'Hepatitis B',
            'medication': 'Antiviral Therapy',
            'symptoms': 'Fatigue, Jaundice',
            'type': 'clinic'
        },
        {
            'name': 'Omar Farooq',
            'date': '23/06/2026',
            'phone': '0322-3456789',
            'email': 'omar@email.com',
            'address': 'House #89, Street 4, Hyderabad',
            'city': 'Hyderabad',
            'age': '62',
            'gender': 'Male',
            'diagnosis': 'Respiratory Infection',
            'medication': 'Ciprofloxacin 500mg',
            'symptoms': 'Cough, Fever',
            'type': 'clinic'
        },
        {
            'name': 'Nadia Khan',
            'date': '24/06/2026',
            'phone': '0334-5678901',
            'email': 'nadia@email.com',
            'address': 'House #12, Street 18, Gujranwala',
            'city': 'Gujranwala',
            'age': '48',
            'gender': 'Female',
            'diagnosis': 'Heart Disease',
            'medication': 'Amlodipine 5mg',
            'symptoms': 'Chest Pain, Fatigue',
            'type': 'clinic'
        }
    ]

    # Generate images
    for i, form in enumerate(forms, 1):
        data = {k: v for k, v in form.items() if k != 'type'}
        output_path = f'data/sample_forms/sample_form_{i:02d}.jpg'
        create_form_image(data, form['type'], output_path)

    print(f"\n✅ Generated {len(forms)} sample form images in data/sample_forms/")


# Run the generation
generate_sample_forms()