import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import pandas as pd
from chains import Chain
from utils import clean_text

# Load the portfolio DataFrame
portfolio = pd.read_csv(r"C:\Users\Asus\Documents\Projects\AI-ML\app\resources\my_portfolio.csv")


def create_streamlit_app(llm, portfolio_df, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Display a sample of the portfolio DataFrame
            st.write("Portfolio Data Loaded:")
            st.dataframe(portfolio_df.head())

            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                # Add logic to query links from the portfolio DataFrame based on skills
                links = []  # Placeholder until you implement actual logic
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    chain = Chain()
    create_streamlit_app(chain, portfolio, clean_text)
