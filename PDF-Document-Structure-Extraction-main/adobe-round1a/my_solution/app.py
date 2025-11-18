import streamlit as st
import pdfplumber
import json

# 1. Configure the page
st.set_page_config(page_title="PDF Extractor", layout="wide")

st.title("📄 PDF Structure to JSON Converter")
st.write("Upload a PDF file below to extract its text and table structure.")

# 2. File Uploader Widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # 3. Processing Logic
    with st.spinner('Extracting data...'):
        try:
            doc_content = []
            
            # pdfplumber can read directly from the uploaded file object
            with pdfplumber.open(uploaded_file) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_data = {
                        "page_number": i + 1,
                        "text": page.extract_text() or "",
                        "tables": page.extract_tables()
                    }
                    doc_content.append(page_data)
            
            # 4. Display Results
            st.subheader("Extraction Result")
            
            # Convert to JSON string for display and download
            json_str = json.dumps(doc_content, indent=4, ensure_ascii=False)
            
            # Show JSON on screen
            st.json(doc_content)
            
            # 5. Download Button
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name="extracted_data.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error processing file: {e}")