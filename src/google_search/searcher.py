"""Utilities for automating Google searches using Playwright."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from .models import SearchResult


@dataclass
class SearchConfig:
    """Configuration for Google search execution."""

    keyword: str
    total_results: int


class GoogleSearcher:
    """Performs Google searches and returns structured results."""

    SEARCH_URL = "https://www.google.com/ncr"

    def __init__(self, playwright: Playwright | None = None) -> None:
        self._playwright = playwright
        self._browser: Browser | None = None

    def __enter__(self) -> "GoogleSearcher":
        self.start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.stop()

    def start(self) -> None:
        """Starts the Playwright browser if it is not already running."""

        if self._playwright is None:
            self._playwright = sync_playwright().start()
        if self._browser is None:
            self._browser = self._playwright.chromium.launch(headless=True)

    def stop(self) -> None:
        """Closes the Playwright browser and stops Playwright."""

        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None

    def search(self, config: SearchConfig) -> List[SearchResult]:
        """Searches Google and returns a list of search results."""

        if self._browser is None:
            self.start()

        assert self._browser is not None  # for type checkers

        page = self._browser.new_page()
        page.goto(self.SEARCH_URL)
        self._accept_consent_if_present(page)
        self._perform_search(page, config.keyword)

        results: List[SearchResult] = []
        while len(results) < config.total_results:
            results.extend(self._collect_results(page))
            if len(results) >= config.total_results:
                break
            if not self._go_to_next_page(page):
                break

        page.close()
        return results[: config.total_results]

    def _perform_search(self, page: Page, keyword: str) -> None:
        search_box_selector = "textarea[name='q']"
        page.fill(search_box_selector, keyword)
        page.keyboard.press("Enter")
        page.wait_for_selector("div#search")

    def _collect_results(self, page: Page) -> List[SearchResult]:
        result_elements = page.query_selector_all("div#search div.g")
        results: List[SearchResult] = []
        for element in result_elements:
            title = element.query_selector("h3")
            description = element.query_selector("div.VwiC3b")
            if title is None or description is None:
                continue
            title_text = title.inner_text().strip()
            description_text = description.inner_text().strip()
            if title_text and description_text:
                results.append(
                    SearchResult(title=title_text, description=description_text)
                )
        return results

    def _go_to_next_page(self, page: Page) -> bool:
        next_button = page.query_selector("a#pnnext")
        if next_button is None:
            return False
        next_button.click()
        page.wait_for_load_state("networkidle")
        return True

    def _accept_consent_if_present(self, page: Page) -> None:
        consent_button_selectors: Iterable[str] = (
            "button#L2AGLb",
            "form[action*='consent'] button",
        )
        for selector in consent_button_selectors:
            button = page.query_selector(selector)
            if button is not None:
                button.click()
                page.wait_for_load_state("networkidle")
                break
