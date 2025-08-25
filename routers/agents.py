from fastapi import APIRouter
from models import AgentCreate, AgentSave

router = APIRouter()

@router.get("/agents")
def get_agents():
    return {
        "code": 0,
        "message": "success",
        "data": [
            {
                "id": "nLR8rOqcdTfn9UmSswBQS",
                "name": "教你如何从0到1,开发上线一个对接了openAI的机器人.pdf",
                "last_trained_at": 1755677533944,
                "visibility": "private",
            },
            {
                "id": "nLR8rOqcdTfn9UmSswBQS23",
                "name": "客服名称2",
                "last_trained_at": 1755677540229,
                "visibility": "private",
            }
        ],
    }

@router.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": agent_id,
            "name": "教你如何从0到1,开发上线一个对接了OpenAI的机器人.pdf",
            "description": "这是一个示例机器人，用于展示如何使用OpenAI API。",
            "created_at": 1755677533944,
            "updated_at": 1755677540229,
            "visibility": "private",
            "model": "gpt-3.5-turbo",
            "embedding_model": "text-embedding-3-small",
            "instructions": "请根据用户输入提供相关信息和帮助。",
            "status": "trained",
            "temperature": 0,
            "max_tokens": 1000,
        },
    }

@router.post("/agents/create")
def create_agent(agent: AgentCreate):
    return {
        "code": 0,
        "message": "Agent created successfully",
        "data": {
            "id": "new_agent_id",
            "name": agent.name,
            "created_at": 1755677540229,
            "visibility": agent.visibility,
        },
    }

@router.post("/agents/save")
def save_agent(agent: AgentSave):
    return {
        "code": 0,
        "message": "Agent saved successfully",
        "data": {
            "id": agent.id or "existing_agent_id",
            "name": agent.name or "Updated Agent",
            "updated_at": 1755677540229,
            "visibility": agent.visibility,
            "temperature": agent.temperature,
            "max_tokens": agent.max_tokens,
            "instructions": agent.instructions,
            "model": agent.model,
        },
    }