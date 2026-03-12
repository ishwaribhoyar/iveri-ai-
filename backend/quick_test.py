"""Verify the think-tag stripping fix."""
import urllib.request
import json

# Test non-streaming (direct API)
try:
    data = json.dumps({
        "message": "What is Python programming language?",
        "conversation_id": "verify-fix-1",
        "model": "sarvam-m",
        "system_prompt": "You are Jarvis, an intelligent AI assistant.",
        "temperature": 0.7,
        "max_tokens": 256,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        "http://localhost:8000/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read().decode())
    content = d["content"]
    has_think = "<think>" in content
    print("NON-STREAMING TEST:")
    print(f"  Has <think> tags: {has_think}")
    print(f"  Response preview: {content[:200]}")
    print(f"  Status: {'FAIL' if has_think else 'PASS'}")
except Exception as e:
    print(f"NON-STREAMING TEST: ERROR - {e}")

# Test streaming (via proxy)
try:
    data2 = json.dumps({
        "message": "What is JavaScript?",
        "conversation_id": "verify-fix-2",
        "model": "sarvam-m",
        "system_prompt": "You are Jarvis.",
        "temperature": 0.7,
        "max_tokens": 256,
        "stream": True,
    }).encode()
    req2 = urllib.request.Request(
        "http://localhost:8000/api/chat",
        data=data2,
        headers={"Content-Type": "application/json"},
    )
    r2 = urllib.request.urlopen(req2, timeout=30)
    body = r2.read().decode()
    accumulated = ""
    for line in body.split("\n"):
        if line.startswith("data: "):
            try:
                chunk = json.loads(line[6:])
                if chunk.get("delta"):
                    accumulated += chunk["delta"]
            except:
                pass
    has_think = "<think>" in accumulated
    print(f"\nSTREAMING TEST:")
    print(f"  Has <think> tags: {has_think}")
    print(f"  Response preview: {accumulated[:200]}")
    print(f"  Status: {'FAIL' if has_think else 'PASS'}")
except Exception as e:
    print(f"\nSTREAMING TEST: ERROR - {e}")
