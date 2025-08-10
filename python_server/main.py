from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import time
import random
import json
from typing import AsyncGenerator

app = FastAPI(title="Streaming API Server", description="텍스트 스트리밍을 위한 파이썬 API 서버")

@app.get("/")
async def root():
    return {"message": "Streaming API Server is running!"}

@app.get("/api/sample")
async def stream_sample() -> StreamingResponse:
    """
    샘플 텍스트를 스트리밍으로 전송하는 엔드포인트
    """
    
    async def generate_text() -> AsyncGenerator[str, None]:
        sample_texts = [
            "안녕하세요! 스트리밍 API 서버입니다.",
            "이것은 실시간으로 전송되는 텍스트입니다.",
            "Spring Boot WebFlux에서 이 데이터를 받아서",
            "다시 클라이언트로 스트리밍할 예정입니다.",
            "각 문장은 1초 간격으로 전송됩니다.",
            "이제 마지막 메시지입니다.",
            "스트리밍이 완료되었습니다!"
        ]
        
        for i, text in enumerate(sample_texts):
            # 각 텍스트를 JSON 형태로 전송
            yield f'data: {{"id": {i+1}, "message": "{text}", "timestamp": "{time.strftime("%H:%M:%S")}"}}\n\n'
            await asyncio.sleep(1)  # 1초 대기
    
    return StreamingResponse(
        generate_text(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

@app.get("/api/numbers")
async def stream_numbers() -> StreamingResponse:
    """
    숫자를 스트리밍으로 전송하는 엔드포인트 (테스트용)
    """
    
    async def generate_numbers() -> AsyncGenerator[str, None]:
        for i in range(1, 11):
            yield f'data: {{"number": {i}, "timestamp": "{time.strftime("%H:%M:%S")}"}}\n\n'
            await asyncio.sleep(0.5)  # 0.5초 대기
    
    return StreamingResponse(
        generate_numbers(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

@app.get("/api/markdown")
async def stream_markdown() -> StreamingResponse:
    """
    마크다운 내용을 랜덤한 텍스트 단위로 스트리밍하는 엔드포인트
    """
    
    async def generate_markdown() -> AsyncGenerator[str, None]:
        # 샘플 마크다운 내용
        markdown_content = """# 마크다운 스트리밍 데모

이것은 **마크다운** 내용을 스트리밍으로 전송하는 데모입니다.

## 주요 기능

- 실시간 텍스트 스트리밍
- 랜덤한 텍스트 단위 분할
- 마크다운 형식 지원

### 코드 예시

```python
async def stream_markdown():
    content = "마크다운 내용"
    for chunk in content.split():
        yield chunk
```

## 장점

1. **실시간성**: 즉시 전송
2. **효율성**: 메모리 사용량 최적화
3. **확장성**: 다양한 형식 지원

> 인용문: 이것은 인용문입니다.

---

스트리밍이 완료되었습니다!"""
        
        # 마크다운 내용을 개행을 보존하면서 분할
        import re
        
        # 개행을 특별한 토큰으로 임시 대체
        NEWLINE_TOKEN = "___NEWLINE___"
        markdown_with_tokens = markdown_content.replace('\n', NEWLINE_TOKEN)
        
        # 마크다운 내용을 더 간단하게 분할
        chunks = []
        
        # 1. 개행 토큰을 기준으로 분할 (줄 단위)
        lines = markdown_with_tokens.split(NEWLINE_TOKEN)
        for line in lines:
            if line.strip():
                # 내용이 있는 줄은 문장 단위로 분할
                sentences = re.split(r'([.!?]+)', line)
                for i in range(0, len(sentences), 2):
                    if i + 1 < len(sentences):
                        chunks.append(sentences[i] + sentences[i + 1])
                    else:
                        chunks.append(sentences[i])
            else:
                # 빈 줄은 개행 토큰으로 추가
                chunks.append(NEWLINE_TOKEN)
        
        # 모든 청크를 하나의 리스트로 합치기
        all_chunks = chunks
        # random.shuffle(all_chunks)  # 순서 섞기 비활성화
        
        # 스트리밍 전송
        for i, chunk in enumerate(all_chunks):
            if chunk.strip() or chunk == NEWLINE_TOKEN:  # 빈 문자열과 개행 토큰 포함
                # 개행 토큰을 특별한 마커로 변환
                actual_chunk = chunk.replace(NEWLINE_TOKEN, '___NEWLINE___')
                
                # 문제가 될 수 있는 문자들을 안전하게 처리
                actual_chunk = actual_chunk.replace('"', '&quot;').replace('\\', '\\\\')
                
                # JSON 객체 생성
                json_data = {
                    "id": i + 1,
                    "chunk": actual_chunk,
                    "timestamp": time.strftime("%H:%M:%S")
                }
                
                print(f"전송 청크 {i+1}: '{actual_chunk}'")  # 디버깅용
                yield f'data: {json.dumps(json_data, ensure_ascii=False, separators=(",", ":"))}\n\n'
                # 랜덤한 간격으로 전송 (0.3~1.2초)
                await asyncio.sleep(random.uniform(0.3, 1.2))
    
    return StreamingResponse(
        generate_markdown(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
