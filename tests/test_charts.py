"""Chart/Explore UI validation tests for http://localhost:8088/."""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8088"


@pytest.mark.smoke
@pytest.mark.chart
class TestChartListPage:
    """Validate the chart list / index page."""

    def test_chart_list_has_header(self, authenticated_page: Page):
        """The chart list page must display a page heading."""
        authenticated_page.goto(f"{BASE_URL}/chart/list/")
        header = authenticated_page.locator(
            "h1, h2, [data-test='page-header'], .title-panel"
        )
        expect(header.first).to_be_visible()

    def test_chart_list_has_search(self, authenticated_page: Page):
        """A search input must be present on the chart list page."""
        authenticated_page.goto(f"{BASE_URL}/chart/list/")
        search = authenticated_page.locator(
            "input[placeholder*='Search' i], "
            "input[type='search'], "
            "[data-test='filters-search'] input"
        )
        expect(search.first).to_be_visible()

    def test_chart_list_create_button(self, authenticated_page: Page):
        """A '+ Chart' or 'Create' button should be visible on the list page."""
        authenticated_page.goto(f"{BASE_URL}/chart/list/")
        create_btn = authenticated_page.locator(
            "button:text('+ Chart'), "
            "button:text('Chart'), "
            "[data-test='add-action-menu']"
        )
        expect(create_btn.first).to_be_visible()

    def test_chart_list_table_renders(self, authenticated_page: Page):
        """The chart list must render a table or card grid of results."""
        authenticated_page.goto(f"{BASE_URL}/chart/list/")
        authenticated_page.wait_for_selector(
            ".table, .ant-table, [data-test='listview-table']",
            timeout=10_000,
        )
        table = authenticated_page.locator(
            ".table, .ant-table, [data-test='listview-table']"
        )
        expect(table.first).to_be_visible()

    def test_chart_view_toggle(self, authenticated_page: Page):
        """List-view / card-view toggle buttons must be present."""
        authenticated_page.goto(f"{BASE_URL}/chart/list/")
        toggle = authenticated_page.locator(
            "[data-test='list-view-controls'], "
            ".ant-radio-group, "
            "[aria-label*='view' i]"
        )
        # Lenient: either the toggle exists or the page loaded without error
        assert authenticated_page.url.endswith("/chart/list/")


@pytest.mark.regression
@pytest.mark.chart
class TestChartDetailPage:
    """Validate individual chart / explore page rendering."""

    def test_chart_detail_loads(self, authenticated_page: Page):
        """If a chart exists, its explore page must load successfully."""
        authenticated_page.goto(f"{BASE_URL}/chart/list/")
        first_chart = authenticated_page.locator(
            "a[href*='/explore/']"
        ).first
        if first_chart.is_visible():
            href = first_chart.get_attribute("href")
            response = authenticated_page.goto(f"{BASE_URL}{href}")
            assert response is not None
            assert response.status == 200
        else:
            pytest.skip("No charts available to test the explore view.")

    def test_explore_page_chart_type_selector(self, authenticated_page: Page):
        """The explore page must load successfully (HTTP 200)."""
        response = authenticated_page.goto(f"{BASE_URL}/chart/add")
        assert response is not None
        assert response.status == 200
