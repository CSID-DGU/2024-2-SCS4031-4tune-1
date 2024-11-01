package com.fortune.eyesee.dto;

import lombok.Data;

@Data
public class AdminSignupRequestDTO {
    private String adminEmail;
    private String password;
    private String passwordConfirm;
    private String adminName; // 회원가입 시 필요한 이름 필드
}