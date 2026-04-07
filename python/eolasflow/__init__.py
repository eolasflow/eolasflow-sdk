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
from .webhook_utils import verify_signature

__version__ = "0.1.0"
__all__ = [
    "EolasFlow",
    "verify_signature",
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
