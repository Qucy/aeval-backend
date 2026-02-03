from fastapi import APIRouter, Depends, HTTPException

from app.models.recommendation import ChatRequest, ChatResponse
from app.services.chat_service import ChatService, get_chat_service


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Process user message and return AI response with recommendation.

    Args:
        request: Chat request with user message
        chat_service: Injected chat service singleton

    Returns:
        ChatResponse with AI content, recommendation, and quick replies

    Raises:
        HTTPException: If message processing fails
    """
    try:
        return await chat_service.process_message(request.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Data file error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
