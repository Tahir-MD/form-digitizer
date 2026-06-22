import streamlit as st
import pandas as pd
import cv2
import numpy as np
import easyocr
from PIL import Image, ImageEnhance, ImageFilter
import os
import re
from datetime import datetime
import io
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.preprocessor import preprocess_image
from utils.form_extractor import extract_form_fields

# Page Configuration
st.set_page_config(
    page_title="Form Digitizer - Tahir Mahmood",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .main-header h1 { font-size: 36px; margin: 0; font-weight: 700; }
    .main-header p { margin: 8px 0 0 0; opacity: 0.9; font-size: 16px; }
    .main-header .subtitle { font-size: 13px; opacity: 0.7; margin-top: 10px; }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #1a1a2e;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #1a1a2e; }
    .metric-label { font-size: 13px; color: #666; margin-top: 5px; }

    .rec-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 5px solid #1a1a2e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    .rec-card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    .rec-title { font-size: 16px; font-weight: 600; color: #1a1a2e; }
    .rec-description { color: #444; font-size: 14px; margin: 10px 0; line-height: 1.6; }

    @media (max-width: 768px) {
        .main-header h1 { font-size: 24px; }
        .metric-value { font-size: 22px; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📝 Handwritten/Printed Form Digitizer</h1>
    <p>AI-Powered Form Digitization for NGOs, Schools & Clinics</p>
    <div class="subtitle">Created by Tahir Mahmood | © 2026 | v2.0</div>
</div>
""", unsafe_allow_html=True)


# Initialize EasyOCR
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])


reader = load_ocr_reader()

# Session State
if 'results' not in st.session_state:
    st.session_state.results = []
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'source_type' not in st.session_state:
    st.session_state.source_type = None

# FUNCTION: Process Images with OCR
def process_images(uploaded_files):
    results = []
    progress_bar = st.progress(0)

    for idx, uploaded_file in enumerate(uploaded_files):
        # Update progress
        progress_bar.progress((idx + 1) / len(uploaded_files))

        # Save temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Process
        try:
            processed_img = preprocess_image(temp_path)
            result = reader.readtext(processed_img)
            form_data = extract_form_fields(result)
            form_data['filename'] = uploaded_file.name
            form_data['source'] = 'image'
            results.append(form_data)
        except Exception as e:
            st.warning(f"⚠️ Error processing {uploaded_file.name}: {e}")
            results.append({
                'filename': uploaded_file.name,
                'name': f'ERROR: {str(e)[:30]}',
                'source': 'image'
            })
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    progress_bar.empty()
    return results

# FUNCTION: Process CSV Data
def process_csv_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        results = []

        for _, row in df.iterrows():
            form_data = {
                'filename': row.get('filename', 'csv_form'),
                'name': row.get('name', None),
                'date': row.get('date', None),
                'phone': row.get('phone', None),
                'email': row.get('email', None),
                'address': row.get('address', None),
                'city': row.get('city', None),
                'age': str(row.get('age', '')) if pd.notna(row.get('age', '')) else None,
                'gender': row.get('gender', None),
                'diagnosis': row.get('diagnosis', None),
                'medication': row.get('medication', None),
                'symptoms': row.get('symptoms', None),
                'type': row.get('type', 'clinic'),
                'source': 'csv'
            }
            results.append(form_data)

        return results
    except Exception as e:
        st.error(f"Error processing CSV: {e}")
        return []


# ============================================================
# FUNCTION: Load Sample Data
# ============================================================
def load_sample_data():
    """
    Load sample form data from CSV file
    """
    sample_csv_path = 'data/sample_forms_data.csv'

    if os.path.exists(sample_csv_path):
        try:
            df = pd.read_csv(sample_csv_path)
            results = []

            for _, row in df.iterrows():
                form_data = {
                    'filename': row.get('filename', 'sample_form'),
                    'name': row.get('name', None),
                    'date': row.get('date', None),
                    'phone': row.get('phone', None),
                    'email': row.get('email', None),
                    'address': row.get('address', None),
                    'city': row.get('city', None),
                    'age': str(row.get('age', '')) if pd.notna(row.get('age', '')) else None,
                    'gender': row.get('gender', None),
                    'diagnosis': row.get('diagnosis', None),
                    'medication': row.get('medication', None),
                    'symptoms': row.get('symptoms', None),
                    'type': row.get('type', 'clinic'),
                    'source': 'sample'
                }
                results.append(form_data)

            return results
        except Exception as e:
            st.error(f"Error loading sample data: {e}")
            return []
    else:
        st.warning("⚠️ Sample data file not found at: data/sample_forms_data.csv")
        return []

# SIDEBAR

with st.sidebar:
    st.header("📁 Data Source")

    # SECTION 1: Upload Images
    st.subheader("📸 Upload Images")
    uploaded_images = st.file_uploader(
        "Upload Form Images",
        type=['jpg', 'jpeg', 'png', 'tiff', 'bmp'],
        accept_multiple_files=True,
        help="Upload images of filled forms"
    )

    if uploaded_images and st.button("🔄 Process Images", use_container_width=True, key="process_images"):
        with st.spinner("🔄 Processing images with AI..."):
            results = process_images(uploaded_images)
            if results:
                st.session_state.results = results
                st.session_state.processed = True
                st.session_state.source_type = "Images"
                st.success(f"✅ Processed {len(results)} forms from images!")
                st.rerun()

    st.markdown("---")

    # Upload CSV

    st.subheader("📊 Upload CSV Data")
    uploaded_csv = st.file_uploader(
        "Upload CSV File with Form Data",
        type=['csv'],
        help="Upload CSV with columns: name, date, phone, email, address, city, age, gender, diagnosis, medication, symptoms, type"
    )

    if uploaded_csv and st.button("📊 Load CSV Data", use_container_width=True, key="load_csv"):
        with st.spinner("📊 Loading CSV data..."):
            results = process_csv_data(uploaded_csv)
            if results:
                st.session_state.results = results
                st.session_state.processed = True
                st.session_state.source_type = "CSV"
                st.success(f"✅ Loaded {len(results)} records from CSV!")
                st.rerun()

    st.markdown("---")

    # Load Sample Data

    st.subheader("📝 Sample Data")
    if st.button("📝 Load Sample Pakistani Forms", use_container_width=True, key="load_sample"):
        with st.spinner("📝 Loading sample data..."):
            results = load_sample_data()
            if results:
                st.session_state.results = results
                st.session_state.processed = True
                st.session_state.source_type = "Sample Data"
                st.success(f"✅ Loaded {len(results)} sample forms!")
                st.rerun()
            else:
                st.error("❌ Failed to load sample data. Please check data/sample_forms_data.csv")

    st.markdown("---")


    # QUICK STATS

    if st.session_state.processed and st.session_state.results:
        st.markdown("### 📊 Quick Stats")
        df = pd.DataFrame(st.session_state.results)
        st.metric("Total Records", len(df))
        st.metric("Names Found", df['name'].notna().sum())
        st.metric("Source", st.session_state.source_type or "Unknown")

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 11px; color: #999; text-align: center;">
        <b>Form Digitizer v2.0</b><br>
        Built with ❤️ by Tahir Mahmood
    </div>
    """, unsafe_allow_html=True)

# MAIN CONTENT

if st.session_state.processed and st.session_state.results:
    df = pd.DataFrame(st.session_state.results)


    # METRICS

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df)}</div>
            <div class="metric-label">📄 Total Forms</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        names_found = df['name'].notna().sum()
        names_pct = (names_found / len(df) * 100) if len(df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #2ecc71;">
            <div class="metric-value">{names_found}</div>
            <div class="metric-label">👤 Names Found ({names_pct:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        dates_found = df['date'].notna().sum()
        dates_pct = (dates_found / len(df) * 100) if len(df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #f39c12;">
            <div class="metric-value">{dates_found}</div>
            <div class="metric-label">📅 Dates Found ({dates_pct:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        phones_found = df['phone'].notna().sum()
        phones_pct = (phones_found / len(df) * 100) if len(df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #9b59b6;">
            <div class="metric-value">{phones_found}</div>
            <div class="metric-label">📞 Phones Found ({phones_pct:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        source = st.session_state.source_type or "Unknown"
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #3498db;">
            <div class="metric-value" style="font-size: 18px;">{source}</div>
            <div class="metric-label">📂 Data Source</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")


    # DATA TABLE

    st.subheader("📊 Extracted Data")

    # Filter by source
    if 'source' in df.columns:
        sources = df['source'].unique().tolist()
        if sources:
            selected_source = st.selectbox("Filter by Source", ["All"] + sources)
            if selected_source != "All":
                df = df[df['source'] == selected_source]

    # Display columns
    display_cols = ['filename', 'name', 'date', 'phone', 'email', 'age', 'gender', 'city', 'diagnosis', 'source']
    display_cols = [col for col in display_cols if col in df.columns]
    st.dataframe(df[display_cols], use_container_width=True)


    # EXPORT

    st.markdown("---")
    st.subheader("📥 Export Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f'digitized_forms_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

    with col2:
        try:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Form Data', index=False)

                summary = pd.DataFrame({
                    'Metric': ['Total Forms', 'Names Found', 'Dates Found', 'Phones Found', 'Data Source'],
                    'Value': [
                        len(df),
                        df['name'].notna().sum(),
                        df['date'].notna().sum(),
                        df['phone'].notna().sum(),
                        st.session_state.source_type or "Unknown"
                    ]
                })
                summary.to_excel(writer, sheet_name='Summary', index=False)

                complete = df[df['name'].notna() & df['date'].notna()]
                if len(complete) > 0:
                    complete.to_excel(writer, sheet_name='Complete Forms', index=False)

            excel_data = output.getvalue()
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=f'digitized_forms_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"Excel export requires openpyxl: {e}")

    with col3:
        # JSON Export
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f'digitized_forms_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            mime='application/json',
            use_container_width=True
        )


    # RECOMMENDATIONS

    st.markdown("---")
    st.subheader("💡 Recommendations")

    if len(df) > 0:
        total = len(df)
        complete = df[df['name'].notna() & df['date'].notna() & df['phone'].notna()]
        complete_pct = (len(complete) / total * 100) if total > 0 else 0

        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-title">📊 Data Quality Summary</div>
            <div class="rec-description">
                • {names_found}/{total} forms have names extracted ({names_pct:.1f}%)<br>
                • {dates_found}/{total} forms have dates extracted ({dates_pct:.1f}%)<br>
                • {phones_found}/{total} forms have phone numbers extracted ({phones_pct:.1f}%)<br>
                • {len(complete)}/{total} forms are complete ({complete_pct:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

        if complete_pct >= 80:
            st.success("✅ Excellent! Most forms have complete data.")
        elif complete_pct >= 50:
            st.warning("⚠️ Good progress. Consider improving image quality for better accuracy.")
        else:
            st.error("❌ Low extraction rate. Please ensure forms are clear, well-lit, and legible.")

else:

    # WELCOME SCREEN

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ## 📝 Welcome to Form Digitizer

        ### Digitize handwritten forms in seconds!

        **Choose how to get started:**

        1️⃣ **Upload Images** - Take photos of forms and let AI extract data
        2️⃣ **Upload CSV** - Load pre-digitized data from CSV files
        3️⃣ **Sample Data** - Try with pre-loaded Pakistani sample forms

        ### Perfect for:
        - 🏥 **Clinics** - Patient intake forms
        - 🏫 **Schools** - Student registration forms  
        - 🏛️ **NGOs** - Beneficiary enrollment forms
        """)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08);">
            <h4>🚀 Key Features</h4>
            <ul style="list-style: none; padding: 0;">
                <li>✅ <b>Handwritten Text</b><br>AI-powered recognition</li>
                <li>✅ <b>Printed Text</b><br>High accuracy OCR</li>
                <li>✅ <b>Multiple Formats</b><br>Images, CSV, Sample Data</li>
                <li>✅ <b>Export Reports</b><br>CSV, Excel, JSON</li>
                <li>✅ <b>Free & Open-Source</b><br>No hidden costs</li>
            </ul>
            <div style="margin-top: 15px; padding: 10px; background: #f0f4ff; border-radius: 8px; text-align: center;">
                <span style="font-size: 12px; color: #1a1a2e;">Created by Tahir Mahmood © 2026</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# FOOTER

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px 0;">
    <b>Form Digitizer v2.0</b> | Created by Tahir Mahmood | © 2026
    <br>Built with ❤️ using EasyOCR, OpenCV & Streamlit
</div>
""", unsafe_allow_html=True)