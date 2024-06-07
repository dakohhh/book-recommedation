from pydantic import BaseModel


class Token(BaseModel):
    user: str
    exp: str

    def get_expiry_time(self):
        return self.exp