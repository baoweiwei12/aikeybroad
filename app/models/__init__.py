from app.core.database import Base, engine
from .user import *
from .cdkey import *
from .api_config import *
from .ai_chat_message import *
from .aippt import *

Base.metadata.create_all(bind=engine)
