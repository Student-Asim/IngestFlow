# for later

from pydantic import BaseModel
from datetime import datetime

class Document(BaseModel):
    id:str
    filename:str
    uploaded_at:datetime
    status:str