CREATE TABLE `User` (
                        `UserID` INT NOT NULL AUTO_INCREMENT,
                        `SessionID` INT NOT NULL,
                        `UserName` VARCHAR(10) NULL,
                        `Department` VARCHAR(50) NULL,
                        `UserNum` INT NULL,
                        `SeatNum` INT NULL,
                        PRIMARY KEY (`UserID`)
);

CREATE TABLE `Exam` (
                        `ExamID` INT NOT NULL AUTO_INCREMENT,
                        `AdminID` INT NOT NULL,
                        `ExamName` VARCHAR(100) NULL,
                        `ExamSemester` VARCHAR(100) NULL,
                        `ExamStudentNumber` INT NULL,
                        `ExamLocation` VARCHAR(100) NULL,
                        `ExamDate` DATE NULL,
                        `ExamStartTime` TIME NULL,
                        `ExamDuration` INT NULL,
                        `ExamQuestionNumber` INT NULL,
                        `ExamTotalScore` INT NULL,
                        `ExamStatus` VARCHAR(100) NULL,
                        `ExamRandomCode` VARCHAR(10) NULL,
                        `ExamNotice` VARCHAR(255) NULL,
                        PRIMARY KEY (`ExamID`)
);

CREATE TABLE `Session` (
                           `SessionID` INT NOT NULL AUTO_INCREMENT,
                           `ExamID` INT NOT NULL,
                           `SessionReport` VARCHAR NULL,
                           PRIMARY KEY (`SessionID`)
);

CREATE TABLE `ObjectDetectionData` (
                                       `ObjectionDetectionID` INT NOT NULL AUTO_INCREMENT,
                                       `DetectedCheatingID` INT NOT NULL,
                                       `TimeStamp` DATETIME NULL,
                                       `ObjectDetected` BOOLEAN NULL,
                                       `ObjectType` VARCHAR(50) NULL,
                                       PRIMARY KEY (`ObjectionDetectionID`)
);

CREATE TABLE `DetectedCheating` (
                                    `DetectedCheatingID` INT NOT NULL AUTO_INCREMENT,
                                    `UserID` INT NOT NULL,
                                    `SessionID` INT NOT NULL,
                                    `CheatingTypeID` INT NOT NULL,
                                    `DetectedTime` DATETIME NULL,
                                    PRIMARY KEY (`DetectedCheatingID`)
);

CREATE TABLE `VideoRecording` (
                                  `VideoID` INT NOT NULL AUTO_INCREMENT,
                                  `SessionID` INT NOT NULL,
                                  `UserID` INT NOT NULL,
                                  `StartTime` DATETIME NULL,
                                  `EndTime` DATETIME NULL,
                                  `FilePath` VARCHAR(255) NULL,
                                  PRIMARY KEY (`VideoID`)
);

CREATE TABLE `CheatingStatistics` (
                                      `CheatingStatisticsID` INT NOT NULL AUTO_INCREMENT,
                                      `UserID` INT NOT NULL,
                                      `CheatingTypeID` INT NOT NULL,
                                      `CheatingCount` INT NULL,
                                      PRIMARY KEY (`CheatingStatisticsID`)
);

CREATE TABLE `Admin` (
                         `AdminID` INT NOT NULL AUTO_INCREMENT,
                         `AdminEmail` VARCHAR(255) NOT NULL,
                         `Password` VARCHAR(255) NULL,
                         `AdminName` VARCHAR(100) NULL,
                         PRIMARY KEY (`AdminID`, `AdminEmail`)
);

CREATE TABLE `CheatingType` (
                                `CheatingTypeID` INT NOT NULL AUTO_INCREMENT,
                                `CheatingTypeName` VARCHAR(20) NULL,
                                PRIMARY KEY (`CheatingTypeID`)
);
