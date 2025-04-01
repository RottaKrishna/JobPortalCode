import streamlit as st
import requests
import pandas as pd

# Backend API URL
BASE_URL = "http://localhost:8080"

# Page Configuration
st.set_page_config(page_title="Job Portal", layout="wide")

# Sidebar Navigation
st.sidebar.title("Job Portal")
page = st.sidebar.radio("Navigation", ["View Jobs", "Add Job", "Edit Job", "Search Jobs", "Delete Job"])

# 1️⃣ View All Jobs
if page == "View Jobs":
    st.title("Available Jobs")
    response = requests.get(f"{BASE_URL}/jobPosts")
    
    if response.status_code == 200:
        jobs = response.json()
        df = pd.DataFrame(jobs)
        st.dataframe(df)  # Display jobs in a table
    else:
        st.error("Failed to fetch jobs")

# 2️⃣ Add a New Job
elif page == "Add Job":
    st.title("Post a Job")

    with st.form("job_form"):
        post_id = st.number_input("Job ID (Must be Unique)", min_value=1, step=1)  # Take Job ID
        title = st.text_input("Job Title")
        description = st.text_area("Job Description")
        experience = st.number_input("Required Experience (Years)", min_value=0, step=1)
        skills = st.text_input("Required Tech Stack (comma-separated)")  # Enter skills as comma-separated
        submit_btn = st.form_submit_button("Post Job")

    if submit_btn:
        job_data = {
            "postId": int(post_id),  # Convert to integer
            "postProfile": title,
            "postDesc": description,
            "reqExperience": int(experience),  # Convert to integer
            "postTechStack": skills.split(",")  # Convert to List
        }
        response = requests.post(f"{BASE_URL}/jobPost", json=job_data)

        if response.status_code == 200:
            st.success("Job added successfully!")
        else:
            st.error(f"Failed to add job: {response.text}")



# 3️⃣ Edit an Existing Job
elif page == "Edit Job":
    st.title("Edit Job Post")

    # Fetch all job posts
    jobs = requests.get(f"{BASE_URL}/jobPosts").json()

    if not jobs:
        st.warning("No jobs available to edit.")
    else:
        job_ids = {f"{job['postId']} - {job['postProfile']}": job["postId"] for job in jobs}
        selected_job = st.selectbox("Select a Job to Edit", list(job_ids.keys()))

        if selected_job:
            job_id = job_ids[selected_job]
            job_data = requests.get(f"{BASE_URL}/jobPost/{job_id}").json()

            # Ensure postTechStack is a list, even if null
            tech_stack = job_data.get("postTechStack", [])
            if not isinstance(tech_stack, list):
                tech_stack = []

            # Pre-fill form fields with existing values
            with st.form("edit_job_form"):
                new_title = st.text_input("Job Title", value=job_data.get("postProfile", ""))
                new_description = st.text_area("Job Description", value=job_data.get("postDesc", ""))
                new_experience = st.number_input("Required Experience (Years)", min_value=0, step=1, value=job_data.get("reqExperience", 0))
                new_skills = st.text_input("Required Tech Stack (comma-separated)", value=",".join(tech_stack))

                submit_btn = st.form_submit_button("Save Changes")

            # Process the form submission
            if submit_btn:
                updated_job = {
                    "postId": job_id,  # Keep the same postId
                    "postProfile": new_title,
                    "postDesc": new_description,
                    "reqExperience": int(new_experience),
                    "postTechStack": new_skills.split(",") if new_skills else []  # Convert string to list
                }

                response = requests.put(f"{BASE_URL}/jobPost", json=updated_job)

                if response.status_code == 200:
                    st.success("Job updated successfully!")
                else:
                    st.error(f"Failed to update job: {response.text}")


# 4️⃣ Search Jobs by Keyword
elif page == "Search Jobs":
    st.title("Search Jobs by Keyword")
    keyword = st.text_input("Enter keyword")
    
    if st.button("Search"):
        response = requests.get(f"{BASE_URL}/jobPosts/keyword/{keyword}")
        if response.status_code == 200:
            jobs = response.json()
            df = pd.DataFrame(jobs)
            st.dataframe(df)
        else:
            st.error("No matching jobs found!")

# 5️⃣ Delete a Job
elif page == "Delete Job":
    st.title("Delete a Job")
    job_id = st.number_input("Enter Job ID to Delete", min_value=1, step=1)
    
    if st.button("Delete"):
        response = requests.delete(f"{BASE_URL}/jobPost/{job_id}")
        if response.status_code == 200:
            st.success("Job deleted successfully!")
        else:
            st.error("Failed to delete job")

