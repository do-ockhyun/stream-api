
# Streaming API Sample

## 개요
Springboot webflux 를 이용해 streaming 으로 데이터를 전달하는 것을 공부할거야

## 구성
A. 파이썬으로 `/api/sample` 를 구성하고
  - StreamingResponse 를 이용한 텍스트를 스트리밍으로 전송

B. Springboot 에서는 /api/messages 호출되면, 파이썬 API 를 호출해 텍스트를 수신한 데이터를 스트리밍으로 전달

C. 화면에서는 스트리밍으로 전달받아서 화면에 즉시 표시 하는 샘플 프로젝트를 만들려고 해

## 프로젝트 
1. 파이썬 API 서버
2. Springboot 서버
  - api 
  - 화면은 타임리프 로 만들고
  - js를 이용해서 화면에 표시

이렇게 하려고 해.

