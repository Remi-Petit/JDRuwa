import strawberry

@strawberry.type
class UserType:
    id: int
    email: str
    username: str
    created_at: str