from sqlalchemy.orm import Query, DeclarativeBase


class PaginationParams:
    def __init__(
            self, page: int = 1, page_size: int = 10, order_by: str = None
    ) -> None:
        self.page = max(1, page)
        self.page_size = min(max(1, page_size), 100)
        self.order_by = order_by

    def apply(self, query: Query, model: DeclarativeBase) -> Query:
        if self.order_by:
            order_column = getattr(model, self.order_by.lstrip('-'), None)
            if order_column is not None:
                query = query.order_by(
                    order_column.desc() if self.order_by.startswith('-')
                    else order_column.asc())
        offset = (self.page - 1) * self.page_size
        return query.limit(self.page_size).offset(offset)
