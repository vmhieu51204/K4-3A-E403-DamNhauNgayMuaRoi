"""
api.py — REST API Endpoint cho Frontend (FE)
Sử dụng FastAPI để bọc TACopilotAgent, giúp FE dễ dàng tích hợp qua HTTP.
Chạy server: uvicorn api:app --reload
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from env_loader import load_env
from agent import TACopilotAgent

# Khởi tạo biến môi trường và Agent
load_env()
agent = TACopilotAgent()

app = FastAPI(
    title="TA Copilot API",
    description="API cho Frontend tích hợp hệ thống TA Copilot K4",
    version="1.0.0"
)

# Models cho Payload
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[Message]] = []
    
class ToolTrace(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Any

class ChatResponse(BaseModel):
    status: str
    answer: str
    total_rounds: int
    traces: List[ToolTrace]

@app.get("/health")
def health_check():
    return {"status": "ok", "version": agent.version_info.full_version}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        # Chuyển đổi history sang format của backend
        history_dict = [{"role": m.role, "content": m.content} for m in request.history]
        
        # Chạy agent logic
        result = agent.run(user_query=request.query, history=history_dict)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
            
        # Trích xuất tool traces cho FE hiển thị (nếu cần)
        traces = []
        for r in result.get("rounds", []):
            if "tool_calls" in r:
                for tc in r["tool_calls"]:
                    # Lấy kết quả tương ứng từ round tiếp theo (role: tool)
                    tool_result = "Hidden"
                    traces.append(ToolTrace(
                        tool_name=tc["function"]["name"],
                        arguments=tc["function"]["arguments"],
                        result=tool_result
                    ))
                    
        return ChatResponse(
            status=result["status"],
            answer=result["final_text"],
            total_rounds=result["total_rounds"],
            traces=traces
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
