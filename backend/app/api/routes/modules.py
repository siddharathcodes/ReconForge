from fastapi import APIRouter, status

from app.core.modules import MODULE_CATALOG
from app.schemas.modules import ModuleCatalogResponse

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get(
    "",
    response_model=ModuleCatalogResponse,
    status_code=status.HTTP_200_OK,
    summary="ReconForge module catalog",
)
def list_modules() -> ModuleCatalogResponse:
    return ModuleCatalogResponse(modules=MODULE_CATALOG)
