from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    user_id: str
    nickname: str
    password: str
    is_admin: bool = False
    create_time: datetime = datetime.utcnow()
    is_withdraw: bool = False

    def withdraw(self):
        self.is_withdraw = True
