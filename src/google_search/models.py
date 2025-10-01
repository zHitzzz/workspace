"""Data models for Google search results."""

from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a single search result entry."""

    title: str
    description: str
