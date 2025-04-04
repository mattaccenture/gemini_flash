import os
import tempfile
import argparse
import pathlib
import subprocess
import requests
from google import genai
from google.genai import types

MODEL = "gemini-2.0-flash-exp"

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)

def upload_files(client, file_paths):
    uploaded_files = []
    for path in file_paths:
        if path.startswith("http://") or path.startswith("https://"):
            response = requests.get(path)
            file_name = path.split("/")[-1]
            pathlib.Path(file_name).write_text(response.text)
            path = file_name

        uploaded_file = client.files.upload(file=path)
        uploaded_files.append(uploaded_file)
    return uploaded_files


def generate_content(client, prompt, uploaded_files, show=False): 
    user_prompt = f"""

            {prompt}

    """

    print(f"Using prompt: {user_prompt}")

    contents = [prompt]
    contents.extend(uploaded_files)

    generate_content_config = types.GenerateContentConfig(
            temperature=1,
            max_output_tokens=8192,
            response_modalities=[
                "image",
                "text",
            ],
            response_mime_type="text/plain",
        )

    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue

        with tempfile.NamedTemporaryFile(suffix=".png", prefix="ai_", delete=False) as temp_file:
            temp_filename = temp_file.name        
            if chunk.candidates[0].content.parts[0].inline_data: 
                file_name = temp_filename 
                save_binary_file(
                    file_name, chunk.candidates[0].content.parts[0].inline_data.data
                )
                print(
                    f"File of mime type {chunk.candidates[0].content.parts[0].inline_data.mime_type} "
                    f"saved to: {file_name}"
                )
            else:
                print(chunk.text)

    print("Finished")
    
    if show:
        print(f"Opening {file_name}")

        subprocess.run(["xdg-open", file_name])

def _get_api_key():
    if api_key := os.environ.get("GEMINI_API_KEY"):
        return api_key

    raise ValueError("GEMINI_API_KEY nie jest ustawiony w zmiennych środowiskowych.")


def main():
    api_key = _get_api_key()

    parser = argparse.ArgumentParser(description="Generuj zawartość za pomocą Gemini API.")
    parser.add_argument("--text", type=str, required=True, help="Prompt do generowania zawartości.")
    parser.add_argument("--files", nargs="+", required=False, default=[], help="Ścieżki do plików lub URL.")
    parser.add_argument("--show", default=False, action="store_true")
    
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    uploaded_files = upload_files(client, args.files)

    generate_content(client, args.text, uploaded_files, args.show)

if __name__ == "__main__":
    main()



