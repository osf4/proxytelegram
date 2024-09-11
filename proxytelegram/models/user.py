from pydantic import BaseModel


class User(BaseModel):
    id: int
    topic_id: int

    blocked: bool = False