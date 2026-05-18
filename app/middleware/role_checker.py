from fastapi import HTTPException


def role_required(user_role, allowed_roles):

    if user_role not in allowed_roles:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )