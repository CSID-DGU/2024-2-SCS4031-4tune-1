package com.fortune.eyesee.entity;

import lombok.Data;

import jakarta.persistence.*;

@Entity
@Table(name = "Session")
@Data
public class Session {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer sessionId; // 자동 증가

    private Integer examId;
    private String sessionReport;
}