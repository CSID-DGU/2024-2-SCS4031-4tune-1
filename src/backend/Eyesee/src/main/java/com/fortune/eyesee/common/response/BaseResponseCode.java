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
    EXPIRED_TOKEN("GL006", HttpStatus.GATEWAY_TIMEOUT, "토큰의 기한이 지났습니다"),
    WRONG_TYPE_TOKEN("GL007", HttpStatus.BAD_REQUEST, "잘못된 타입의 토큰입니다."),
    UNSUPPORTED_TOKEN("GL008", HttpStatus.BAD_REQUEST, "지원하지 않는 토큰입니다."),
    TOKEN_ERROR("GL009", HttpStatus.BAD_REQUEST, "토큰에 문제가 발생했습니다."),
    MALFORMED_TOKEN("GL010", HttpStatus.BAD_REQUEST, "토큰의 구조가 잘못되었습니다."),
    INVALID_INPUT("GL011", HttpStatus.BAD_REQUEST, "입력이 잘못되었습니다."),

    // User Errors
    ALREADY_EXIST_USER("U0001", HttpStatus.CONFLICT, "이미 존재하는 사용자입니다"),
    WRONG_PASSWORD("U0002", HttpStatus.BAD_REQUEST, "비밀번호가 틀렸습니다."),
    NOT_FOUND_USER("U0003", HttpStatus.NOT_FOUND, "사용자를 찾을 수 없습니다."),
    NOT_EQUAL_PASSWORD("U0004", HttpStatus.BAD_REQUEST, "비밀번호가 일치하지 않습니다."),
    WEAK_PASSWORD("U0005", HttpStatus.BAD_REQUEST, "비밀번호는 8자 이상이어야 합니다."),
    INVALID_EMAIL_FORMAT("U0006", HttpStatus.BAD_REQUEST, "이메일 형식이 잘못되었습니다."),

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