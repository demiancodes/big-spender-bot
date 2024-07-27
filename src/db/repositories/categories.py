from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from src.db.models import ExpenseCategory, IncomeCategory
from src.db.repositories.exceptions import ExceededLengthError

MAX_CATEGORY_NAME_LENGTH: int = 30


def create_category(
    category_name: str,
    model_type: Type[IncomeCategory | ExpenseCategory],
    session: Session,
) -> IncomeCategory | ExpenseCategory:
    """
    Creates a new category with the given name and category model type.

    :param category_name: The name of the category to create.
    :param model_type: Specifies the category model type to be created. Accepts either
        IncomeCategory or ExpenseCategory to determine whether to create an income category or
        expense category, respectively.
    :param session: The SQLAlchemy session to be used for executing database operations within the
        transaction.
    :return: The newly created category.
    :raise ExceededLengthError: If the length of the category name exceeds MAX_CATEGORY_NAME_LENGTH.
    :raise IntegrityError: If there is a violation of database integrity constraints, such as a
        duplicate category name.
    """
    try:
        if len(category_name) <= MAX_CATEGORY_NAME_LENGTH:
            new_category = model_type(category_name=category_name)
            session.add(new_category)
            session.commit()
            return new_category
        else:
            raise ExceededLengthError
    except IntegrityError:
        session.rollback()
        raise


def get_categories(
    session: Session,
    model_type: Type[IncomeCategory | ExpenseCategory],
) -> Sequence[IncomeCategory | ExpenseCategory]:
    """
    This function performs a database query using the provided SQLAlchemy session and model type.
    It returns all categories where category_is_deleted is set to 0, indicating they are active.
    The results are ordered by the category_name field.

    :param session: The SQLAlchemy session to be used for executing database operations within the
        transaction.
    :param model_type: The type of the model to query for. This should be either IncomeCategory or
        ExpenseCategory.
    :return: A list of IncomeCategory or ExpenseCategory instances that are active.
    :raise NoResultFound: If no categories are found.
    """
    categories = session.scalars(
        select(model_type)
        .filter(model_type.category_is_deleted == 0)
        .order_by(model_type.category_name),
    ).all()
    if categories:
        return categories
    else:
        raise NoResultFound


def get_category_name_by_id(
    session: Session,
    model_type: Type[IncomeCategory | ExpenseCategory],
    category_id: int,
) -> str:
    """
    Retrieves the name of a category by its identifier from the database.

    :param session: The SQLAlchemy session to be used for executing database operations within the
        transaction.
    :param model_type: The type of the model to query for. This should be either IncomeCategory or
        ExpenseCategory.
    :param category_id: The identifier of the category for which the name is to be retrieved.
    :return: A string with the category name.
    """
    return session.scalar(
        select(model_type.category_name).filter(model_type.category_id == category_id),
    )


def rename_category(
    new_category_name: str,
    session: Session,
    model_type: Type[IncomeCategory | ExpenseCategory],
    category_id: int,
):
    """
    This function updates the name of an income or expense category in the database.

    :param new_category_name: The new name for the category.
    :param session: The SQLAlchemy session to be used for executing database operations within the
        transaction.
    :param model_type: The type of the category model, which can be either IncomeCategory or
        ExpenseCategory.
    :param category_id: The unique identifier of the category to be renamed.
    :raise ExceededLengthError: If the length of the new category name exceeds
        MAX_CATEGORY_NAME_LENGTH.
    """
    if len(new_category_name) <= MAX_CATEGORY_NAME_LENGTH:
        category_to_rename = session.scalar(
            select(model_type).filter(model_type.category_id == category_id),
        )
        category_to_rename.category_name = new_category_name
        session.commit()
    else:
        raise ExceededLengthError


def soft_delete_category(
    session: Session,
    model_type: Type[IncomeCategory | ExpenseCategory],
    category_id: int,
):
    """
    This function does not actually remove the category from the database. Instead, it sets a flag
    on the category to indicate that it has been deleted and modifies the category's name to reflect
    this change. This allows the data to be preserved for analysis and, if necessary, the category
    can be restored later.

    :param session: The SQLAlchemy session to be used for executing database operations within the
        transaction.
    :param model_type: The type of the category model, which can be either IncomeCategory or
        ExpenseCategory.
    :param category_id: The unique identifier of the category to be softly deleted.
    """
    category_to_delete = session.scalar(
        select(model_type).filter(model_type.category_id == category_id),
    )
    category_to_delete.category_is_deleted = 1
    category_to_delete.category_name += f" (категория удалена) [ID: {category_id}]"
    session.commit()
