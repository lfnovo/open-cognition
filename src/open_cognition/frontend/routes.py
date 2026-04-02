import json

from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from open_cognition.config import get_templates_dir
from open_cognition.models.doubt import DoubtCreate
from open_cognition.models.topic import TopicCreate, TopicUpdate
from open_cognition.services import (
    artifact_service,
    doubt_service,
    flashcard_service,
    resource_service,
    review_service,
    topic_service,
)

router = APIRouter(tags=["frontend"])

_env = Environment(
    loader=FileSystemLoader(get_templates_dir()),
    autoescape=True,
    cache_size=0,
)
templates = Jinja2Templates(env=_env)


def _render(request: Request, name: str, context: dict):
    """Render template with kwargs for Starlette compatibility."""
    return templates.TemplateResponse(request=request, name=name, context=context)


# --- Dashboard ---


@router.get("/")
async def dashboard(request: Request):
    all_topics = await topic_service.get_all_topics()
    due_cards = await flashcard_service.get_due_flashcards()

    topics_with_due = []
    for topic in all_topics:
        topic_due = await flashcard_service.get_due_flashcards(topic.id)
        if topic_due:
            topics_with_due.append({"topic": topic, "due_count": len(topic_due)})

    struggling = await review_service.get_struggling_cards(limit=20)

    return _render(request, "dashboard.html", {
        "due_count": len(due_cards),
        "struggling_count": len(struggling),
        "topics_with_due": topics_with_due,
        "all_topics": all_topics,
    })


# --- Topics ---


@router.get("/topics")
async def topics_list(request: Request):
    topics = await topic_service.get_all_topics()
    return _render(request, "topics.html", {"topics": topics})


@router.post("/topics/create")
async def create_topic(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    parent_id: str = Form(""),
):
    data = TopicCreate(name=name, description=description or None)
    topic = await topic_service.create_topic(data)

    if parent_id:
        await topic_service.add_subtopic(parent_id, topic.id)

    if request.headers.get("HX-Request"):
        topics = await topic_service.get_all_topics()
        return _render(request, "partials/topics_list.html", {"topics": topics})

    return RedirectResponse("/topics", status_code=303)


@router.get("/topics/{topic_id}")
async def topic_detail(request: Request, topic_id: str):
    topic = await topic_service.get_topic(topic_id)
    flashcards = await flashcard_service.get_flashcards(topic_id)
    due_cards = await flashcard_service.get_due_flashcards(topic_id)
    resources = await resource_service.get_resources(topic_id)
    artifacts = await artifact_service.get_artifacts(topic_id)

    return _render(request, "topic_detail.html", {
        "topic": topic,
        "flashcards": flashcards,
        "due_cards": due_cards,
        "resources": resources,
        "artifacts": artifacts,
    })


@router.get("/topics/{topic_id}/edit")
async def topic_edit_form(request: Request, topic_id: str):
    topic = await topic_service.get_topic(topic_id)
    return _render(request, "topic_edit.html", {"topic": topic})


@router.post("/topics/{topic_id}/edit")
async def topic_edit_submit(
    topic_id: str,
    name: str = Form(...),
    description: str = Form(""),
):
    data = TopicUpdate(name=name, description=description or None)
    await topic_service.update_topic(topic_id, data)
    return RedirectResponse(f"/topics/{topic_id}", status_code=303)


@router.post("/topics/{topic_id}/delete")
async def topic_delete(topic_id: str):
    await topic_service.delete_topic(topic_id)
    return RedirectResponse("/topics", status_code=303)


# --- Resources ---


@router.get("/resources")
async def resources_list(
    request: Request, topic_id: str | None = Query(None)
):
    all_topics = await topic_service.get_all_topics()
    resources = await resource_service.get_resources(topic_id)
    return _render(request, "resources.html", {
        "resources": resources,
        "all_topics": all_topics,
        "selected_topic": topic_id or "",
    })


# --- Artifacts ---


