import streamlit as st
import requests

# Backend URL
BASE_URL = "http://localhost:8080"

# Login Page
def login_page():
    st.subheader("Login")

    # Inputs for user credentials
    user_name = st.text_input("Username")
    user_id = st.number_input("ID", min_value=1, step=1)
    role = st.radio("Role", ["Employee", "Employer"])

    if st.button("Login"):
        if user_name and user_id and role:
            login_data={"userName":user_name,
                        "id":str(user_id),
                        "role":role}
            responce = requests.post(f"{BASE_URL}/login",json=login_data)
            if responce.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.user_name = user_name
                st.session_state.user_role = role
                st.session_state.user_id = user_id
                st.success("Login Successful")
                st.session_state.first_run=False
            else:
                st.error("Invalid Credentials. Please try again.")
        else:
            st.warning("Please fill in all fields.")

# Employee Dashboard
def employee_dashboard():
    st.header("Employee Dashboard")

    tab1, tab2, tab3 = st.tabs(["View All Jobs", "Search Jobs", "Apply for Job"])

    # View All Jobs
    with tab1:
        st.subheader("All Available Jobs")

        # Create two columns for the job listings
        cols = st.columns(2)

        response = requests.get(f"{BASE_URL}/jobPosts")
        
        if response.status_code == 200:
            jobs = response.json()
            if jobs:
                for i, job in enumerate(jobs):
                    with cols[i % 2]:  # Alternate between the two columns
                        st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 16px; margin: 8px; border-radius: 8px; background-color: #f1f1f1;">
                                <h4 style="color: #333;">{job["postProfile"]} (ID: {job["postId"]})</h4>
                                <p style="color: #555;">{job["postDesc"]}</p>
                                <p style="color: #555;"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                                <p style="color: #555;"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                                <p style="color: #555;"><b>Employer ID:</b> {job["employerId"]}</p>
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
                            <div style="border: 1px solid #ddd; padding: 16px; margin: 8px; border-radius: 8px; background-color: #f1f1f1;">
                                <h4 style="color: #333;">{job["postProfile"]} (ID: {job["postId"]})</h4>
                                <p style="color: #555;">{job["postDesc"]}</p>
                                <p style="color: #555;"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                                <p style="color: #555;"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                                <p style="color: #555;"><b>Employer ID:</b> {job["employerId"]}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No jobs found for this keyword.")
            else:
                st.error("Failed to search jobs.")

    # Apply for Job
    with tab3:
        st.subheader("Apply for a Job")

        # Fetch jobs for selection
        jobs_response = requests.get(f"{BASE_URL}/jobPosts")
        if jobs_response.status_code == 200 and jobs_response.json():
            jobs = jobs_response.json()
            job_options = {job["postId"]: job["postProfile"] for job in jobs}
            selected_job_id = st.selectbox("Select Job ID to Apply", options=job_options.keys(), format_func=lambda x: f"{x} - {job_options[x]}")
            employee_id=st.number_input("Employee ID", min_value=1, step = 1)
            application_id=st.number_input("Application ID", min_value=1, step=1)
            # Inputs for job application
            

            if st.button("Apply"):
                # Create application data based on employee ID, selected job ID, and status
                application_data = {
                    "applicationId":application_id,
                    "userId": employee_id,  # Using the employee ID stored in session state
                    "jobId": selected_job_id,
                    "status": "Pending",  # Status is set to "Pending"
                    
                }

                # Send POST request to backend to submit application
                response = requests.post(f"{BASE_URL}/apply", json=application_data)

                if response.status_code == 200:
                    st.success("Applied successfully!")
                else:
                    st.error("Failed to apply for job.")

# Employer Dashboard
def employer_dashboard():
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

# Main Page Handling
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.first_run = True

if st.session_state.first_run:
    login_page()
else:
    if st.session_state.user_role == "Employee":
        employee_dashboard()
    elif st.session_state.user_role == "Employer":
        employer_dashboard()
