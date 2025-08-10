# Python Streaming API Server

FastAPI를 사용한 스트리밍 텍스트 API 서버입니다.

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
python main.py
```

또는 uvicorn으로 직접 실행:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API 엔드포인트

### 1. 서버 상태 확인
- **URL**: `GET /`
- **응답**: 서버 실행 상태 확인

### 2. 텍스트 스트리밍
- **URL**: `GET /api/sample`
- **설명**: 샘플 텍스트를 1초 간격으로 스트리밍
- **응답 형식**: Server-Sent Events (SSE)
- **데이터 형식**: JSON

### 3. 숫자 스트리밍 (테스트용)
- **URL**: `GET /api/numbers`
- **설명**: 1부터 10까지 숫자를 0.5초 간격으로 스트리밍
- **응답 형식**: Server-Sent Events (SSE)

## 테스트 방법

### 브라우저에서 직접 테스트
```
http://localhost:8000/api/sample
```

### curl로 테스트
```bash
curl -N http://localhost:8000/api/sample
```

### JavaScript로 테스트
```javascript
const eventSource = new EventSource('http://localhost:8000/api/sample');
eventSource.onmessage = function(event) {
    console.log(JSON.parse(event.data));
};
```

## 데이터 형식

각 스트리밍 메시지는 다음과 같은 JSON 형식으로 전송됩니다:

```json
{
    "id": 1,
    "message": "안녕하세요! 스트리밍 API 서버입니다.",
    "timestamp": "14:30:25"
}
```

## CORS 설정

현재 CORS가 설정되어 있지 않으므로, 필요시 FastAPI의 CORS 미들웨어를 추가해야 합니다.
