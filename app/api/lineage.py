from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LineageCreate
from app.crud import create_lineage
from app.lineage import LineageCycleError

router = APIRouter(
    prefix="/lineage",
    tags=["lineage"],
)


@router.post("")
def add_lineage(
    payload: LineageCreate,
    db: Session = Depends(get_db),
):
    try:
        create_lineage(
            db=db,
            upstream_fqn=payload.upstream_fqn,
            downstream_fqn=payload.downstream_fqn,
        )
        return {"message": "lineage created"}
    except LineageCycleError as e:
        raise HTTPException(status_code=400, detail=str(e))
