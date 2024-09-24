import json

from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
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
    
    def __init__(self, bedrock_runtime_client: BedrockRuntimeClient) -> None:
        self.bedrock_runtime_client = bedrock_runtime_client

    def get_answer(self, prompt: str) -> GenerationResult:
        model = "amazon.titan-text-premier-v1:0"

        # See https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text.html to learn more about the parameters
        text_generation_config: dict[str, int | float | str] = {
            "maxTokenCount": 2000
        }

        body_request = json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": text_generation_config
            }
        )

        response = self.bedrock_runtime_client.invoke_model(
            modelId=model,
            contentType="application/json",
            accept="*/*",
            body=body_request,
        )
        body_as_plain_text = response.get("body").read()
        response_body = json.loads(body_as_plain_text)

        generation_result = GenerationResult(
            input_text_token_count=response_body["inputTextTokenCount"],
            token_count=response_body["results"][0]["tokenCount"],
            completion_reason=response_body["results"][0][
                "completionReason"
            ].strip(),
            output_text=response_body["results"][0]["outputText"].strip(),
            text_generation_config=text_generation_config,
        )
        return generation_result
