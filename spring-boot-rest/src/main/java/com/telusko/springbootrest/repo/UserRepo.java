package com.telusko.springbootrest.repo;

import com.telusko.springbootrest.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepo extends JpaRepository<User, Integer> {
    Optional<User> findByUserNameAndIdAndRole(String userName, int id, String role);
}
