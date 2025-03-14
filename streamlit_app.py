import streamlit as st
import fitz  # PyMuPDF
import base64
from bs4 import BeautifulSoup

def pdf_to_html_converter(pdf_file):
    """Converts a PDF file to HTML using PyMuPDF."""
    try:
        doc = fitz.open(pdf_file)
        html_string = ""
        for page in doc:
            html_string += page.get_text("html")
        doc.close()
        return html_string
    except Exception as e:
        st.error(f"Error converting PDF to HTML: {e}")
        return None

def download_html(html_content, filename="converted.html"):
    """Creates a download link for HTML content."""
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="{filename}">Download HTML</a>'
    return href

def main():
    st.title("PDF to Editable HTML Converter")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        html_content = pdf_to_html_converter(uploaded_file)

        if html_content:
            st.subheader("Converted HTML (Read-Only Preview)")
            st.components.v1.html(html_content, height=600, scrolling=True)

            st.subheader("Editable HTML")
            edited_html = st.text_area("Edit the HTML below:", value=html_content, height=600)

            if edited_html != html_content:
              st.info("HTML has been edited.")

            st.markdown(download_html(edited_html), unsafe_allow_html=True)
            try:
                soup = BeautifulSoup(edited_html, 'html.parser')
                formatted_html = soup.prettify()
                st.download_button(
                    label="Download Formatted HTML",
                    data=formatted_html.encode('utf-8'),
                    file_name="edited_formatted.html",
                    mime="text/html",
                )
            except Exception as e:
                st.error(f"Error formating html: {e}")

if __name__ == "__main__":
    main()
