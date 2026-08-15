import asyncio
import logging
from PIL import Image
from rembg import remove, new_session
import requests

from config import REMOVEBG_API_KEY

logger = logging.getLogger(__name__)

rembg_session = new_session("u2netp")


class BackgroundRemoverService:

    @staticmethod
    async def process_image(input_path: str, output_path: str) -> bool:
        if REMOVEBG_API_KEY:
            return await BackgroundRemoverService._process_with_removebg_api(
                input_path, output_path
            )
        else:
            return await BackgroundRemoverService._process_with_rembg(
                input_path, output_path
            )

    @staticmethod
    async def _process_with_rembg(
        input_path: str, output_path: str
    ) -> bool:
        def _remove_bg():
            try:
                with Image.open(input_path) as img:
                    output = remove(img, session=rembg_session)
                    output.save(output_path, format="PNG")
                return True
            except Exception as e:
                logger.error(f"Error processing image with rembg: {e}")
                return False

        return await asyncio.to_thread(_remove_bg)

    @staticmethod
    async def _process_with_removebg_api(
        input_path: str, output_path: str
    ) -> bool:
        def _call_api():
            try:
                with open(input_path, "rb") as img_file:
                    response = requests.post(
                        "https://api.remove.bg/v1.0/removebg",
                        files={"image_file": img_file},
                        data={"size": "auto"},
                        headers={"X-Api-Key": REMOVEBG_API_KEY},
                        timeout=60,
                    )
                if response.status_code == requests.codes.ok:
                    with open(output_path, "wb") as out_file:
                        out_file.write(response.content)
                    return True
                else:
                    logger.error(
                        f"Remove.bg API Error [{response.status_code}]: {response.text}"
                    )
                    return False
            except Exception as e:
                logger.error(f"Exception during Remove.bg API call: {e}")
                return False

        return await asyncio.to_thread(_call_api)
