import os

from google import genai
from google.genai import types

from logger import get_logger

MODEL = "gemini-2.0-flash-exp"


logger = get_logger(__name__)


class Ai:
    def __init__(self):
        self.client = genai.Client(api_key=self.api_key)

    @property
    def api_key(self):
        if key := os.getenv("GEMINI_API_KEY"):
            return key

        raise ValueError("GEMINI_API_KEY is missing")

    def config(self, temperatue=1, max_output_tokens=8192):
        return types.GenerateContentConfig(
            temperature=temperatue,
            max_output_tokens=max_output_tokens,
            response_modalities=[
                "image",
                "text",
            ],
            response_mime_type="text/plain",
        )

    def generate(self, prompt, files=[]):
        contents = [prompt]
        contents.extend(files)

        logger.debug(f"Generating content: prompt={prompt}, files={files}")

        for chunk in self.client.models.generate_content_stream(
            model=MODEL,
            contents=contents,
            config=self.config(),
        ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue

            if data := chunk.candidates[0].content.parts[0].inline_data: 
                logger.debug("Received chunk")
                yield data.data


    def upload_files(self, paths: list):
        if not len(paths):
            return []

        logger.info(f"Uploading {len(paths)} files")

        uploaded_files = []

        for path in paths:
            uploaded_file = self.client.files.upload(file=path)
            uploaded_files.append(uploaded_file)

        logger.info(f"Uploaded {len(paths)} files")

        return uploaded_files




