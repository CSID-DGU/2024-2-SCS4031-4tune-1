package com.fortune.eyesee.common.exception;

import com.fortune.eyesee.common.response.BaseResponse;
import com.fortune.eyesee.common.response.BaseResponseCode;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Objects;

@RestControllerAdvice
public class ExceptionHandlerAdvice {

    // BaseException 처리
    @ExceptionHandler(BaseException.class)
    protected ResponseEntity<?> handleBaseException(BaseException e) {
        return ResponseEntity.status(e.getBaseResponseCode().getStatus())
                .body(BaseResponse.error(
                        e.getBaseResponseCode().getStatus().value(),
                        e.getBaseResponseCode().getCode(),
                        e.getBaseResponseCode().getMessage()
                ));
    }

    // 유효성 검사 실패 예외 처리 (MethodArgumentNotValidException)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    protected ResponseEntity<?> handleMethodArgumentNotValidException(MethodArgumentNotValidException e) {
        // 기본 메시지를 BaseResponseCode로 매핑
        Objects.requireNonNull(e.getFieldError());
        BaseResponseCode baseResponseCode = BaseResponseCode.findByCode(e.getFieldError().getDefaultMessage());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(BaseResponse.error(
                        baseResponseCode.getStatus().value(),
                        baseResponseCode.getCode(),
                        baseResponseCode.getMessage()
                ));
    }

    // 요청 파라미터 누락 예외 처리 (MissingServletRequestParameterException)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MissingServletRequestParameterException.class)
    protected ResponseEntity<?> handleMissingServletRequestParameterException(MissingServletRequestParameterException e) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(BaseResponse.error(
                        HttpStatus.BAD_REQUEST.value(),
                        BaseResponseCode.NULL_REQUEST_PARAM.getCode(),
                        BaseResponseCode.NULL_REQUEST_PARAM.getMessage()
                ));
    }

    // 그 외 예외 처리 (일반적인 예외)
    @ExceptionHandler(Exception.class)
    protected ResponseEntity<?> handleException(Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(BaseResponse.error(
                        HttpStatus.INTERNAL_SERVER_ERROR.value(),
                        BaseResponseCode.INTERNAL_SERVER_ERROR.getCode(),
                        BaseResponseCode.INTERNAL_SERVER_ERROR.getMessage()
                ));
    }
}