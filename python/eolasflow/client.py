"""EolasFlow client — main entry point for the SDK."""

from __future__ import annotations

from ._http import HttpClient, AsyncHttpClient
from .resources import Calls, Contacts, VoiceFlows, Webhooks, PhoneNumbers


class EolasFlow:
    """
    EolasFlow API client.

    Usage:
        client = EolasFlow(api_key="your-api-key")
        calls = client.calls.list()
        contact = client.contacts.create(name="John", phone="+353851234567")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.eolasflow.ai",
        timeout: float = 30.0,
    ):
        """
        Initialize the EolasFlow client.

        Args:
            api_key: Your API key from the EolasFlow Dashboard
            base_url: API base URL (default: https://api.eolasflow.ai)
            timeout: Request timeout in seconds (default: 30)
        """
        self._http = HttpClient(api_key=api_key, base_url=base_url, timeout=timeout)

        self.calls = Calls(self._http)
        self.contacts = Contacts(self._http)
        self.voiceflows = VoiceFlows(self._http)
        self.webhooks = Webhooks(self._http)
        self.phone_numbers = PhoneNumbers(self._http)

    def close(self):
        """Close the HTTP client connection."""
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class AsyncEolasFlow:
    """
    Async EolasFlow API client.

    Usage:
        async with AsyncEolasFlow(api_key="your-api-key") as client:
            calls = await client.calls.list()
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.eolasflow.ai",
        timeout: float = 30.0,
    ):
        self._http = AsyncHttpClient(api_key=api_key, base_url=base_url, timeout=timeout)

        # Async resources use the same classes — the http client handles async
        self.calls = Calls(self._http)
        self.contacts = Contacts(self._http)
        self.voiceflows = VoiceFlows(self._http)
        self.webhooks = Webhooks(self._http)
        self.phone_numbers = PhoneNumbers(self._http)

    async def close(self):
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
