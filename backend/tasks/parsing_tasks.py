import logging

import torch
from core.celery_config import celery_app as celery

# from core.factories.database_factory import get_database

logger = logging.getLogger(__name__)


@celery.task(name="parse_docling")
def parse_docling_task(document_id: str):
    logger.info(f"Starting Docling parsing to document ID: {document_id}")
    try:
        pass
    except Exception as e:
        logger.error(f"Parse failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}
    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