@router.get("/artifacts")
async def artifacts_list(
    request: Request, topic_id: str | None = Query(None)
):
    all_topics = await topic_service.get_all_topics()
    artifacts = await artifact_service.get_artifacts_with_topics(topic_id)
    return _render(request, "artifacts.html", {
        "artifacts": artifacts,
        "all_topics": all_topics,
        "selected_topic": topic_id or "",
    })


# --- Doubts ---


@router.get("/doubts")
async def doubts_list(
    request: Request,
    topic_id: str | None = Query(None),
    status: str | None = Query(None),
):
    all_topics = await topic_service.get_all_topics()
    doubts = await doubt_service.get_doubts(topic_id, status)
    return _render(request, "doubts.html", {
        "doubts": doubts,
        "all_topics": all_topics,
        "selected_topic": topic_id or "",
        "selected_status": status or "",
    })


@router.get("/doubts/new")
async def doubt_new_form(request: Request):
    all_topics = await topic_service.get_all_topics()
    return _render(request, "doubt_new.html", {"all_topics": all_topics})


@router.post("/doubts/create")
async def doubt_create_submit(
    content: str = Form(...),
    topic_id: str = Form(""),
):
    data = DoubtCreate(content=content, topic_id=topic_id or None)
    await doubt_service.create_doubt(data)
    return RedirectResponse("/doubts", status_code=303)


@router.post("/doubts/{doubt_id}/resolve")
async def doubt_resolve(doubt_id: str):
    await doubt_service.resolve_doubt(doubt_id)
    return RedirectResponse("/doubts", status_code=303)


# --- Struggling ---


@router.get("/struggling")
async def struggling_cards(request: Request):
    cards = await review_service.get_struggling_cards(limit=20)
    return _render(request, "struggling.html", {"cards": cards})


# --- Review ---


@router.get("/review")
async def review_all(request: Request):
    cards = await flashcard_service.get_due_flashcards()
    return await _render_review(request, cards, topic=None)


@router.get("/review/{topic_id}")
async def review_topic(request: Request, topic_id: str):
    topic = await topic_service.get_topic(topic_id)
    cards = await flashcard_service.get_due_flashcards(topic_id)
    return await _render_review(request, cards, topic=topic)


def _serialize_card(card) -> dict:
    d = card.model_dump()
    d["due_date"] = d["due_date"].isoformat() if d.get("due_date") else None
    d["created"] = d["created"].isoformat() if d.get("created") else None
    d["updated"] = d["updated"].isoformat() if d.get("updated") else None
    return d


async def _render_review(request: Request, cards, topic):
    from surreal_basics import repo_query

    cards_data = []
    topic_artifacts_cache: dict[str, list] = {}

    for card in cards:
        cd = _serialize_card(card)
        res = await resource_service.get_resources_for_flashcard(card.id)
        cd["resources"] = [r.model_dump() for r in res]

        card_topic_ids = []
        if topic:
            card_topic_ids = [topic.id]
        else:
            edges = await repo_query(
                "SELECT ->belongs_to->topic AS tids FROM type::thing('flashcard', $fid)",
                {"fid": card.id},
            )
            if edges and edges[0].get("tids"):
                for tid in edges[0]["tids"]:
                    tid_clean = str(tid).split(":", 1)[1] if ":" in str(tid) else str(tid)
                    card_topic_ids.append(tid_clean)

        cd["topic_ids"] = card_topic_ids

        card_artifacts = []
        seen_art_ids = set()
        for tid in card_topic_ids:
            if tid not in topic_artifacts_cache:
                arts = await artifact_service.get_artifacts(tid)
                topic_artifacts_cache[tid] = [a.model_dump() for a in arts]
            for a in topic_artifacts_cache[tid]:
                if a["id"] not in seen_art_ids:
                    seen_art_ids.add(a["id"])
                    card_artifacts.append(a)
        cd["artifacts"] = card_artifacts

        cards_data.append(cd)

    return _render(request, "review.html", {
        "topic": topic,
        "cards": cards,
        "cards_json": json.dumps(cards_data, default=str).replace("</", "<\\/"),
        "total": len(cards),
        "current": 0,
    })
