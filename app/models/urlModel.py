from pydantic import BaseModel


class UrlModel(BaseModel):
    """
    Model for storing URL data.
    """
    url : str