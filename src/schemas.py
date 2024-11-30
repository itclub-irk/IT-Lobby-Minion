import enum
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ButtonTypeEnum(str, enum.Enum):
    static = 'static'
    dynamic = 'dynamic'


class KbButtonSchema(BaseModel):
    id: int
    name: str
    url: HttpUrl
    type: ButtonTypeEnum


class UserSchema(BaseModel):
    id: int
    full_name: str
    created_at: datetime


class WelcomeMessageSchema(BaseModel):
    id: int
    text: str


class SettingsSchema(BaseModel):
    id: int
    dynamic_button_count: int
    welcome_message: str
