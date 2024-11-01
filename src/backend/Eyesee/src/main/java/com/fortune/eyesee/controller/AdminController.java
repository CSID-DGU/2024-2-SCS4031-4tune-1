package com.fortune.eyesee.controller;

import com.fortune.eyesee.common.response.BaseResponse;
import com.fortune.eyesee.dto.AdminLoginRequestDTO;
import com.fortune.eyesee.dto.AdminLoginResponseDTO;
import com.fortune.eyesee.dto.AdminSignupRequestDTO;
import com.fortune.eyesee.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpSession;

@RestController
@RequestMapping("/api/admin")
public class AdminController {
    @Autowired
    private AdminService adminService;

    // 회원가입 API
    @PostMapping("/signup")
    public ResponseEntity<BaseResponse<String>> registerAdmin(@RequestBody AdminSignupRequestDTO adminSignupRequestDTO) {
        adminService.registerAdmin(adminSignupRequestDTO);
        return ResponseEntity.ok(BaseResponse.success("회원가입 성공"));
    }

    // 로그인 성공 시, AdminResponseDTO 정보와 함께 메시지를 포함하여 응답
    @PostMapping("/login")
    public ResponseEntity<BaseResponse<AdminLoginResponseDTO>> loginAdmin(@RequestBody AdminLoginRequestDTO adminLoginRequestDTO, HttpSession session) {
        AdminLoginResponseDTO adminResponse = adminService.loginAdmin(adminLoginRequestDTO);
        session.setAttribute("admin", adminResponse); // 세션에 필요한 정보 저장

        // AdminResponseDTO와 "로그인 성공" 메시지를 포함하여 응답
        return ResponseEntity.ok(new BaseResponse<>(adminResponse, "로그인 성공"));
    }

    // 로그아웃 API
    @PostMapping("/logout")
    public ResponseEntity<BaseResponse<String>> logoutAdmin(HttpSession session) {
        session.invalidate(); // 세션 무효화
        return ResponseEntity.ok(BaseResponse.success("로그아웃 성공"));
    }
}