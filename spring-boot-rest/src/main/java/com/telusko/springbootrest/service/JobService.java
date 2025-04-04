package com.telusko.springbootrest.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.telusko.springbootrest.model.JobPost;
import com.telusko.springbootrest.repo.JobRepo;


@Service
public class JobService {

    @Autowired
    public JobRepo repo;





    //method to return all JobPosts
    public List<JobPost> getAllJobs() {
        return repo.findAll();


    }









    // method to add a jobPost
    public void addJob(JobPost jobPost) {
        repo.save(jobPost);

    }




    //method to get job by id
    public JobPost getJob(int postId) {

        return repo.findById(postId).orElse(new JobPost());
    }




    //method to update job with job post object
    public void updateJob(JobPost jobPost) {
        repo.save(jobPost);

    }




    //method to delete job post by id
    public String deleteJob(int postId,int employerId) {
        Optional<JobPost> job = repo.findById(postId);
        if(job.isPresent())
        {
            JobPost jobpost = job.get();
            if(jobpost.getEmployerId()==employerId)
            {
                repo.delete(jobpost);
                return "JobPost Deleted Successfully";
            }
            else {
                return "UNAUTHORIZED";
            }}
        else
        {
            return "Job Not Found";
        }
    }











public void load() {
    // arrayList to store store JobPost objects
    List<JobPost> jobs =
            new ArrayList<>(List.of(
                    new JobPost(1, "Software Engineer", "Exciting opportunity for a skilled software engineer.", 3, List.of("Java", "Spring", "SQL","API"),103),
                    new JobPost(2, "Data Scientist", "Join our data science team and work on cutting-edge projects.", 5, List.of("Python", "Machine Learning", "TensorFlow","API"),104),
                    new JobPost(3, "Frontend Developer", "Create API amazing user interfaces with our talented frontend team.", 2, List.of("JavaScript", "React", "CSS","API"),103),
                    new JobPost(4, "Network Engineer", "Design and API maintain our robust network infrastructure.", 4, List.of("Cisco", "Routing", "Firewalls"),104),
                    new JobPost(5, "UX Designer", "Shape the user experience with your creative design skills.", 3, List.of("UI/UX Design", "Adobe XD", "Prototyping"),103)

            ));

    repo.saveAll(jobs);

}









public List<JobPost> search(String keyword) {

    return repo.findByPostProfileContainingOrPostDescContaining(keyword,keyword);
}


public List<JobPost> viewJobsByEmployerId(int employerId) {
    return repo.findJobsPostedByEmployer(employerId);
}
}
