from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base


class Category(Base):
    """This is an abstract base class for all categories."""

    __abstract__ = True

    category_id: Mapped[int] = mapped_column(primary_key=True)
    """The identifier for a category (primary key)."""
    category_name: Mapped[str] = mapped_column(unique=True)
    """The name of a category (unique)."""
    category_is_deleted: Mapped[bool] = mapped_column(default=False)
    """A flag indicating whether a category is deleted. Default is False."""


class IncomeCategory(Category):
    """Represents categories for income."""

    __tablename__ = "income_categories"


class ExpenseCategory(Category):
    """Represents categories for expenses."""

    __tablename__ = "expense_categories"
