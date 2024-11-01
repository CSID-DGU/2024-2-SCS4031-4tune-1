package com.fortune.eyesee.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class AdminLoginResponseDTO {
    private Integer adminId;
    private String adminEmail;
    private String adminName;
}