from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def commit_to_db(db: Session, instance, commit: bool = True, refresh: bool = False):
    """
    Adds the object to the database, performs the commit, and optionally refreshes the object.
    """
    try:
        db.add(instance)  # Add the object to the session
        if commit:
            db.commit()  # Commit the session
        if refresh:
            db.refresh(instance)  # Reload the latest data from the DB
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database transaction error: {str(e)}"
        )