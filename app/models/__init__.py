from app.core.database import Base, engine
from .user import *
from .cdkey import *
from .api_config import *

Base.metadata.create_all(bind=engine)
