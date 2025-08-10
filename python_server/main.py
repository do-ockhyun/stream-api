from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import time
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
