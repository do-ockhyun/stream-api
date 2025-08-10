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
        return getStreamingMessages("/api/sample");
    }

    /**
     * Python API에서 스트리밍 데이터를 받아와서 MessageDTO로 변환 (엔드포인트 지정)
     */
    public Flux<MessageDTO> getStreamingMessages(String endpoint) {
        log.info("Python 서버 엔드포인트 호출: {}", endpoint);
        
        return webClient.get()
                .uri(endpoint)
                .retrieve()
                .bodyToFlux(String.class)
                .filter(line -> line != null && !line.trim().isEmpty())
                .map(this::parseMessage)
                .doOnError(error -> log.error("스트리밍 에러: ", error))
                .doOnComplete(() -> log.info("MessageService 스트리밍 완료 - 엔드포인트: {}", endpoint));
    }

    /**
     * JSON 문자열을 MessageDTO로 파싱
     */
    private MessageDTO parseMessage(String jsonLine) {
        try {
            log.warn("jsonLine: {}", jsonLine); 

            // WebClient가 이미 "data: " 접두사를 제거했으므로 직접 JSON 파싱
            JsonNode jsonNode = objectMapper.readTree(jsonLine);
            
            MessageDTO message = new MessageDTO();
            
            // numbers 엔드포인트의 경우 "number" 필드를 사용
            if (jsonNode.has("number")) {
                message.setId(jsonNode.get("number").asInt());
                message.setMessage("숫자: " + jsonNode.get("number").asText());
            } else {
                // sample 엔드포인트의 경우 기존 필드 사용
                message.setId(jsonNode.get("id").asInt());
                message.setMessage(jsonNode.get("message").asText());
            }
            
            message.setTimestamp(jsonNode.get("timestamp").asText());
            
            return message;
        } catch (Exception e) {
            log.error("메시지 파싱 에러: {}", jsonLine, e);
            // 에러 발생시 기본 메시지 반환
            MessageDTO errorMessage = new MessageDTO();
            errorMessage.setId(-1);
            errorMessage.setMessage("파싱 에러: " + jsonLine);
            errorMessage.setTimestamp("에러");
            return errorMessage;
        }
    }
}
