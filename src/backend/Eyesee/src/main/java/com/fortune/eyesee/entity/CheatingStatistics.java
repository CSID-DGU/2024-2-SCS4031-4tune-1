package com.fortune.eyesee.entity;


import lombok.Data;

import jakarta.persistence.*;
@Entity
@Table(name = "CheatingStatistics")
@Data
public class CheatingStatistics {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer cheatingStatisticsId;

    private Integer userId;
    private Integer cheatingTypeId;     // 부정행위 종류 ID
    private Integer cheatingCount;      // 부정행위 횟수
}
