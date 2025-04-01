package com.telusko.springbootrest.repo;

// JobApplicationRepository.java (Repository)
import com.telusko.springbootrest.model.JobApplication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JobApplicationRepo extends JpaRepository<JobApplication, Long> {

}

