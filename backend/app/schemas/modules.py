from pydantic import BaseModel, ConfigDict

from app.core.modules import ModuleDefinition


class ModuleCatalogResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    modules: tuple[ModuleDefinition, ...]
