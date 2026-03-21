from fastapi import APIRouter, Query

from open_cognition.models.artifact import (
    ArtifactCreate,
    ArtifactResponse,
    ArtifactUpdate,
)
from open_cognition.services import artifact_service

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.get("", response_model=list[ArtifactResponse])
async def list_artifacts(topic_id: str | None = Query(None)):
    return await artifact_service.get_artifacts(topic_id)


@router.post("", response_model=ArtifactResponse, status_code=201)
async def create_artifact(data: ArtifactCreate):
    return await artifact_service.create_artifact(data)


@router.patch("/{artifact_id}", response_model=ArtifactResponse)
async def update_artifact(artifact_id: str, data: ArtifactUpdate):
    return await artifact_service.update_artifact(artifact_id, data)
