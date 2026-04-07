"""EolasFlow SDK data models."""

from __future__ import annotations
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# ─── Calls ───

class CallParticipant(BaseModel):
    number: str
    type: str  # "agent" | "customer"


class CallTiming(BaseModel):
    initiated_at: Optional[str] = None
    answered_at: Optional[str] = None
    ended_at: Optional[str] = None
    duration_seconds: Optional[int] = None
    ring_duration_seconds: Optional[int] = None
    talk_duration_seconds: Optional[int] = None


class Call(BaseModel):
    id: str
    call_sid: Optional[str] = None
    direction: str = "inbound"
    status: str = "unknown"
    outcome: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    duration: Optional[int] = None
    duration_seconds: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    campaign: Optional[Dict[str, Any]] = None
    contact: Optional[Dict[str, Any]] = None
    agent: Optional[Dict[str, Any]] = None
    # Flattened convenience fields
    campaign_id: Optional[str] = None
    campaign_name: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    created_at: Optional[str] = None

    def model_post_init(self, __context):
        # Flatten nested campaign/contact into convenience fields
        if self.campaign and not self.campaign_id:
            self.campaign_id = self.campaign.get("id")
            self.campaign_name = self.campaign.get("name")
        if self.contact and not self.customer_id:
            self.customer_id = self.contact.get("id")
            self.customer_name = self.contact.get("name")
        if self.duration and not self.duration_seconds:
            self.duration_seconds = self.duration


class TranscriptSegment(BaseModel):
    speaker: str
    text: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    sentiment: Optional[float] = None


class CallTranscript(BaseModel):
    call_id: str
    segments: List[TranscriptSegment] = []
    summary: Optional[str] = None
    full_text: Optional[str] = None


class CallAnalysis(BaseModel):
    call_id: str
    summary: Optional[str] = None
    sentiment_score: Optional[float] = None
    action_items: List[Dict[str, Any]] = []
    call_outcome: Optional[str] = None
    outcome_reason: Optional[str] = None
    quality_score: Optional[float] = None


class CallRecording(BaseModel):
    call_id: str
    recording_url: Optional[str] = None
    duration_seconds: Optional[int] = None


# ─── Contacts ───

class Contact(BaseModel):
    id: str
    name: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phone")
    email: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    tags: List[str] = []
    total_calls: int = 0
    last_call_date: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"populate_by_name": True}


# ─── VoiceFlows ───

class VoiceFlow(BaseModel):
    id: str
    name: str
    status: Optional[str] = None
    campaign_type: Optional[str] = None
    objective: Optional[str] = None
    total_contacts: int = 0
    completed_calls: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class VoiceFlowStats(BaseModel):
    voiceflow_id: str
    total_calls: int = 0
    completed_calls: int = 0
    success_rate: float = 0.0
    avg_duration_seconds: Optional[float] = None


# ─── Webhooks ───

class Webhook(BaseModel):
    id: str
    url: str
    events: List[str] = []
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


# ─── Phone Numbers ───

class PhoneNumber(BaseModel):
    id: str
    phone_number: str
    friendly_name: Optional[str] = None
    provider: Optional[str] = None
    status: Optional[str] = None
    country_code: Optional[str] = None
