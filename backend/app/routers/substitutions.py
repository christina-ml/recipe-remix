from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/substitutions", tags=["substitutions"])


@router.get("/", response_model=List[schemas.SubstitutionOut])
def list_substitutions(db: Session = Depends(get_db)):
    subs = db.query(models.Substitution).all()
    return [crud.to_substitution_out(db, s) for s in subs]


@router.post("/", response_model=schemas.SubstitutionOut, status_code=201)
def create_substitution(sub: schemas.SubstitutionCreate, db: Session = Depends(get_db)):
    db_sub = crud.create_substitution(db, sub)
    return crud.to_substitution_out(db, db_sub)


@router.post("/{substitution_id}/vote", response_model=schemas.SubstitutionOut)
def vote_substitution(
    substitution_id: int, vote: schemas.VoteCreate, db: Session = Depends(get_db)
):
    if vote.value not in (1, -1):
        raise HTTPException(status_code=400, detail="Vote value must be 1 or -1")
    sub = db.query(models.Substitution).filter(models.Substitution.id == substitution_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Substitution not found")
    crud.cast_vote(db, substitution_id, vote.value)
    return crud.to_substitution_out(db, sub)
