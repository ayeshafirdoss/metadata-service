from sqlalchemy.orm import Session

from app import models
from app.lineage import validate_no_cycle


def parse_fqn(fqn: str) -> tuple[str, str, str, str]:
    """
    Parse FQN: connection.database.schema.table
    """
    parts = fqn.split(".")
    if len(parts) != 4:
        raise ValueError(
            "FQN must be in format: connection.database.schema.table"
        )
    return parts[0], parts[1], parts[2], parts[3]


def create_dataset(db: Session, fqn: str, source_type: str, columns: list[dict]):
    connection, database, schema, table = parse_fqn(fqn)

    dataset = models.Dataset(
        fqn=fqn,
        source_type=source_type,
        connection=connection,
        database=database,
        schema=schema,
        table=table,
    )

    for col in columns:
        dataset.columns.append(
            models.DatasetColumn(
                name=col["name"],
                type=col["type"],
            )
        )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


def create_lineage(
    db: Session,
    upstream_fqn: str,
    downstream_fqn: str,
):
    # Validate no cycles
    validate_no_cycle(db, upstream_fqn, downstream_fqn)

    lineage = models.Lineage(
        upstream_fqn=upstream_fqn,
        downstream_fqn=downstream_fqn,
    )

    db.add(lineage)
    db.commit()
    return lineage
