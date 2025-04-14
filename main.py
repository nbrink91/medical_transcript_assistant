import os
import sys
from datetime import datetime, timezone
from openai import AzureOpenAI
import json

from dotenv import load_dotenv
load_dotenv()


def main():

    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    model_name = "gpt-35-turbo"
    model_name = "gpt-4o"
    model_name = "gpt-4"

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )

    # Read system prompt from a file
    with open("system_prompt.txt", "r") as file:
        system_prompt = file.read()

    # Read user prompt from a file
    with open("user_prompt.txt", "r") as file:
        user_prompt = file.read()

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=model_name
    )

    response_content = response.choices[0].message.content
    print(response_content)

    # save response to a file with timestamp
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')    
    with open(f"logs/{timestamp}_response.json", "w") as file:
        json.dump({
            "model_name": model_name,
            "timestamp": timestamp,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "response": response_content
        }, file, indent=4)

    with open(f"logs/{timestamp}_response.txt", "w") as file:
        file.write("=========================\n")
        file.write(f"Model: {model_name}\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write("=========================\n")
        file.write("System Prompt\n")
        file.write("=========================\n")
        file.write(system_prompt)
        file.write("\n")
        file.write("=========================\n")
        file.write("User Prompt\n")
        file.write("=========================\n")
        file.write(user_prompt)
        file.write("\n")
        file.write("=========================\n")
        file.write("Response\n")
        file.write("=========================\n")
        file.write(response_content)

if __name__ == "__main__":
    sys.exit(main())