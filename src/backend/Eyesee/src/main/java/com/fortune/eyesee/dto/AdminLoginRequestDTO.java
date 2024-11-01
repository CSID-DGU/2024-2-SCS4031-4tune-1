package com.fortune.eyesee.dto;

import lombok.Data;

@Data
public class AdminLoginRequestDTO {
    private String adminEmail;
    private String password;
}