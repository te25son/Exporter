from flask import Request


class Context:
    def __init__(
        self, request: Request, template_folder: str, template_name: str
    ) -> None:
        self.template = self.get_template_path(request, template_folder, template_name)

    @staticmethod
    def get_template_path(request: Request, template_folder: str, template_name: str):
        """
        Method for getting the template path of the decorated function depending on
        whether it is an HTMX request or not.
        If it is not an HTMX request, we want to append '_base' to the end of the file name.
        This will load the base template and subsequently all of the scripts associated with
        it.
        """
        template = (
            template_name
            if request.headers.get("HX-Request")
            else f"{template_name}_base"
        )
        return f"{template_folder}/{template}.html"


class AuthContext(Context):
    def __init__(self, request: Request, template_name: str) -> None:
        super().__init__(request, "auth", template_name)


class MainContext(Context):
    def __init__(self, request: Request, template_name: str) -> None:
        super().__init__(request, "main", template_name)
