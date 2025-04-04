import requests
import pathlib
import tempfile
import subprocess

from logger import get_logger

logger = get_logger(__name__)


class OutputFile:
    def __init__(self, path: str = ""):
        self.path = path if path else tempfile.mktemp(suffix='.png')  

    def write(self, data):
        try:
            path = pathlib.Path(self.path)
            path.parent.mkdir(parents=True, exist_ok=True)
           
            with open(path, "wb") as f:
                for d in data:
                    f.write(d)

            logger.info(f"Image saved to {self.path}")
        except Exception as err:
            logger.error(f"Failed to write to: {self.path}: {err}")

    def open(self):
        logger.info(f"Opening {self.path}")
        subprocess.run(["xdg-open", self.path])


class Files:
    def __init__(self, files):
        self.files = files

    def __iter__(self):
        for path in self.files:
            if path.startswith("http://") or path.startswith("https://"):
                response = requests.get(path)
                file_name = path.split("/")[-1]
                pathlib.Path(file_name).write_text(response.text)
                path = file_name

            yield path

