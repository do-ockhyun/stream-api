package com.example.demo.app;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class ApiController {

    private final MessageService messageService;

    @GetMapping(value = "/api/messages", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> getMessages() {
        return messageService.getStreamingMessages()
                .map(message -> {
                    // SSE 형식으로 변환
                    return String.format("data: {\"id\":%d,\"message\":\"%s\",\"timestamp\":\"%s\"}\n\n",
                            message.getId(), message.getMessage(), message.getTimestamp());
                });
    }
}
