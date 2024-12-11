from pydantic import BaseModel


class PaginationSchema(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    pages: int
