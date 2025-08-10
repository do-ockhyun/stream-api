package com.example.demo.app;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
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
    public Flux<String> getMessages() {
        log.info("스트리밍 요청 수신");
        
        return messageService.getStreamingMessages()
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
}
