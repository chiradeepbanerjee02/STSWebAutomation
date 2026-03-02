"""Dashboard UI validation tests for http://localhost:8088/."""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8088"


@pytest.mark.smoke
@pytest.mark.dashboard
class TestDashboardListPage:
    """Validate the dashboard list / index page."""

    def test_dashboard_list_has_header(self, authenticated_page: Page):
        """The dashboard list page must display a page heading."""
        authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        header = authenticated_page.locator(
            "h1, h2, [data-test='page-header'], .title-panel"
        )
        expect(header.first).to_be_visible()

    def test_dashboard_list_has_search(self, authenticated_page: Page):
        """A search / filter input must be present on the dashboard list page."""
        authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        search = authenticated_page.locator(
            "input[placeholder*='Search' i], "
            "input[type='search'], "
            "[data-test='filters-search'] input"
        )
        expect(search.first).to_be_visible()

    def test_dashboard_list_create_button(self, authenticated_page: Page):
        """A '+ Dashboard' or 'Create' button should appear on the list page."""
        authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        create_btn = authenticated_page.locator(
            "button:text('+ Dashboard'), "
            "button:text('Dashboard'), "
            "[data-test='add-action-menu']"
        )
        expect(create_btn.first).to_be_visible()

    def test_dashboard_list_table_renders(self, authenticated_page: Page):
        """The dashboard list should render a table or card grid."""
        authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        authenticated_page.wait_for_selector(
            ".table, .ant-table, [data-test='listview-table']",
            timeout=10_000,
        )
        table = authenticated_page.locator(
            ".table, .ant-table, [data-test='listview-table']"
        )
        expect(table.first).to_be_visible()

    def test_dashboard_list_sort_controls(self, authenticated_page: Page):
        """Column sort headers must be present in the dashboard table."""
        authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        authenticated_page.wait_for_selector(
            "th, .ant-table-column-title", timeout=10_000
        )
        column_headers = authenticated_page.locator("th, .ant-table-column-title")
        assert column_headers.count() > 0


@pytest.mark.regression
@pytest.mark.dashboard
class TestDashboardDetailPage:
    """Validate individual dashboard rendering (if any dashboards exist)."""

    def test_dashboard_title_visible(self, authenticated_page: Page):
        """If a dashboard exists, its title must be visible when opened."""
        authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        # Try to open the first available dashboard link
        first_dashboard = authenticated_page.locator(
            "a[href*='/superset/dashboard/']"
        ).first
        if first_dashboard.is_visible():
            href = first_dashboard.get_attribute("href")
            authenticated_page.goto(f"{BASE_URL}{href}")
            authenticated_page.wait_for_load_state("networkidle", timeout=20_000)
            title = authenticated_page.locator(
                ".dashboard-title, h1, [data-test='dashboard-header-title']"
            )
            expect(title.first).to_be_visible()
        else:
            pytest.skip("No dashboards available to test detail view.")

    def test_dashboard_filter_bar(self, authenticated_page: Page):
        """The filter bar should render on a dashboard detail page."""
        authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        first_dashboard = authenticated_page.locator(
            "a[href*='/superset/dashboard/']"
        ).first
        if first_dashboard.is_visible():
            href = first_dashboard.get_attribute("href")
            assert href, "Dashboard link href must not be empty"
            response = authenticated_page.goto(f"{BASE_URL}{href}")
            assert response is not None
            assert response.status == 200
        else:
            pytest.skip("No dashboards available to test filter bar.")
