package com.fortune.eyesee.service;

import com.fortune.eyesee.common.exception.BaseException;
import com.fortune.eyesee.common.response.BaseResponseCode;
import com.fortune.eyesee.dto.AdminLoginRequestDTO;
import com.fortune.eyesee.dto.AdminLoginResponseDTO;
import com.fortune.eyesee.dto.AdminSignupRequestDTO;
import com.fortune.eyesee.entity.Admin;
import com.fortune.eyesee.repository.AdminRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AdminService {
    @Autowired
    private AdminRepository adminRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    // 회원가입 메서드
    public Admin registerAdmin(AdminSignupRequestDTO adminSignupRequestDTO) {
        if (adminRepository.findByAdminEmail(adminSignupRequestDTO.getAdminEmail()).isPresent()) {
            throw new BaseException(BaseResponseCode.ALREADY_EXIST_USER); // 이메일 중복 예외 처리
        }
        if (!adminSignupRequestDTO.getPassword().equals(adminSignupRequestDTO.getPasswordConfirm())) {
            throw new BaseException(BaseResponseCode.NOT_EQUAL_PASSWORD); // 비밀번호 불일치 예외 처리
        }

        Admin admin = new Admin();
        admin.setAdminEmail(adminSignupRequestDTO.getAdminEmail());
        admin.setPassword(passwordEncoder.encode(adminSignupRequestDTO.getPassword()));
        admin.setAdminName(adminSignupRequestDTO.getAdminName());
        return adminRepository.save(admin);
    }

    // 로그인 메서드 AdminResponseDTO 변환
    public AdminLoginResponseDTO loginAdmin(AdminLoginRequestDTO adminLoginRequestDTO) {
        Admin admin = adminRepository.findByAdminEmail(adminLoginRequestDTO.getAdminEmail())
                .orElseThrow(() -> new BaseException(BaseResponseCode.NOT_FOUND_USER));

        if (!passwordEncoder.matches(adminLoginRequestDTO.getPassword(), admin.getPassword())) {
            throw new BaseException(BaseResponseCode.WRONG_PASSWORD);
        }

        // 필요한 정보만 포함하는 DTO로 변환
        return new AdminLoginResponseDTO(admin.getAdminId(), admin.getAdminEmail(), admin.getAdminName());
    }
}