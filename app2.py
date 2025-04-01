import streamlit as st
import requests
import pandas as pd

# Backend URL
BASE_URL = "http://localhost:8080"

st.title("Job Portal")

# Sidebar for role selection
role = st.sidebar.radio("Login as:", ["Employee", "Employer"])

# Apply custom CSS styles for job cards
st.markdown("""
    <style>
    .job-card {
        background-color: #ffffff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #007BFF;
    }
    .job-title {
        font-size: 18px;
        font-weight: bold;
        color: #007BFF;
    }
    .job-description {
        font-size: 14px;
        color: #555;
        margin: 5px 0;
    }
    .job-info {
        font-size: 13px;
        color: #777;
        margin: 2px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Employee Dashboard
if role == "Employee":
    st.header("Employee Dashboard")

    tab1, tab2 = st.tabs(["View All Jobs", "Search Jobs"])

    # View All Jobs
    with tab1:
        st.subheader("All Available Jobs")
        response = requests.get(f"{BASE_URL}/jobPosts")
        
        if response.status_code == 200:
            jobs = response.json()
            if jobs:
                for job in jobs:
                    st.markdown(f"""
                        <div class="job-card">
                            <p class="job-title">{job["postProfile"]} (ID: {job["postId"]})</p>
                            <p class="job-description">{job["postDesc"]}</p>
                            <p class="job-info"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                            <p class="job-info"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                            <p class="job-info"><b>Employer ID:</b> {job["employerId"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No jobs available.")
        else:
            st.error("Failed to fetch jobs.")

    # Search Jobs
    with tab2:
        st.subheader("Search Jobs")
        keyword = st.text_input("Enter keyword to search for jobs")
        if st.button("Search"):
            search_response = requests.get(f"{BASE_URL}/jobPosts/keyword/{keyword}")
            if search_response.status_code == 200:
                search_results = search_response.json()
                if search_results:
                    for job in search_results:
                        st.markdown(f"""
                            <div class="job-card">
                                <p class="job-title">{job["postProfile"]} (ID: {job["postId"]})</p>
                                <p class="job-description">{job["postDesc"]}</p>
                                <p class="job-info"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                                <p class="job-info"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                                <p class="job-info"><b>Employer ID:</b> {job["employerId"]}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No jobs found for this keyword.")
            else:
                st.error("Failed to search jobs.")

# Employer Dashboard
elif role == "Employer":
    st.header("Employer Dashboard")

    tab1, tab2, tab3 = st.tabs(["Add Job", "Update Job", "Delete Job"])

    # Add Job
    with tab1:
        st.subheader("Add a New Job")
        post_id = st.number_input("Job ID", min_value=1, step=1)
        employer_id = st.number_input("Employer ID", min_value=1, step=1)
        post_profile = st.text_input("Job Role")
        post_desc = st.text_area("Job Description")
        req_experience = st.number_input("Required Experience (Years)", min_value=0, step=1)
        post_tech_stack = st.text_input("Required Tech Stack (comma-separated)")
        
        if st.button("Add Job"):
            job_data = {
                "postId": post_id, 
                "employerId": employer_id,
                "postProfile": post_profile,
                "postDesc": post_desc,
                "reqExperience": req_experience,
                "postTechStack": post_tech_stack.split(",")  # Convert to list
            }
            response = requests.post(f"{BASE_URL}/jobPost", json=job_data)

            if response.status_code == 200:
                st.success("Job added successfully!")
            else:
                st.error("Failed to add job.")

    # Update Job
    with tab2:
        st.subheader("Update an Existing Job")
        
        # Fetch jobs for selection
        jobs_response = requests.get(f"{BASE_URL}/jobPosts")
        if jobs_response.status_code == 200 and jobs_response.json():
            jobs = jobs_response.json()
            job_options = {job["postId"]: job["postProfile"] for job in jobs}
            selected_job_id = st.selectbox("Select Job ID to Update", options=job_options.keys(), format_func=lambda x: f"{x} - {job_options[x]}")

            # Fetch job details for the selected job
            job_data = next((job for job in jobs if job["postId"] == selected_job_id), None)
            
            if job_data:
                employer_id = st.number_input("Employer ID", min_value=1, step=1, value=job_data["employerId"])
                new_profile = st.text_input("Job Role", value=job_data["postProfile"])
                new_desc = st.text_area("Job Description", value=job_data["postDesc"])
                new_experience = st.number_input("Required Experience (Years)", min_value=0, step=1, value=job_data["reqExperience"])
                new_skills = st.text_input("Required Tech Stack (comma-separated)", value=",".join(job_data["postTechStack"]))

                if st.button("Save Changes"):
                    updated_job = {
                        "postId": selected_job_id,
                        "employerId": employer_id,
                        "postProfile": new_profile,
                        "postDesc": new_desc,
                        "reqExperience": new_experience,
                        "postTechStack": new_skills.split(",")
                    }
                    update_response = requests.put(f"{BASE_URL}/jobPost", json=updated_job)

                    if update_response.status_code == 200:
                        st.success("Job updated successfully!")
                    else:
                        st.error("Failed to update job.")

        else:
            st.warning("No jobs available for updating.")

    # Delete Job
    with tab3:
        st.subheader("Delete a Job")

        # Fetch jobs for selection
        jobs_response = requests.get(f"{BASE_URL}/jobPosts")
        if jobs_response.status_code == 200 and jobs_response.json():
            jobs = jobs_response.json()
            job_options = {job["postId"]: job["postProfile"] for job in jobs}
            selected_job_id = st.selectbox("Select Job ID to Delete", options=job_options.keys(), format_func=lambda x: f"{x} - {job_options[x]}")

            if st.button("Delete Job"):
                delete_response = requests.delete(f"{BASE_URL}/jobPost/{selected_job_id}")

                if delete_response.status_code == 200:
                    st.success("Job deleted successfully!")
                else:
                    st.error("Failed to delete job.")
        else:
            st.warning("No jobs available for deletion.")
