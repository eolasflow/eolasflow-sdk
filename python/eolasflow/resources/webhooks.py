"""Webhooks resource — manage webhook subscriptions."""

from __future__ import annotations
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from ..models import Webhook

if TYPE_CHECKING:
    from .._http import HttpClient


class Webhooks:
    def __init__(self, http: HttpClient):
        self._http = http

    def create(
        self,
        url: str,
        events: List[str],
        description: Optional[str] = None,
    ) -> Webhook:
        """
        Create a webhook subscription.

        Args:
            url: Endpoint URL to receive events
            events: Event types — "call.completed", "call.started", "agent.event"
            description: Optional description
        """
        body: Dict[str, Any] = {"url": url, "events": events}
        if description:
            body["description"] = description

        data = self._http.post("/webhooks", json=body)
        return Webhook(**data)

    def list(self) -> List[Webhook]:
        """List all webhook subscriptions."""
        data = self._http.get("/webhooks")
        webhooks = data.get("webhooks", data) if isinstance(data, dict) else data
        if isinstance(webhooks, list):
            return [Webhook(**w) for w in webhooks]
        return []

    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook subscription."""
        return self._http.delete(f"/webhooks/{webhook_id}")
