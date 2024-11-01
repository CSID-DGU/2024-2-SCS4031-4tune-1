package com.fortune.eyesee.entity;


import lombok.Data;

import jakarta.persistence.*;

@Entity
@Table(name = "User")
@Data
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer userId;

    @Column(name = "sessionID", nullable = false)
    private int sessionID; // 세션 ID (int 타입)

    @Column(nullable = false)
    private String userNum;

    private String department;
    private String userName;
    private Integer seatNum; // 좌석 번호



}