from fastapi import APIRouter



router = APIRouter(prefix="/priority", tags=["priority"])

@router.get("")
async def get_priority_options():
    return [
        {"value": "low", "label": "Низкий"},
        {"value": "medium", "label": "Средний"},
        {"value": "high", "label": "Высокий"},
    ]