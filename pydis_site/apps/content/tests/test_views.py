from pathlib import Path
from unittest import TestCase

from django.http import Http404
from django.test import RequestFactory, SimpleTestCase, override_settings

from pydis_site.apps.content.tests.helpers import (
    BASE_PATH, MockPagesTestCase, PARSED_CATEGORY_INFO, PARSED_HTML, PARSED_METADATA
)
from pydis_site.apps.content.views import PageOrCategoryView


def patch_dispatch_attributes(view: PageOrCategoryView, location: str) -> None:
    """
    Set the attributes set in the `dispatch` method manually.

    This is necessary because it is never automatically called during tests.
    """
    view.location = Path(BASE_PATH, location)

    # URL location on the filesystem
    view.full_location = view.location

    # Possible places to find page content information
    view.category_path = view.full_location
    view.page_path = view.full_location.with_suffix(".md")


@override_settings(CONTENT_PAGES_PATH=BASE_PATH)
class PageOrCategoryViewTests(MockPagesTestCase, SimpleTestCase, TestCase):
    """Tests for the PageOrCategoryView class."""

    def setUp(self):
        """Set test helpers, then set up fake filesystem."""
        self.factory = RequestFactory()
        self.view = PageOrCategoryView.as_view()
        self.ViewClass = PageOrCategoryView()
        super().setUp()

    # Integration tests
    def test_valid_page_or_category_returns_200(self):
        cases = [
            ("Page at root", "root"),
            ("Category page", "category"),
            ("Page in category", "category/with_metadata"),
            ("Subcategory page", "category/subcategory"),
            ("Page in subcategory", "category/subcategory/with_metadata"),
        ]
        for msg, path in cases:
            with self.subTest(msg=msg, path=path):
                request = self.factory.get(f"/{path}")
                response = self.view(request, location=path)
                self.assertEqual(response.status_code, 200)

    def test_nonexistent_page_returns_404(self):
        with self.assertRaises(Http404):
            request = self.factory.get("/invalid")
            self.view(request, location="invalid")

    # Unit tests
    def test_get_template_names_returns_correct_templates(self):
        category_template = "content/listing.html"
        page_template = "content/page.html"
        cases = [
            ("root", page_template),
            ("root_without_metadata", page_template),
            ("category/with_metadata", page_template),
            ("category/subcategory/with_metadata", page_template),
            ("category", category_template),
            ("category/subcategory", category_template),
        ]

        for path, expected_template in cases:
            with self.subTest(path=path, expected_template=expected_template):
                patch_dispatch_attributes(self.ViewClass, path)
                self.assertEqual(self.ViewClass.get_template_names(), [expected_template])

    def test_get_template_names_with_nonexistent_paths_returns_404(self):
        for path in ("invalid", "another_invalid", "nonexistent"):
            with self.subTest(path=path):
                patch_dispatch_attributes(self.ViewClass, path)
                with self.assertRaises(Http404):
                    self.ViewClass.get_template_names()

    def test_get_template_names_returns_page_template_for_category_with_page(self):
        """Make sure the proper page is returned for category locations with pages."""
        patch_dispatch_attributes(self.ViewClass, "tmp")
        self.assertEqual(self.ViewClass.get_template_names(), ["content/page.html"])

    def test_get_context_data_with_valid_page(self):
        """The method should return required fields in the template context."""
        request = self.factory.get("/root")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="root")

        cases = [
            ("Context includes HTML page content", "page", PARSED_HTML),
            ("Context includes page title", "page_title", PARSED_METADATA["title"]),
            (
                "Context includes page description",
                "page_description",
                PARSED_METADATA["description"]
            ),
            (
                "Context includes relevant link names and URLs",
                "relevant_links",
                PARSED_METADATA["relevant_links"]
            ),
        ]
        context = self.ViewClass.get_context_data()
        for msg, key, expected_value in cases:
            with self.subTest(msg=msg):
                self.assertEqual(context[key], expected_value)

    def test_get_context_data_with_valid_category(self):
        """The method should return required fields in the template context."""
        request = self.factory.get("/category")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="category")

        cases = [
            (
                "Context includes subcategory names and their information",
                "categories",
                {"subcategory": PARSED_CATEGORY_INFO}
            ),
            (
                "Context includes page names and their metadata",
                "pages",
                {"with_metadata": PARSED_METADATA}
            ),
            (
                "Context includes page description",
                "page_description",
                PARSED_CATEGORY_INFO["description"]
            ),
            ("Context includes page title", "page_title", PARSED_CATEGORY_INFO["title"]),
        ]

        context = self.ViewClass.get_context_data()
        for msg, key, expected_value in cases:
            with self.subTest(msg=msg):
                self.assertEqual(context[key], expected_value)

    def test_get_context_data_for_category_with_page(self):
        """Make sure the proper page is returned for category locations with pages."""
        request = self.factory.get("/category")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="tmp")

        context = self.ViewClass.get_context_data()
        expected_page_context = {
            "page": PARSED_HTML,
            "page_title": PARSED_METADATA["title"],
            "page_description": PARSED_METADATA["description"],
            "relevant_links": PARSED_METADATA["relevant_links"],
            "subarticles": [{"path": "category", "name": "Category Name"}]
        }
        for key, expected_value in expected_page_context.items():
            with self.subTest():
                self.assertEqual(context[key], expected_value)

    def test_get_context_data_breadcrumbs(self):
        """The method should return correct breadcrumbs."""
        request = self.factory.get("/category/subcategory/with_metadata")
        self.ViewClass.setup(request)
        self.ViewClass.dispatch(request, location="category/subcategory/with_metadata")

        context = self.ViewClass.get_context_data()
        self.assertEquals(
            context["breadcrumb_items"],
            [
                {"name": PARSED_CATEGORY_INFO["title"], "path": "."},
                {"name": PARSED_CATEGORY_INFO["title"], "path": "category"},
                {"name": PARSED_CATEGORY_INFO["title"], "path": "category/subcategory"},
            ]
        )
