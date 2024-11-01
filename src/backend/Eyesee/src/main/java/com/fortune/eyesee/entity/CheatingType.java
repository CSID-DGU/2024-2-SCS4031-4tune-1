package com.fortune.eyesee.entity;


import lombok.Data;

import jakarta.persistence.*;
@Entity
@Table(name = "CheatingType")
@Data
public class CheatingType {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer cheatingTypeId;

    private String cheatingTypeName; // 부정행위 종류 이름
}