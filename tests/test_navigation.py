"""Navigation UI validation tests for http://localhost:8088/."""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8088"


@pytest.mark.smoke
@pytest.mark.navigation
class TestTopNavigation:
    """Validate the top navigation bar visible after authentication."""

    def test_navbar_is_visible(self, authenticated_page: Page):
        """The top navigation bar must render after login."""
        nav = authenticated_page.locator(".navbar, [data-test='navbar-top']")
        expect(nav.first).to_be_visible()

    def test_home_link_present(self, authenticated_page: Page):
        """The Home (Superset logo) navigation link must be present."""
        home = authenticated_page.locator(
            "a[href='/superset/welcome/'], a[href='/'], .navbar-brand"
        )
        expect(home.first).to_be_visible()

    def test_dashboards_menu_item(self, authenticated_page: Page):
        """A 'Dashboards' link or menu item must appear in the top bar."""
        dashboards = authenticated_page.locator(
            "a[href*='/dashboard/'], [data-test='navbar-top'] *:text('Dashboards')"
        )
        expect(dashboards.first).to_be_visible()

    def test_charts_menu_item(self, authenticated_page: Page):
        """A 'Charts' link or menu item must appear in the top bar."""
        charts = authenticated_page.locator(
            "a[href*='/chart/'], [data-test='navbar-top'] *:text('Charts')"
        )
        expect(charts.first).to_be_visible()

    def test_datasets_menu_item(self, authenticated_page: Page):
        """A 'Datasets' link or menu item must appear in the top bar."""
        datasets = authenticated_page.locator(
            "a[href*='/tablemodelview/'], "
            "[data-test='navbar-top'] *:text('Datasets'), "
            "*:text('Datasets')"
        )
        expect(datasets.first).to_be_visible()

    def test_settings_menu_item(self, authenticated_page: Page):
        """A 'Settings' or gear-icon menu entry must appear in the top bar."""
        settings = authenticated_page.locator(
            "[data-test='settings-menu'], *:text('Settings'), "
            "a[href*='/users/'], .anticon-setting"
        )
        expect(settings.first).to_be_visible()

    def test_user_menu_visible(self, authenticated_page: Page):
        """The logged-in user avatar / menu must be present in the top bar."""
        user_menu = authenticated_page.locator(
            "[data-test='user-menu'], .navbar-right .dropdown, "
            ".ant-avatar, [aria-label*='user' i]"
        )
        expect(user_menu.first).to_be_visible()


@pytest.mark.regression
@pytest.mark.navigation
class TestSideNavigation:
    """Validate sidebar or secondary navigation elements."""

    def test_welcome_page_loads(self, authenticated_page: Page):
        """The welcome / home page must load successfully after login."""
        response = authenticated_page.goto(f"{BASE_URL}/superset/welcome/")
        assert response is not None
        assert response.status == 200

    def test_dashboard_list_page_loads(self, authenticated_page: Page):
        """The /dashboard/list/ page must return HTTP 200."""
        response = authenticated_page.goto(f"{BASE_URL}/dashboard/list/")
        assert response is not None
        assert response.status == 200

    def test_chart_list_page_loads(self, authenticated_page: Page):
        """The /chart/list/ page must return HTTP 200."""
        response = authenticated_page.goto(f"{BASE_URL}/chart/list/")
        assert response is not None
        assert response.status == 200

    def test_dataset_list_page_loads(self, authenticated_page: Page):
        """The /tablemodelview/list/ page must return HTTP 200."""
        response = authenticated_page.goto(f"{BASE_URL}/tablemodelview/list/")
        assert response is not None
        assert response.status == 200
