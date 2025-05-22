"""Example script to generate clinical notes using Azure OpenAI Service."""

import json
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


def generate_clinical_notes(client, model, system_prompt, transcript):
    """Generate clinical notes using Azure OpenAI Service."""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": transcript,
            },
        ],
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=model,
    )

    response_content = response.choices[0].message.content
    return response_content


def save_results(
    content,
    model_name,
    system_prompt,
    user_prompt,
    appointment_reason=None,
    icd_10_code=None,
):
    """Save the response content to a file."""
    print(content)

    # save response to a file with timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    with open(f"logs/{timestamp}_{icd_10_code}_response.json", "w") as file:
        json.dump(
            {
                "model_name": model_name,
                "timestamp": timestamp,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "appointment_reason": appointment_reason,
                "icd_10_code": icd_10_code,
                "response": content,
            },
            file,
            indent=4,
        )

    with open(f"logs/{timestamp}_{icd_10_code}_response.txt", "w") as file:
        file.write("=========================\n")
        file.write(f"Model: {model_name}\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Appointment Reason: {appointment_reason}\n")
        file.write(f"ICD-10 Code: {icd_10_code}\n")
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
        file.write(content)


def main():
    """Load environment variables and generate clinical notes."""
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    # model_name = "gpt-35-turbo"
    # model_name = "gpt-4o"
    # model_name = "gpt-4"
    model_name = "gpt-4o-mini"

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )

    # Read system prompt from a file
    with open("system_prompt.txt", "r") as file:
        system_prompt = file.read()

    # Load prompts from json file
    with open("prompts/prompts.json", "r") as file:
        prompt_metadata = json.load(file)
        # Iterate through the prompts
        for prompt_m in prompt_metadata[:5]:
            prompt_path = prompt_m["path"]
            appointment_reason = prompt_m["appointmentReason"]
            icd_10_code = prompt_m["icd10code"]
            with open(f"prompts/{prompt_path}", "r") as file:
                user_prompt = file.read()
                response_content = generate_clinical_notes(
                    client, model_name, system_prompt, user_prompt
                )
                save_results(
                    response_content,
                    model_name,
                    system_prompt,
                    user_prompt,
                    appointment_reason,
                    icd_10_code,
                )


if __name__ == "__main__":
    sys.exit(main())
