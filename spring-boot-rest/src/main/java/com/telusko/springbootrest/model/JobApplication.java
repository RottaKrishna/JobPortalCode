package com.telusko.springbootrest.model;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
public class JobApplication {
    @Id

    private int applicationId;
    private int userId; // ID of the user who applied
    private int jobId;  // ID of the job that the user applied for
    private String status; // Status of the application (e.g., Pending, Accepted, Rejected)

}
