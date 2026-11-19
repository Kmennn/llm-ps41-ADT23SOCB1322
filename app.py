"""PS41 Resume Analyzer - Streamlit UI. Run: streamlit run app.py"""
import streamlit as st

from analyzer import MODEL, analyze, read_resume

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer")
st.caption(f"Compare your resume with a job description. Model: {MODEL} (local LLM)")

resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf", "txt"])
jd_text = st.text_area("Paste the job description", height=220)

if st.button("Analyze", type="primary"):
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Reading resume and asking the LLM..."):
            try:
                resume_text = read_resume(resume_file)
                if not resume_text:
                    st.error("No text found in the PDF. Is it a scanned image?")
                    st.stop()
                result = analyze(resume_text, jd_text)
            except Exception as err:
                st.error(f"Analysis failed: {err}")
                st.stop()

        score = result["match_score"]
        st.subheader(f"Match score: {score}/100")
        st.progress(score / 100)
        st.write(result["summary"])

        left, right = st.columns(2)
        with left:
            st.markdown("**✅ Matched skills**")
            for skill in result["matched_skills"] or ["(none)"]:
                st.markdown(f"- {skill}")
        with right:
            st.markdown("**❌ Missing skills**")
            for skill in result["missing_skills"] or ["(none)"]:
                st.markdown(f"- {skill}")

        st.markdown("**💡 3 tips to improve**")
        for i, tip in enumerate(result["tips"], 1):
            st.markdown(f"{i}. {tip}")

        with st.expander("Text extracted from your resume"):
            st.text(resume_text[:3000])
