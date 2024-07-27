class ExceededLengthError(Exception):
    """This class represents a custom exception raised when the length of a category name exceeds 30
    characters."""

    def __init__(
        self,
        message="⚠️ Название категории не должно превышать 30 символов ⚠️\n\n"
        "Пожалуйста, попробуйте указать другое название:",
    ):
        """
        The constructor method initializes an instance of the ExceededLengthError class.

        :param message: A custom error message indicating that the category name should not exceed
            30 characters. Defaults to a predefined message in Russian.
        """
        self.message = message
        super().__init__(self.message)
