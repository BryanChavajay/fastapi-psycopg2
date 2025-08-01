from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    sv: int


class RefreshTokenPayload(BaseModel):
    sub: str
