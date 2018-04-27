from pysite.base_route import RouteView


class IndexView(RouteView):
    path = "/"
    name = "index"

    def get(self):
        return self.render("main/index.html")
