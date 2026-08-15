import os
import uuid
import logging
from typing import Set

logger = logging.getLogger(__name__)

processing_users: Set[int] = set()


def get_temp_filename(extension: str = ".png") -> str:
    return f"temp_{uuid.uuid4().hex}{extension}"


def cleanup_files(*file_paths: str):
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {path}: {e}")


def acquire_user_lock(user_id: int) -> bool:
    if user_id in processing_users:
        return False
    processing_users.add(user_id)
    return True


def release_user_lock(user_id: int):
    processing_users.discard(user_id)
