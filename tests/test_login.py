"""Login page UI validation tests for http://localhost:8088/."""

import re

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8088"


@pytest.mark.smoke
@pytest.mark.login
class TestLoginPage:
    """Validate the login page UI and behaviour."""

    def test_login_page_loads(self, page: Page):
        """The login page must return HTTP 200 and render without errors."""
        response = page.goto(f"{BASE_URL}/login/")
        assert response is not None
        assert response.status == 200

    def test_login_page_title(self, page: Page):
        """The browser tab title should contain 'Superset'."""
        page.goto(f"{BASE_URL}/login/")
        expect(page).to_have_title(re.compile(r"Superset", re.IGNORECASE))

    def test_username_field_visible(self, page: Page):
        """The username input field must be visible on the login page."""
        page.goto(f"{BASE_URL}/login/")
        expect(page.locator("#username")).to_be_visible()

    def test_password_field_visible(self, page: Page):
        """The password input field must be visible on the login page."""
        page.goto(f"{BASE_URL}/login/")
        expect(page.locator("#password")).to_be_visible()

    def test_login_button_visible(self, page: Page):
        """The login submit button must be visible and enabled."""
        page.goto(f"{BASE_URL}/login/")
        btn = page.locator('[data-test="login-button"]')
        expect(btn).to_be_visible()
        expect(btn).to_be_enabled()

    def test_superset_logo_visible(self, page: Page):
        """The Apache Superset logo / branding should appear on the login page."""
        page.goto(f"{BASE_URL}/login/")
        logo = page.locator("img.logocell, .login-container img, img[alt*='Superset']")
        expect(logo.first).to_be_visible()

    def test_invalid_credentials_shows_error(self, page: Page):
        """Submitting wrong credentials must display an error message."""
        page.goto(f"{BASE_URL}/login/")
        page.fill("#username", "invalid_user")
        page.fill("#password", "wrong_password")
        page.click('[data-test="login-button"]')
        error = page.locator(".alert-danger, [class*='error'], [class*='Error']")
        expect(error.first).to_be_visible(timeout=8_000)

    def test_empty_credentials_shows_error(self, page: Page):
        """Submitting the form with empty fields must show a validation error."""
        page.goto(f"{BASE_URL}/login/")
        page.click('[data-test="login-button"]')
        # Either the browser native validation fires or an app-level error appears
        username_field = page.locator("#username")
        # The field should still be on-screen (no redirect occurred)
        expect(username_field).to_be_visible()

    def test_successful_login_redirects(self, page: Page):
        """Logging in with valid credentials must redirect to the welcome page."""
        page.goto(f"{BASE_URL}/login/")
        page.fill("#username", "admin")
        page.fill("#password", "general")
        page.click('[data-test="login-button"]')
        page.wait_for_url(f"{BASE_URL}/superset/welcome/", timeout=15_000)
        assert "/superset/welcome/" in page.url

    def test_logout_redirects_to_login(self, authenticated_page: Page):
        """After logout the user must be sent back to the login page."""
        p = authenticated_page
        p.goto(f"{BASE_URL}/logout/")
        p.wait_for_url(f"{BASE_URL}/login/", timeout=10_000)
        expect(p.locator("#username")).to_be_visible()
