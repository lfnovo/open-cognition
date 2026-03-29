from fastapi import APIRouter, Query

from open_cognition.models.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from open_cognition.services import resource_service

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[ResourceResponse])
async def list_resources(topic_id: str | None = Query(None)):
    return await resource_service.get_resources(topic_id)


@router.post("", response_model=ResourceResponse, status_code=201)
async def create_resource(data: ResourceCreate):
    return await resource_service.create_resource(data)


@router.patch("/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: str, data: ResourceUpdate):
    return await resource_service.update_resource(resource_id, data)
