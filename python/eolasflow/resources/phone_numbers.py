"""Phone Numbers resource — list available numbers."""

from __future__ import annotations
from typing import List, Dict, Any, TYPE_CHECKING

from ..models import PhoneNumber

if TYPE_CHECKING:
    from .._http import HttpClient


class PhoneNumbers:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(self) -> List[PhoneNumber]:
        """List all phone numbers on the account."""
        data = self._http.get("/phone-numbers")
        numbers = data.get("phone_numbers", [])
        return [PhoneNumber(**n) for n in numbers]
