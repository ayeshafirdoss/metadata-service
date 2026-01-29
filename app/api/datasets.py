from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
)


@router.post("", response_model=schemas.DatasetResponse)
def create_dataset(
    payload: schemas.DatasetCreate,
    db: Session = Depends(get_db),
):
    try:
        dataset = crud.create_dataset(
            db=db,
            fqn=payload.fqn,
            source_type=payload.source_type,
            columns=[c.model_dump() for c in payload.columns],
        )
        return dataset
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
