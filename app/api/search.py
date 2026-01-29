from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Dataset, DatasetColumn

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("")
def search_datasets(
    query: str,
    db: Session = Depends(get_db),
):
    results: dict[str, dict] = {}

    q = f"%{query.lower()}%"

    # Priority 1: table name
    table_matches = (
        db.query(Dataset)
        .filter(Dataset.table.ilike(q))
        .all()
    )

    for ds in table_matches:
        results[ds.fqn] = {
            "priority": 1,
            "dataset": ds,
        }

    # Priority 2: column name
    column_matches = (
        db.query(Dataset)
        .join(DatasetColumn)
        .filter(DatasetColumn.name.ilike(q))
        .all()
    )

    for ds in column_matches:
        if ds.fqn not in results:
            results[ds.fqn] = {
                "priority": 2,
                "dataset": ds,
            }

    # Priority 3: schema name
    schema_matches = (
        db.query(Dataset)
        .filter(Dataset.schema.ilike(q))
        .all()
    )

    for ds in schema_matches:
        if ds.fqn not in results:
            results[ds.fqn] = {
                "priority": 3,
                "dataset": ds,
            }

    # Priority 4: database name
    database_matches = (
        db.query(Dataset)
        .filter(Dataset.database.ilike(q))
        .all()
    )

    for ds in database_matches:
        if ds.fqn not in results:
            results[ds.fqn] = {
                "priority": 4,
                "dataset": ds,
            }

    # Sort results by priority
    sorted_results = sorted(
        results.values(),
        key=lambda x: x["priority"],
    )

    # Build response
    response = [
        {
            "fqn": item["dataset"].fqn,
            "source_type": item["dataset"].source_type,
            "priority": item["priority"],
        }
        for item in sorted_results
    ]

    return {
        "query": query,
        "count": len(response),
        "results": response,
    }
