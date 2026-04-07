"""EolasFlow Python SDK — Official client for the EolasFlow Voice AI API."""

from .client import EolasFlow
from .models import (
    Call,
    CallTranscript,
    CallAnalysis,
    CallRecording,
    Contact,
    VoiceFlow,
    VoiceFlowStats,
    Webhook,
    PhoneNumber,
)
from .exceptions import (
    EolasFlowError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "EolasFlow",
    "Call",
    "CallTranscript",
    "CallAnalysis",
    "CallRecording",
    "Contact",
    "VoiceFlow",
    "VoiceFlowStats",
    "Webhook",
    "PhoneNumber",
    "EolasFlowError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
]
