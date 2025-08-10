package com.example.demo.app;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class MessageService {

    private final WebClient webClient;
    private final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * Python API에서 스트리밍 데이터를 받아와서 MessageDTO로 변환
     */
    public Flux<MessageDTO> getStreamingMessages() {
        return webClient.get()
                .uri("/api/sample")
                .retrieve()
                .bodyToFlux(String.class)
                .filter(line -> line.startsWith("data: "))
                .map(this::parseMessage)
                .doOnNext(message -> log.info("수신된 메시지: {}", message))
                .doOnError(error -> log.error("스트리밍 에러: ", error));
    }

    /**
     * SSE 형식의 문자열을 MessageDTO로 파싱
     */
    private MessageDTO parseMessage(String sseLine) {
        try {
            // "data: " 제거하고 JSON 파싱
            String jsonStr = sseLine.substring(6);
            JsonNode jsonNode = objectMapper.readTree(jsonStr);
            
            MessageDTO message = new MessageDTO();
            message.setId(jsonNode.get("id").asInt());
            message.setMessage(jsonNode.get("message").asText());
            message.setTimestamp(jsonNode.get("timestamp").asText());
            
            return message;
        } catch (Exception e) {
            log.error("메시지 파싱 에러: {}", sseLine, e);
            // 에러 발생시 기본 메시지 반환
            MessageDTO errorMessage = new MessageDTO();
            errorMessage.setId(-1);
            errorMessage.setMessage("파싱 에러: " + sseLine);
            errorMessage.setTimestamp("에러");
            return errorMessage;
        }
    }
}
