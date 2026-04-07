"""Contacts resource — CRUD operations for contacts/customers."""

from __future__ import annotations
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from ..models import Contact

if TYPE_CHECKING:
    from .._http import HttpClient


class Contacts:
    def __init__(self, http: HttpClient):
        self._http = http

    def create(
        self,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        status: str = "lead",
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Contact:
        """Create a new contact."""
        body: Dict[str, Any] = {"name": name}
        if phone:
            body["phone_number"] = phone
        if email:
            body["email"] = email
        if company:
            body["company"] = company
        if status != "lead":
            body["status"] = status
        if tags:
            body["tags"] = tags
        if notes:
            body["notes"] = notes
        if custom_fields:
            body["custom_fields"] = custom_fields

        data = self._http.post("/customers", json=body)
        return Contact(**data)

    def get(self, contact_id: str) -> Contact:
        """Get a contact by ID."""
        data = self._http.get(f"/customers/{contact_id}")
        return Contact(**data)

    def find_by_phone(self, phone: str) -> Contact:
        """Look up a contact by phone number."""
        data = self._http.get(f"/customers/phone/{phone}")
        return Contact(**data)

    def list(
        self,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> List[Contact]:
        """List contacts with optional search."""
        params: Dict[str, Any] = {"page": page, "page_size": page_size}
        if search:
            params["search"] = search

        data = self._http.get("/customers", params=params)
        customers = data.get("customers", [])
        return [Contact(**c) for c in customers]

    def update(
        self,
        contact_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Contact:
        """Update a contact. Only provided fields are changed."""
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if phone is not None:
            body["phone_number"] = phone
        if email is not None:
            body["email"] = email
        if company is not None:
            body["company"] = company
        if status is not None:
            body["status"] = status
        if tags is not None:
            body["tags"] = tags
        if custom_fields is not None:
            body["custom_fields"] = custom_fields

        data = self._http.patch(f"/customers/{contact_id}", json=body)
        return Contact(**data)

    def delete(self, contact_id: str) -> Dict[str, Any]:
        """Delete a contact permanently."""
        return self._http.delete(f"/customers/{contact_id}")

    def bulk_import(self, contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Import multiple contacts at once. Duplicates are skipped."""
        return self._http.post("/customers/bulk", json={"contacts": contacts})
