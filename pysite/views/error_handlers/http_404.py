# coding=utf-8
from werkzeug.exceptions import NotFound

from pysite.base_route import ErrorView


class Error404View(ErrorView):
    name = "error_404"
    error_code = 404

    def get(self, error: NotFound):
        return "replace me with a template, 404 not found", 404
