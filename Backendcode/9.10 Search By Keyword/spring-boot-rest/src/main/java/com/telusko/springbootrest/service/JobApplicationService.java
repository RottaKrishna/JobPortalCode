package com.telusko.springbootrest.service;

// JobApplicationService.java (Service)
import com.telusko.springbootrest.model.JobApplication;
import com.telusko.springbootrest.model.User;
import com.telusko.springbootrest.repo.JobApplicationRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class JobApplicationService {

    @Autowired
    private JobApplicationRepo jobApplicationRepository;

    public JobApplication applyForJob(int applicationId, int userId, int jobId) {
        JobApplication jobApplication = new JobApplication();
        jobApplication.setApplicationId(applicationId);
        jobApplication.setUserId(userId);
        jobApplication.setJobId(jobId);
        jobApplication.setStatus("Pending"); // Default status when applying

        return jobApplicationRepository.save(jobApplication);
    }

    public void store() {
        List<JobApplication> applications = List.of(
                new JobApplication(200,101,1,"pending"),
                new JobApplication(201,102,2,"pending"),

                new JobApplication(202,103,3,"pending"),
                new JobApplication(203,104,4,"pending")
        );

       jobApplicationRepository.saveAll(applications);
    }

    public List<JobApplication> getAllApplications() {
        return jobApplicationRepository.findAll();
    }

    public void addApplication(JobApplication jobApplication) {
        jobApplicationRepository.save(jobApplication);
    }

    // Method to fetch job applications by user

}

