import asyncio
from typing import Type, Union, get_type_hints

from fastapi import APIRouter
from pydantic import BaseModel, ValidationError, create_model
from starlette import status
from starlette.responses import Response

from config import Config, ValidatableConfig, config
from modules.utils.config import DROP_KEYS, save_config

router = APIRouter(
    prefix="/settings",
)


def create_partial_update_model(base_model: Type[BaseModel]) -> Type[BaseModel]:
    field_definitions = {}
    for name, type_hint in get_type_hints(base_model).items():
        field_definitions[name] = (Union[type_hint, None], None)
    return create_model("PartialUpdateModel", **field_definitions)  # type: ignore[call-overload]


# Create partial update model dynamically
PartialUpdateModel: Type[BaseModel] = create_partial_update_model(Config)


@router.get("/")
async def handle_get_settings():
    return config.dict()


@router.get("/default")
async def handle_get_default_settings():
    # Generate default config
    cfg = Config()
    # Remove keys that are useless
    dict_ = {k: v for k, v in cfg.dict().items() if k not in DROP_KEYS}
    return dict_


@router.post("/")
async def update_settings(settings: PartialUpdateModel):  # type: ignore[valid-type]
    update_data = {k: v for k, v in settings.dict().items() if v is not None}  # type: ignore[attr-defined]

    try:
        # Get current model as a dict, can't use Config() 'cos of possible session overwrites
        current_config_dict = config.model_dump()
        # Update that dict with data received from request
        current_config_dict.update(update_data)
        # If it doesn't throw ValidationError we're safe to go
        tmp_config = ValidatableConfig(**current_config_dict)
        # Finally replace app config with updated config
        config.update_config(config.model_copy(update=tmp_config.dict(), deep=True))
        # Save config on filesystem
        await asyncio.to_thread(save_config, "config.ini")
    except ValidationError as exc:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=exc.json())

    return Response(status_code=status.HTTP_201_CREATED)
