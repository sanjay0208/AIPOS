from app.database.models.user import User


def get_user_profile(user: User):
    """
    Return the current user's profile.
    """

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }