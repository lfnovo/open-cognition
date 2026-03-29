from fastapi import APIRouter, Query

from open_cognition.models.flashcard import (
    FlashcardCreate,
    FlashcardResponse,
    FlashcardUpdate,
)
from open_cognition.models.review import ReviewRequest, ReviewResponse, StrugglingCardResponse
from open_cognition.services import flashcard_service, review_service

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.get("/struggling", response_model=list[StrugglingCardResponse])
async def get_struggling_cards(
    topic_id: str | None = Query(None), limit: int = Query(10),
):
    return await review_service.get_struggling_cards(topic_id, limit)


@router.get("/due", response_model=list[FlashcardResponse])
async def get_due_flashcards(topic_id: str | None = Query(None)):
    return await flashcard_service.get_due_flashcards(topic_id)


@router.get("", response_model=list[FlashcardResponse])
async def list_flashcards(topic_id: str | None = Query(None)):
    return await flashcard_service.get_flashcards(topic_id)


@router.post("", response_model=FlashcardResponse, status_code=201)
async def create_flashcard(data: FlashcardCreate):
    return await flashcard_service.create_flashcard(data)


@router.get("/{flashcard_id}", response_model=FlashcardResponse)
async def get_flashcard(flashcard_id: str):
    record = await flashcard_service.get_flashcards()
    for r in record:
        if r.id == flashcard_id:
            return r


@router.patch("/{flashcard_id}", response_model=FlashcardResponse)
async def update_flashcard(flashcard_id: str, data: FlashcardUpdate):
    return await flashcard_service.update_flashcard(flashcard_id, data)


@router.post("/{flashcard_id}/review", response_model=ReviewResponse)
async def review_flashcard(flashcard_id: str, data: ReviewRequest):
    return await review_service.review_flashcard(flashcard_id, data)
