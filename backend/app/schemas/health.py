from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthCheck(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: Literal["ok"]
    service: str
    version: str
    checks: dict[str, str]
