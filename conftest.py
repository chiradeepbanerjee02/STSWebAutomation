import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

BASE_URL = "http://localhost:8088"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "general"


@pytest.fixture(scope="session")
def browser_instance():
    """Launch a single browser for the entire test session."""
    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser_instance: Browser):
    """Create a fresh browser context for each test."""
    ctx: BrowserContext = browser_instance.new_context(
        base_url=BASE_URL,
        viewport={"width": 1280, "height": 800},
    )
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Open a new page in the current context."""
    p: Page = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def authenticated_page(context: BrowserContext) -> Page:
    """Open a page and log in as admin before the test."""
    p: Page = context.new_page()
    p.goto(f"{BASE_URL}/login/")
    p.fill("#username", ADMIN_USERNAME)
    p.fill("#password", ADMIN_PASSWORD)
    p.click('[data-test="login-button"]')
    p.wait_for_url(f"{BASE_URL}/superset/welcome/", timeout=15_000)
    yield p
    p.close()
