package com.fortune.eyesee.common.response;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

import java.util.Arrays;

@Getter
@AllArgsConstructor
public enum BaseResponseCode {

    // Success
    SUCCESS("S0001", HttpStatus.OK, "요청에 성공했습니다"),

    // Global Errors
    INTERNAL_SERVER_ERROR("GL000", HttpStatus.INTERNAL_SERVER_ERROR, "서버 내부 오류가 발생했습니다."),
    NO_PERMISSION("GL001", HttpStatus.FORBIDDEN, "권한이 없습니다."),
    NULL_REQUEST_PARAM("GL002", HttpStatus.BAD_REQUEST, "쿼리 파라미터가 없습니다."),
    BAD_REQUEST("GL003", HttpStatus.BAD_REQUEST, "잘못된 요청입니다."),
    CONTENT_NULL("GL004", HttpStatus.BAD_REQUEST, "내용을 입력해 주세요."),

    NOT_FOUND_TOKEN("GL005", HttpStatus.NOT_FOUND, "토큰이 존재하지 않습니다"),
    EXPIRED_TOKEN("GL006", HttpStatus.UNAUTHORIZED, "토큰의 기한이 지났습니다"),
    WRONG_TYPE_TOKEN("GL007", HttpStatus.UNAUTHORIZED, "잘못된 타입의 토큰입니다."),
    UNSUPPORTED_TOKEN("GL008", HttpStatus.UNAUTHORIZED, "지원하지 않는 토큰입니다."),
    TOKEN_ERROR("GL009", HttpStatus.UNAUTHORIZED, "토큰에 문제가 발생했습니다."),
    MALFORMED_TOKEN("GL010", HttpStatus.UNAUTHORIZED, "토큰의 구조가 잘못되었습니다."),

    UNAUTHORIZED("GL011", HttpStatus.UNAUTHORIZED, "로그인이 필요합니다."),
    INVALID_STATUS("GL012", HttpStatus.BAD_REQUEST, "유효하지 않은 상태 값입니다."),
    INVALID_INPUT("GL013", HttpStatus.BAD_REQUEST, "입력이 잘못되었습니다."),

    NOT_FOUND_DATA("GL014", HttpStatus.NOT_FOUND, "요청한 데이터를 찾을 수 없습니다."),

    EXPIRED_REFRESH_TOKEN("GL015", HttpStatus.UNAUTHORIZED, "리프레시 토큰이 만료되었습니다."),
    INVALID_REFRESH_TOKEN("GL016", HttpStatus.UNAUTHORIZED, "리프레시 토큰이 유효하지 않습니다."),

    // User Errors
    ALREADY_EXIST_USER("U0001", HttpStatus.CONFLICT, "이미 존재하는 사용자입니다"),
    WRONG_PASSWORD("U0002", HttpStatus.BAD_REQUEST, "비밀번호가 틀렸습니다."),
    NOT_FOUND_USER("U0003", HttpStatus.NOT_FOUND, "사용자를 찾을 수 없습니다."),
    NOT_EQUAL_PASSWORD("U0004", HttpStatus.BAD_REQUEST, "비밀번호가 일치하지 않습니다."),
    WEAK_PASSWORD("U0005", HttpStatus.BAD_REQUEST, "비밀번호는 8자 이상이어야 합니다."),
    INVALID_EMAIL_FORMAT("U0006", HttpStatus.BAD_REQUEST, "이메일 형식이 잘못되었습니다."),

    // Exam Errors
    NOT_FOUND_EXAM("E0001", HttpStatus.NOT_FOUND, "시험을 찾을 수 없습니다."),
    NOT_FOUND_EXAM_CODE("E0002", HttpStatus.NOT_FOUND, "시험 코드를 찾을 수 없습니다."),

    // Exam Errors
    EXAM_NOT_FOUND("E0001", HttpStatus.NOT_FOUND, "시험을 찾을 수 없습니다."),
    SESSION_NOT_FOUND("E0002", HttpStatus.NOT_FOUND, "세션을 찾을 수 없습니다."),
    EXAM_ALREADY_EXISTS("E0003", HttpStatus.CONFLICT, "이미 존재하는 시험입니다."),
    INVALID_EXAM_STATUS("E0004", HttpStatus.BAD_REQUEST, "유효하지 않은 시험 상태입니다."),
    EXAM_ACCESS_DENIED("E0005", HttpStatus.FORBIDDEN, "시험에 접근할 권한이 없습니다."),

    // Session Errors
    NOT_FOUND_SESSION("E0006", HttpStatus.NOT_FOUND, "세션을 찾을 수 없습니다."),

    // Cheating Errors
    NOT_FOUND_CHEATING_TYPE("C0001", HttpStatus.NOT_FOUND, "부정행위 타입을 찾을 수 없습니다."),


    // 기타 추가 오류 코드 ...

    ;

    private final String code;
    private final HttpStatus status;
    private final String message;

    // 코드로 BaseResponseCode 조회
    public static BaseResponseCode findByCode(String code) {
        return Arrays.stream(BaseResponseCode.values())
                .filter(b -> b.getCode().equals(code))
                .findAny()
                .orElseThrow(() -> new IllegalArgumentException("해당 코드에 대한 BaseResponseCode를 찾을 수 없습니다."));
    }
}