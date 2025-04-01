package com.telusko.springbootrest.service;

import com.telusko.springbootrest.model.JobPost;
import com.telusko.springbootrest.model.User;
import com.telusko.springbootrest.repo.UserRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepo userRepository;




    public void store() {
        List<User> users = List.of(
                new User("krishna", 101, "Employee"),
                new User("vamsi", 102, "Employee"),
                new User("venu", 103, "Employer"),
                new User("kishn", 104, "Employer")
        );

        userRepository.saveAll(users);
    }



    public List<User> getAllUsers() {
        return userRepository.findAll();


    }
    public boolean validateUser(String userName, int id, String role) {
        Optional<User> user1 = userRepository.findByUserNameAndIdAndRole(userName, id, role);
        return user1.isPresent();
    }
}
