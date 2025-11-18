from fastapi import APIRouter
from . import professionals, classes, webhooks

router = APIRouter()

router.include_router(professionals.router)
router.include_router(classes.router)
router.include_router(webhooks.router)