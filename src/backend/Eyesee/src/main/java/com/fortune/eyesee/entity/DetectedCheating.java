package com.fortune.eyesee.entity;

import lombok.Data;

import jakarta.persistence.*;

import java.time.LocalTime;

@Entity
@Table(name = "DetectedCheating")
@Data
public class DetectedCheating {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer detectedCheatingId;

    private Integer userId;                  // 사용자 ID
    private Integer sessionId;               // 세션 ID
    private Integer cheatingTypeId;          // 부정행위 종류 ID
    private String videoId;
    private LocalTime detectedTime;         // 탐지된 시간
}