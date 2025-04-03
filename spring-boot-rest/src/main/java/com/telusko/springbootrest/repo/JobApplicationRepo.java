package com.telusko.springbootrest.repo;

// JobApplicationRepository.java (Repository)
import com.telusko.springbootrest.model.JobApplication;
import com.telusko.springbootrest.model.JobPost;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface JobApplicationRepo extends JpaRepository<JobApplication, Long> {
    @Query("SELECT jp FROM JobApplication ja JOIN JobPost jp ON ja.jobId=jp.postId WHERE ja.userId=:userId")
    List<JobPost> findJobsAppliedByEmployee(@Param("userId") int userId);
}

