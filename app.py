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
        with st.spinner("Generating Search Keywords..."):
            key_words = ask_groq(f"Based on this resume summary, suggest 3 specific job titles. Return ONLY the titles separated by commas.\n\n Summary: {summary}", max_tokens=50)
            keyword_list = [k.strip() for k in key_words.split(",")]

        st.success(f"Keywords identified: {', '.join(keyword_list)}")

        all_linkedin = []
        all_naukri = []

        for keyword in keyword_list:
            with st.spinner(f"Searching for {keyword}..."):
                # 1. LinkedIn (supports 10)
                l_jobs = fetch_linkdin_jobs(keyword, row=10) 
                all_linkedin.extend(l_jobs)
                
                # 2. Naukri (MUST be >= 50)
                n_jobs = fetch_naukri_jobs(keyword, row=50) # Changed from 10 to 50
                all_naukri.extend(n_jobs)


        st.markdown("---")
        st.header("Top LinkedIn Jobs")
        if all_linkedin:
            for job in all_linkedin:
                title = (job.get('Job Title') or job.get('title') or 
                        job.get('jobTitle') or job.get('positionName') or "Untitled Role")
                
                company = (job.get('Company Name') or job.get('company') or 
                        job.get('companyName') or job.get('name') or "Unknown Company")
                
                link = (job.get('Job Url') or job.get('url') or 
                        job.get('link') or job.get('job_url') or "#")

                st.write(f"### **{title}**")
                st.write(f"🏢 *{company}*")
                if link != "#":
                    st.write(f"🔗 [Apply Here]({link})")
                st.markdown("---")
