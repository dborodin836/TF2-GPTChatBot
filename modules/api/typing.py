# Request and Response types for TextGenWebUI OpenAI compatible API
# https://github.com/oobabooga/text-generation-webui/blob/main/extensions/openai/typing.py
import time
from typing import List

from pydantic import BaseModel, Field


class GenerationOptions(BaseModel):
    preset: str | None = Field(
        default=None,
        description="The name of a file under text-generation-webui/presets (without the .yaml extension). The "
        "sampling parameters that get overwritten by this option are the keys in the default_preset() "
        "function in modules/presets.py.",
    )
    min_p: float = 0
    dynamic_temperature: bool = False
    dynatemp_low: float = 1
    dynatemp_high: float = 1
    dynatemp_exponent: float = 1
    smoothing_factor: float = 0
    smoothing_curve: float = 1
    top_k: int = 0
    repetition_penalty: float = 1
    repetition_penalty_range: int = 1024
    typical_p: float = 1
    tfs: float = 1
    top_a: float = 0
    epsilon_cutoff: float = 0
    eta_cutoff: float = 0
    guidance_scale: float = 1
    negative_prompt: str = ""
    penalty_alpha: float = 0
    mirostat_mode: int = 0
    mirostat_tau: float = 5
    mirostat_eta: float = 0.1
    temperature_last: bool = False
    do_sample: bool = True
    seed: int = -1
    encoder_repetition_penalty: float = 1
    no_repeat_ngram_size: int = 0
    truncation_length: int = 0
    max_tokens_second: int = 0
    prompt_lookup_num_tokens: int = 0
    custom_token_bans: str = ""
    sampler_priority: List[str] | str | None = Field(
        default=None,
        description='List of samplers where the first items will appear first in the stack. Example: ["top_k", '
        '"temperature", "top_p"].',
    )
    auto_max_new_tokens: bool = False
    ban_eos_token: bool = False
    add_bos_token: bool = True
    skip_special_tokens: bool = True
    grammar_string: str = ""


class CompletionRequestParams(BaseModel):
    model: str | None = Field(
        default=None,
        description="Unused parameter. To change the model, use the /v1/internal/model/load endpoint.",
    )
    prompt: str | List[str]
    best_of: int | None = Field(default=1, description="Unused parameter.")
    echo: bool | None = False
    frequency_penalty: float | None = 0
    logit_bias: dict | None = None
    logprobs: int | None = None
    max_tokens: int | None = 16
    n: int | None = Field(default=1, description="Unused parameter.")
    presence_penalty: float | None = 0
    stop: str | List[str] | None = None
    stream: bool | None = False
    suffix: str | None = None
    temperature: float | None = 1
    top_p: float | None = 1
    user: str | None = Field(default=None, description="Unused parameter.")


class CompletionRequest(GenerationOptions, CompletionRequestParams):
    pass


class ChatCompletionResponse(BaseModel):
    id: str
    choices: List[dict]
    created: int = int(time.time())
    model: str
    object: str = "chat.completion"
    usage: dict
