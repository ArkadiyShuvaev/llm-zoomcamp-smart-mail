import json
from typing import Any, Dict
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
from common.settings import Settings
from services.generation.generation_result import GenerationResult
from services.generation.generation_service import GenerationService


class AwsGenerationService(GenerationService):
    """
    AwsGenerationService is a concrete implementation of the GenerationService
    abstract base class. It uses AWS Bedrock Runtime to generate text responses
    based on a given prompt.

    Attributes:
        bedrock_runtime_client (BedrockRuntimeClient): The AWS Bedrock Runtime client used to invoke the model.

    Methods:
        get_answer(prompt: str) -> GenerationResult:
            Generates a text response based on the given prompt using the AWS Bedrock Runtime.
    """

    def __init__(self, settings: Settings, bedrock_runtime_client: BedrockRuntimeClient) -> None:
        self._settings = settings
        self._bedrock_runtime_client = bedrock_runtime_client

    def get_answer(self, prompt: str) -> GenerationResult:
        model = self._settings.aws_model_name

        # See https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html
        request: Dict[str, Any] = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ]
        }

        response = self._bedrock_runtime_client.invoke_model(
            modelId=model,
            contentType="application/json",
            accept="*/*",
            body=json.dumps(request)
        )

        body_as_plain_text = response.get("body").read()
        response_body = json.loads(body_as_plain_text)

        config_for_logging: Dict[str, Any] = {k: v for k, v in request.items() if k != "messages"}

        generation_result = GenerationResult(
            input_text_token_count=response_body["usage"]["input_tokens"],
            token_count=response_body["usage"]["output_tokens"],
            completion_reason=response_body["stop_reason"].strip(),
            output_text=response_body["content"][0]["text"].strip(),
            text_generation_config=config_for_logging
        )
        return generation_result
