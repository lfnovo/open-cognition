from fastapi import APIRouter, Query

from open_cognition.models.doubt import DoubtCreate, DoubtResponse, DoubtUpdate
from open_cognition.services import doubt_service

router = APIRouter(prefix="/doubts", tags=["doubts"])


@router.get("", response_model=list[DoubtResponse])
async def list_doubts(
    topic_id: str | None = Query(None),
    status: str | None = Query(None),
):
    return await doubt_service.get_doubts(topic_id, status)


@router.post("", response_model=DoubtResponse, status_code=201)
async def create_doubt(data: DoubtCreate):
    return await doubt_service.create_doubt(data)


@router.patch("/{doubt_id}", response_model=DoubtResponse)
async def update_doubt(doubt_id: str, data: DoubtUpdate):
    return await doubt_service.update_doubt(doubt_id, data)
