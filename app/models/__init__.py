from app.core.database import Base, engine
from .user import *
from .cdkey import *

Base.metadata.create_all(bind=engine)
