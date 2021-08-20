from pathlib import Path

from django.http import Http404

from pydis_site.apps.content import utils
from pydis_site.apps.content.tests.helpers import (
    BASE_PATH, MockPagesTestCase, PARSED_CATEGORY_INFO, PARSED_HTML, PARSED_METADATA
)


class GetCategoryTests(MockPagesTestCase):
    """Tests for the get_category function."""

    def test_get_valid_category(self):
        result = utils.get_category(Path(BASE_PATH, "category"))

        self.assertEqual(result, {"title": "Category Name", "description": "Description"})

    def test_get_nonexistent_category(self):
        with self.assertRaises(Http404):
            utils.get_category(Path(BASE_PATH, "invalid"))

    def test_get_category_with_path_to_file(self):
        # Valid categories are directories, not files
        with self.assertRaises(Http404):
            utils.get_category(Path(BASE_PATH, "root.md"))

    def test_get_category_without_info_yml(self):
        # Categories should provide an _info.yml file
        with self.assertRaises(FileNotFoundError):
            utils.get_category(Path(BASE_PATH, "tmp/category/subcategory_without_info"))


class GetCategoriesTests(MockPagesTestCase):
    """Tests for the get_categories function."""

    def test_get_root_categories(self):
        result = utils.get_categories(BASE_PATH)

        info = PARSED_CATEGORY_INFO
        categories = {
            "category": info,
            "tmp": info,
            "not_a_page.md": info,
        }
        self.assertEqual(result, categories)

    def test_get_categories_with_subcategories(self):
        result = utils.get_categories(Path(BASE_PATH, "category"))

        self.assertEqual(result, {"subcategory": PARSED_CATEGORY_INFO})

    def test_get_categories_without_subcategories(self):
        result = utils.get_categories(Path(BASE_PATH, "category/subcategory"))

        self.assertEqual(result, {})


class GetCategoryPagesTests(MockPagesTestCase):
    """Tests for the get_category_pages function."""

    def test_get_pages_in_root_category_successfully(self):
        """The method should successfully retrieve page metadata."""
        root_category_pages = utils.get_category_pages(BASE_PATH)
        self.assertEqual(
            root_category_pages, {"root": PARSED_METADATA, "root_without_metadata": {}}
        )

    def test_get_pages_in_subcategories_successfully(self):
        """The method should successfully retrieve page metadata."""
        category_pages = utils.get_category_pages(Path(BASE_PATH, "category"))

        # Page metadata is properly retrieved
        self.assertEqual(category_pages, {"with_metadata": PARSED_METADATA})


class GetPageTests(MockPagesTestCase):
    """Tests for the get_page function."""

    def test_get_page(self):
        # TOC is a special case because the markdown converter outputs the TOC as HTML
        updated_metadata = {**PARSED_METADATA, "toc": '<div class="toc">\n<ul></ul>\n</div>\n'}
        cases = [
            ("Root page with metadata", "root.md", PARSED_HTML, updated_metadata),
            ("Root page without metadata", "root_without_metadata.md", PARSED_HTML, {}),
            ("Page with metadata", "category/with_metadata.md", PARSED_HTML, updated_metadata),
            ("Page without metadata", "category/subcategory/without_metadata.md", PARSED_HTML, {}),
        ]

        for msg, page_path, expected_html, expected_metadata in cases:
            with self.subTest(msg=msg):
                html, metadata = utils.get_page(Path(BASE_PATH, page_path))
                self.assertEqual(html, expected_html)
                self.assertEqual(metadata, expected_metadata)

    def test_get_nonexistent_page_returns_404(self):
        with self.assertRaises(Http404):
            utils.get_page(Path(BASE_PATH, "invalid"))
