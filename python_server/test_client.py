#!/usr/bin/env python3
"""
파이썬 스트리밍 API 서버 테스트 클라이언트
"""

import requests
import json
import time

def test_streaming_api():
    """스트리밍 API를 테스트하는 함수"""
    
    print("=== Python Streaming API 테스트 ===")
    print("서버: http://localhost:8000")
    print()
    
    # 1. 서버 상태 확인
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✅ 서버 상태: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return
    except Exception as e:
        print(f"❌ 오류: {e}")
        return
    
    print()
    print("=== /api/sample 스트리밍 테스트 ===")
    
    # 2. 스트리밍 API 테스트
    try:
        response = requests.get("http://localhost:8000/api/sample", stream=True)
        
        if response.status_code == 200:
            print("스트리밍 시작...")
            print("-" * 50)
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        # JSON 데이터 추출
                        json_str = line_str[6:]  # 'data: ' 제거
                        try:
                            data = json.loads(json_str)
                            print(f"[{data['timestamp']}] ID {data['id']}: {data['message']}")
                        except json.JSONDecodeError:
                            print(f"JSON 파싱 오류: {json_str}")
                    else:
                        print(f"Raw line: {line_str}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 스트리밍 테스트 오류: {e}")

def test_numbers_api():
    """숫자 스트리밍 API를 테스트하는 함수"""
    
    print()
    print("=== /api/numbers 스트리밍 테스트 ===")
    
    try:
        response = requests.get("http://localhost:8000/api/numbers", stream=True)
        
        if response.status_code == 200:
            print("숫자 스트리밍 시작...")
            print("-" * 30)
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        json_str = line_str[6:]
                        try:
                            data = json.loads(json_str)
                            print(f"[{data['timestamp']}] 숫자: {data['number']}")
                        except json.JSONDecodeError:
                            print(f"JSON 파싱 오류: {json_str}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 숫자 스트리밍 테스트 오류: {e}")

def test_markdown_api():
    """마크다운 스트리밍 API를 테스트하는 함수"""
    
    print()
    print("=== /api/markdown 스트리밍 테스트 ===")
    
    try:
        response = requests.get("http://localhost:8000/api/markdown", stream=True)
        
        if response.status_code == 200:
            print("마크다운 스트리밍 시작...")
            print("-" * 40)
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        json_str = line_str[6:]
                        try:
                            data = json.loads(json_str)
                            print(f"[{data['timestamp']}] ID {data['id']}: {data['chunk']}")
                        except json.JSONDecodeError:
                            print(f"JSON 파싱 오류: {json_str}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 마크다운 스트리밍 테스트 오류: {e}")

if __name__ == "__main__":
    test_streaming_api()
    test_numbers_api()
    test_markdown_api()
    print()
    print("테스트 완료!")
