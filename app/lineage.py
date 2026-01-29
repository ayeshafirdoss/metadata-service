from sqlalchemy.orm import Session
from app.models import Lineage


class LineageCycleError(Exception):
    """Raised when lineage creation would introduce a cycle."""
    pass


def _dfs_has_path(
    db: Session,
    start_fqn: str,
    target_fqn: str,
    visited: set[str],
) -> bool:
    """
    DFS to check if there is a path from start_fqn to target_fqn.
    """
    if start_fqn == target_fqn:
        return True

    visited.add(start_fqn)

    # Find all downstream datasets from start_fqn
    children = (
        db.query(Lineage)
        .filter(Lineage.upstream_fqn == start_fqn)
        .all()
    )

    for edge in children:
        next_fqn = edge.downstream_fqn
        if next_fqn not in visited:
            if _dfs_has_path(db, next_fqn, target_fqn, visited):
                return True

    return False


def validate_no_cycle(
    db: Session,
    upstream_fqn: str,
    downstream_fqn: str,
) -> None:
    """
    Validates that adding upstream_fqn -> downstream_fqn
    does NOT create a cycle.
    """

    # Direct self-loop check
    if upstream_fqn == downstream_fqn:
        raise LineageCycleError(
            "Invalid lineage: dataset cannot depend on itself."
        )

    # If downstream can already reach upstream → cycle
    visited: set[str] = set()
    has_cycle = _dfs_has_path(
        db=db,
        start_fqn=downstream_fqn,
        target_fqn=upstream_fqn,
        visited=visited,
    )

    if has_cycle:
        raise LineageCycleError(
            f"Invalid lineage: adding {upstream_fqn} → {downstream_fqn} "
            f"would create a cycle."
        )
