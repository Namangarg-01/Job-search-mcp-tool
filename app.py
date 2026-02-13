import streamlit as st
from src.helper import extract_text_from_pdf, ask_groq
from src.jobs_api import fetch_linkdin_jobs, fetch_naukri_jobs

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("AI Job Recommender📃")
st.markdown("Upload resume to get job recomm. based on your skills and experience from linkdin and naukri")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume"): # Loading Button
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your Resume"):
        summary = ask_groq(
            f"Summarize this resume highlighting the skills, education and experience : \n\n {resume_text}", 
            max_tokens=500
        )
    
    with st.spinner("Finding Skill Gaps"):
        skill_gaps = ask_groq(
            f"Analyze this resume and highlight missing skills, certification and experiences and other things needed for better job opportunities: \n\n {resume_text}",
            max_tokens=500
        )

    with st.spinner("Creating.... Future road Map"):
        road_map = ask_groq(
            f"Based on this resume sugget future roadmap to improve this person's career prospects (skill to learn, certification needed, industry exposure): \n\n {resume_text}",
            max_tokens=400
        )

    st.markdown("---")
    st.header("📜 Resume Summary")
    st.markdown(f"<div style='background-color: #0d0d0d; padding: 20px; border-radius: 10px; border: 1px solid #333;'> <p style='color: #ffffff;'>{summary}</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #0d0d0d; padding: 20px; border-radius: 10px; border: 1px solid #333;'> <p style='color: #ffffff;'>{skill_gaps}</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap and Prepration Strategy")
    st.markdown(f"<div style='background-color: #0d0d0d; padding: 20px; border-radius: 10px; border: 1px solid #333;'> <p style='color: #ffffff;'>{road_map}</p></div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")

    if st.button("🔎 Get Job Recommendation"):
        with st.spinner("Fetching Job Recommendation."):
            key_words = ask_groq(f"Based on this resume summary, Suggest 3 specific job titles for this resume. Return ONLY the titles separated by commas, no numbers or bullets.\n\n Summary: {summary}", max_tokens=50)
            search_query = [k.strip() for k in key_words.split(",")]

        st.success(f"Searching for: {search_query}")

        with st.spinner("Fetching Jobs from Linkdin and Naukri"):
            all_jobs = []
            for keyword in search_query:
                st.write(f"Searching for {keyword}...")
                results = fetch_linkdin_jobs(keyword, row=10)
                linkdin_jobs = fetch_linkdin_jobs(search_query, row=60)
                naukri_jobs = fetch_naukri_jobs(search_query, row=60)

        st.markdown("---")
        st.header("Top Linkdin Jobs")

        if linkdin_jobs:
            for job in linkdin_jobs:
                title = job.get('Job Title') or job.get('title') or "Untitled Role"
                company = job.get('Company Name') or job.get('company') or "Unknown Company"
                location = job.get('Job Location') or job.get('location') or "India"
                link = job.get('Job Url') or job.get('url') or job.get('link')

                st.markdown(f"### **{title}**")
                st.markdown(f"🏢 *{company}*")
                st.markdown(f"📍 {location}")
                if link:
                    st.markdown(f"🔗 [Apply on LinkedIn]({link})")
                st.markdown("---")
        else:
            st.warning("No Linkdin jobs found")

        if naukri_jobs:
            for job in naukri_jobs:
                title = job.get('title') or job.get('jobTitle') or "No Title"
                company = job.get('companyName') or job.get('company') or "Unknown Company"
                location = job.get('location') or job.get('jobLocation') or "No Location"
                link = job.get('link') or job.get('jobUrl') or job.get('url') or "#"

                st.markdown(f"### **{title}**")
                st.markdown(f"🏢 *{company}*")
                st.markdown(f"📍 {location}")
                st.markdown(f"🔗 [View Job Details]({link})")
                st.markdown("---")
        else:
            st.warning("No Naukri Jobs found")

