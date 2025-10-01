"""Google search automation package."""

from .models import SearchResult
from .searcher import GoogleSearcher

__all__ = ["GoogleSearcher", "SearchResult"]
