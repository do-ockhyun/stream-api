package com.example.demo.app;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class ApiController {

    private final MessageService messageService;

    @GetMapping(value = "/api/messages", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> getMessages(@RequestParam(required = false) String type) {
        log.info("messages 요청 수신 - type: {}", type);
        
        // 파라미터가 없는 경우 에러 메시지 반환
        if (type == null || type.trim().isEmpty()) {
            log.warn("type 파라미터가 없습니다.");
            return Flux.just("{\"error\":\"type 파라미터가 필요합니다. 'sample' 또는 'numbers'를 입력하세요.\"}")
                    .doOnNext(message -> log.info("에러 메시지 전송: {}", message));
        }
        
        // type 파라미터에 따라 다른 엔드포인트 호출
        String endpoint;
        switch (type.toLowerCase()) {
            case "sample":
                endpoint = "/api/sample";
                break;
            case "numbers":
                endpoint = "/api/numbers";
                break;
            default:
                log.warn("잘못된 type 파라미터: {}", type);
                return Flux.just("{\"error\":\"잘못된 type입니다. 'sample' 또는 'numbers'를 입력하세요.\"}")
                        .doOnNext(message -> log.info("에러 메시지 전송: {}", message));
        }
        
        log.info("Python 서버 엔드포인트 호출: {}", endpoint);
        
        return messageService.getStreamingMessages(endpoint)
                .doOnNext(message -> log.info("메시지 전송: {}", message))
                .map(message -> {
                    // JSON을 문자열로 변환하고 SSE 형식으로 변환
                    String jsonData = String.format("{\"id\":%d,\"message\":\"%s\",\"timestamp\":\"%s\"}",
                            message.getId(), message.getMessage(), message.getTimestamp());
                    return jsonData;
                })
                .doOnError(error -> log.error("스트리밍 에러: ", error))
                .doOnComplete(() -> log.info("스트리밍 완료"));
    }

    @GetMapping(value = "/api/md", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> getMarkdown() {
        log.info("마크다운 요청 수신");
        
        return messageService.getMarkdownStream()
                .doOnNext(message -> log.info("마크다운 청크 전송: {}", message))
                .map(message -> {
                    // JSON을 문자열로 변환하고 SSE 형식으로 변환
                    String jsonData = String.format("{\"id\":%d,\"chunk\":\"%s\",\"timestamp\":\"%s\"}",
                            message.getId(), message.getMessage(), message.getTimestamp());
                    return jsonData;
                })
                .doOnError(error -> log.error("마크다운 스트리밍 에러: ", error))
                .doOnComplete(() -> log.info("마크다운 스트리밍 완료"));
    }
}
