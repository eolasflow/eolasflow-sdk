"""VoiceFlows resource — manage VoiceFlows (campaigns) and their contacts."""

from __future__ import annotations
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from ..models import VoiceFlow, VoiceFlowStats

if TYPE_CHECKING:
    from .._http import HttpClient


class VoiceFlows:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(
        self,
        status: Optional[str] = None,
        type: Optional[str] = None,
    ) -> List[VoiceFlow]:
        """List all VoiceFlows. Optionally filter by status or type."""
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        if type:
            params["campaign_type"] = type

        data = self._http.get("/campaigns", params=params)
        campaigns = data.get("campaigns", [])
        return [VoiceFlow(**c) for c in campaigns]

    def get(self, voiceflow_id: str) -> VoiceFlow:
        """Get a VoiceFlow by ID."""
        data = self._http.get(f"/campaigns/{voiceflow_id}")
        return VoiceFlow(**data)

    def get_stats(self, voiceflow_id: str) -> VoiceFlowStats:
        """Get call statistics for a VoiceFlow."""
        data = self._http.get(f"/campaigns/{voiceflow_id}/stats")
        return VoiceFlowStats(voiceflow_id=voiceflow_id, **data)

    def create(
        self,
        name: str,
        objective: Optional[str] = None,
        campaign_type: str = "inbound",
    ) -> VoiceFlow:
        """Create a new VoiceFlow."""
        body: Dict[str, Any] = {"name": name, "campaign_type": campaign_type}
        if objective:
            body["objective"] = objective

        data = self._http.post("/campaigns", json=body)
        return VoiceFlow(**data)

    def update(
        self,
        voiceflow_id: str,
        name: Optional[str] = None,
        objective: Optional[str] = None,
        status: Optional[str] = None,
    ) -> VoiceFlow:
        """Update a VoiceFlow."""
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if objective is not None:
            body["objective"] = objective
        if status is not None:
            body["status"] = status

        data = self._http.patch(f"/campaigns/{voiceflow_id}", json=body)
        return VoiceFlow(**data)

    def delete(self, voiceflow_id: str) -> Dict[str, Any]:
        """Delete a VoiceFlow."""
        return self._http.delete(f"/campaigns/{voiceflow_id}")

    def start(self, voiceflow_id: str) -> Dict[str, Any]:
        """Start/activate a VoiceFlow for outbound calling."""
        return self._http.post(f"/campaigns/{voiceflow_id}/start")

    def pause(self, voiceflow_id: str) -> Dict[str, Any]:
        """Pause a running VoiceFlow."""
        return self._http.post(f"/campaigns/{voiceflow_id}/pause")

    def add_contacts(
        self, voiceflow_id: str, contacts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Add contacts to a VoiceFlow for outbound calling."""
        return self._http.post(
            f"/campaigns/{voiceflow_id}/contacts/bulk",
            json={"contacts": contacts},
        )
