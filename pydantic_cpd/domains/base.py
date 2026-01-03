from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CDPModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )

    def to_cdp_params(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)
