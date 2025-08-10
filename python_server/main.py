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
        # README.md 파일 읽기
        try:
            with open('README.md', 'r', encoding='utf-8') as file:
                markdown_content = file.read()
        except FileNotFoundError:
            markdown_content = """# README.md 파일을 찾을 수 없습니다

README.md 파일이 현재 디렉토리에 있는지 확인해주세요.

## 파일 위치
- Python 서버 실행 디렉토리: `python_server/`
- README.md 파일 위치: `../README.md`

## 해결 방법
1. README.md 파일이 프로젝트 루트에 있는지 확인
2. Python 서버를 프로젝트 루트에서 실행하거나
3. 파일 경로를 수정해주세요."""
        except Exception as e:
            markdown_content = f"""# 파일 읽기 오류

README.md 파일을 읽는 중 오류가 발생했습니다.

## 오류 내용
```
{str(e)}
```

## 해결 방법
1. 파일 권한 확인
2. 파일 인코딩 확인 (UTF-8)
3. 파일 경로 확인"""
        
        # 마크다운 내용을 라인별로 분할
        lines = markdown_content.split('\n')
        
        # 스트리밍 전송
        for line in lines:
            # 라인만 전송
            yield f'data: {line}\n\n'
            # 1초 간격으로 전송
            await asyncio.sleep(1.0)
    
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
