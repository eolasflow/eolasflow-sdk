"""Calls resource — initiate calls, get transcripts, recordings, analysis."""

from __future__ import annotations
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from ..models import Call, CallTranscript, CallAnalysis, CallRecording

if TYPE_CHECKING:
    from .._http import HttpClient


class Calls:
    def __init__(self, http: HttpClient):
        self._http = http

    def create(
        self,
        to_number: str,
        from_number: str,
        voiceflow_id: str,
        customer_data: Optional[Dict[str, Any]] = None,
        priority: str = "normal",
        schedule_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Initiate an outbound AI voice call.

        Args:
            to_number: Phone number to call (E.164 format)
            from_number: Caller ID phone number
            voiceflow_id: VoiceFlow to use for the conversation
            customer_data: Optional context passed to the AI agent
            priority: Call priority — "high", "normal", "low"
            schedule_at: ISO datetime to schedule call (omit for immediate)

        Returns:
            Call initiation result with call_sid
        """
        body = {
            "to_number": to_number,
            "from_number": from_number,
            "campaign_id": voiceflow_id,
        }
        if customer_data:
            body["customer_data"] = customer_data
        if priority != "normal":
            body["priority"] = priority
        if schedule_at:
            body["schedule_at"] = schedule_at

        return self._http.post("/calls/initiate", json=body)

    def list(
        self,
        status: Optional[str] = None,
        voiceflow_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50,
        skip: int = 0,
    ) -> List[Call]:
        """List call records with optional filters."""
        params = {"limit": limit, "skip": skip}
        if status:
            params["status"] = status
        if voiceflow_id:
            params["campaign_id"] = voiceflow_id
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        data = self._http.get("/call-records", params=params)
        records = data.get("call_records", data.get("records", []))
        return [Call(**r) for r in records]

    def get(self, call_id: str) -> Call:
        """Get a single call record by ID."""
        data = self._http.get(f"/call-records/{call_id}")
        return Call(**data)

    def get_transcript(self, call_id: str) -> CallTranscript:
        """Get the full transcript for a call."""
        data = self._http.get(f"/call-records/{call_id}/transcript")
        return CallTranscript(call_id=call_id, **data)

    def get_analysis(self, call_id: str) -> CallAnalysis:
        """Get the AI analysis for a call."""
        data = self._http.get(f"/call-records/{call_id}/analysis")
        return CallAnalysis(call_id=call_id, **data)

    def get_recording(self, call_id: str) -> CallRecording:
        """Get the recording URL for a call."""
        data = self._http.get(f"/call-records/{call_id}/recording")
        return CallRecording(call_id=call_id, **data)
