import argparse

from ai.client import Ai
from ai.files import OutputFile
from logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Generuj zawartość za pomocą Gemini API.")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt do generowania zawartości.")
    parser.add_argument("--files", nargs="+", required=False, default=[], help="Ścieżki do plików lub URL.")
    parser.add_argument("--output", type=str, required=False)
    parser.add_argument("--open", default=False, action="store_true")
    
    args = parser.parse_args()

    ai = Ai()

    uploaded_files = ai.upload_files(args.files)
    response = ai.generate(
        args.prompt,
        uploaded_files
    )

    output = OutputFile(args.output)

    if response is None:
        logger.warning("No response from gemini")
        return
    
    output.write(
        response
    )

    if args.open:
        output.open()


if __name__ == "__main__":
    main()



