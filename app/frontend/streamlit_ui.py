import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("📚 Legal Document Summarizer")

# Upload PDF file
uploaded_file = st.file_uploader("Upload Legal PDF", type=["pdf"])
extracted_text = ""

if uploaded_file:
    if st.button("📤 Upload and Extract"):
        with st.spinner("Uploading to server..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            upload_res = requests.post(f"{API_BASE}/upload-pdf", files=files)

        if upload_res.status_code == 200:
            s3_key = upload_res.json()["key"]
            st.success("✅ Uploaded Successfully")

            with st.spinner("Extracting text from PDF..."):
                extract_res = requests.post(f"{API_BASE}/extract-pdf", json={"key": s3_key})

            if extract_res.status_code == 200:
                extracted_text = extract_res.json()["extracted_text"]
                st.text_area("📄 Extracted Text", extracted_text, height=300)
                st.session_state["extracted_text"] = extracted_text
            else:
                st.error("❌ Failed to extract text.")
        else:
            st.error("❌ Upload failed.")

# If extracted text is available, allow model selection and summarization
if "extracted_text" in st.session_state and st.session_state["extracted_text"]:
    st.markdown("### ✨ Select Summarization Model")
    model_choice = st.radio("Choose a model:", ["bart", "pegasus"])

    if st.button("📝 Summarize"):
        with st.spinner("Summarizing with selected model..."):
            sum_res = requests.post(
                f"{API_BASE}/summarize",
                json={
                    "text": st.session_state["extracted_text"],
                    "model": model_choice
                }
            )

        if sum_res.status_code == 200:
            summary = sum_res.json()["summary"]
            st.success("✅ Summary Generated")
            st.text_area("🧾 Summary", summary, height=200)
        else:
            st.error("❌ Summarization failed.")
