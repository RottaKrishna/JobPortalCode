package com.telusko.springbootrest.repo;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import com.telusko.springbootrest.model.JobPost;


@Repository
public interface JobRepo extends JpaRepository<JobPost, Integer> {

	List<JobPost> findByPostProfileContainingOrPostDescContaining(String postProfile, String postDesc);

	@Query("SELECT jp FROM JobPost jp WHERE jp.employerId =:employerId")
	List<JobPost> findJobsPostedByEmployer(@Param("employerId") int employerId);
}
