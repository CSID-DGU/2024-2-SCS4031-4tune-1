package com.fortune.eyesee.entity;

import lombok.Data;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.time.LocalTime;


@Entity
@Table(name = "Exam")
@Data
public class Exam {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer examId;

    private Integer adminId;                // 관리자 ID
    private String examName;                // 시험명
    private String examSemester;            // 학기
    private Integer examStudentNumber;      // 학생 수
    private String examLocation;            // 시험 장소
    private LocalDate examDate;             // 시험 날짜
    private LocalTime examStartTime;        // 시험 시작 시간
    private Integer examDuration;           // 진행 시간
    private Integer examQuestionNumber;     // 질문 수
    private Integer examTotalScore;         // 총점
    private String examStatus;              // 시험 상태
    private String examRandomCode;          // 랜덤 코드
    private String examNotice;              // 공지사항
}