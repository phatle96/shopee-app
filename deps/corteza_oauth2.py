from fastapi import HTTPException, status

from deps.models import Token
from sqlmodel import Session, select
from deps import models, scripts

import requests


def save_client_credentials(
    db: Session,
    token: str,
    client_id: int,
    client_secret: str,
    tokenUrl: str,
):

    try:
        jwt_credential = scripts.jwt_decode(token)
        user_id = int(jwt_credential.get("sub"))

        data = models.CortezaCredentialsInDB(
            client_id=client_id,
            client_secret=client_secret,
            token=token,
            user_id=user_id,
            tokenUrl=tokenUrl,
        )

        db_data = models.CortezaCredentialsInDB.model_validate(data)
        db.add(db_data)
        db.commit()
        db.refresh(db_data)

        return {"client_id": client_id, "client_secret": client_secret}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def get_token(db: Session, token: str):

    try:

        jwt_credential = scripts.jwt_decode(token)
        user_id = int(jwt_credential.get("sub"))

        corteza_credentail = db.exec(
            select(models.CortezaCredentialsInDB).where(
                models.CortezaCredentialsInDB.user_id == user_id
            )
        ).first()

        print("corteza_credentail: ----", corteza_credentail)

        if corteza_credentail:

            form = {
                "scope": "api",
                "grant_type": "client_credentials",
                "client_id": corteza_credentail.client_id,
                "client_secret": corteza_credentail.client_secret,
            }

            print("form", form)

            response = requests.post(corteza_credentail.tokenUrl, data=form)
            return response.json()

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Corteza credential not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
