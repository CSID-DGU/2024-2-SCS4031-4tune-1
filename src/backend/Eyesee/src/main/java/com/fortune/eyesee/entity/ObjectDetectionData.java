package com.fortune.eyesee.entity;


import lombok.Data;

import jakarta.persistence.*;

import java.time.LocalTime;

@Entity
@Table(name = "ObjectDetectionData")
@Data
public class ObjectDetectionData {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer objectionDetectionId;

    private Integer detectedCheatingId;         // 탐지된 부정행위 ID
    private LocalTime timeStamp;                // 타임스탬프
    private Boolean objectDetected;             // 객체 감지 여부
    private String objectType;                  // 객체 종류
}