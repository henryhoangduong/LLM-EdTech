import logging
import os

import torch
from celery import Celery
from celery.signals import worker_init, worker_shutdown, worker_shutting_down
from dotenv import load_dotenv

from core.config import settings

logger = logging.getLogger(__name__)
load_dotenv()

UPSTASH_REDIS_HOST = os.getenv("UPSTASH_REDIS_HOST")
UPSTASH_REDIS_PORT = os.getenv("UPSTASH_REDIS_PORT")
UPSTASH_REDIS_PASSWORD = os.getenv("UPSTASH_REDIS_PASSWORD")

connection_link = f"rediss://:{UPSTASH_REDIS_PASSWORD}@{UPSTASH_REDIS_HOST}:{UPSTASH_REDIS_PORT}?ssl_cert_reqs=required"


def get_celery_config():
    return {
        "broken_url": connection_link,
        "result_backend": connection_link,
        "task_serializer": "json",
        "accept_content": ["json"],
        "result_serializer": "json",
        "enable_utc": True,
        "worker_send_task_events": True,
        "task_send_sent_event": True,
        "worker_redirect_stdouts": False,
        "worker_cancel_long_running_tasks_on_connection_loss": True,
        "worker_max_tasks_per_child": 1,
        "broker_connection_max_retries": 0,
        "worker_pool": "solo",
        "worker_max_memory_per_child": 1000000,
        "task_time_limit": 3600,
        "task_soft_time_limit": 3000,
        "worker_shutdown_timeout": 10,
        "imports": [
            "tasks.parsing_tasks",
        ],
        "task_routes": {
            "parse_markitdown": {"queue": "parsing"},
            "parse_docling": {"queue": "parsing"},
        },
    }


def create_celery_app():
    app = Celery("tasks")
    app.conf.update(get_celery_config())

    @worker_init.connect
    def init_worker(**kwargs):
        logger.info("🚀 Initializing Celery worker...")

    @worker_shutting_down.connect
    def worker_shutting_down_handler(**kwargs):
        if torch.cuda.is_available():
            try:
                torch.cuda.empty_cache()
                logger.info("Successfully cleared CUDA cache")
            except Exception as e:
                logger.error(f"Error clearing CUDA cache: {e}")

    @worker_shutdown.connect
    def worker_shutdown_handler(**kwargs):
        logger.info("Celery worker shutdown complete")

    return app


celery_app = create_celery_app()
