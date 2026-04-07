"""HTTP client wrapper for EolasFlow API."""

from __future__ import annotations
from typing import Any, Dict, Optional

import httpx

from .exceptions import (
    EolasFlowError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    PlanLimitError,
)


class HttpClient:
    """Low-level HTTP client for the EolasFlow API Gateway."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.eolasflow.ai",
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/") + "/api/external/v1"
        self._client = httpx.Client(
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "eolasflow-python/0.1.0",
            },
            timeout=timeout,
            follow_redirects=True,
        )

    def _handle_response(self, response: httpx.Response) -> Any:
        """Parse response and raise appropriate exceptions."""
        if response.status_code in (200, 201):
            return response.json()
        if response.status_code == 204:
            return {"success": True}

        # Try to get error detail from response body
        try:
            body = response.json()
            detail = body.get("detail", body.get("error", str(body)))
        except Exception:
            detail = response.text or f"HTTP {response.status_code}"

        if response.status_code == 401:
            raise AuthenticationError(detail, status_code=401)
        elif response.status_code == 403:
            if "plan limit" in detail.lower() or "upgrade" in detail.lower():
                raise PlanLimitError(detail, status_code=403)
            raise AuthenticationError(detail, status_code=403)
        elif response.status_code == 404:
            raise NotFoundError(detail, status_code=404)
        elif response.status_code == 422:
            raise ValidationError(detail, status_code=422)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                detail,
                status_code=429,
                retry_after=int(retry_after) if retry_after else None,
            )
        else:
            raise EolasFlowError(detail, status_code=response.status_code)

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        response = self._client.get(f"{self.base_url}{path}", params=params)
        return self._handle_response(response)

    def post(self, path: str, json: Optional[Dict] = None) -> Any:
        response = self._client.post(f"{self.base_url}{path}", json=json or {})
        return self._handle_response(response)

    def patch(self, path: str, json: Optional[Dict] = None) -> Any:
        response = self._client.patch(f"{self.base_url}{path}", json=json or {})
        return self._handle_response(response)

    def delete(self, path: str) -> Any:
        response = self._client.delete(f"{self.base_url}{path}")
        return self._handle_response(response)

    def close(self):
        self._client.close()


class AsyncHttpClient:
    """Async HTTP client for the EolasFlow API Gateway."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.eolasflow.ai",
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/") + "/api/external/v1"
        self._client = httpx.AsyncClient(
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "eolasflow-python/0.1.0",
            },
            timeout=timeout,
            follow_redirects=True,
        )

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.status_code in (200, 201):
            return response.json()
        if response.status_code == 204:
            return {"success": True}

        try:
            body = response.json()
            detail = body.get("detail", body.get("error", str(body)))
        except Exception:
            detail = response.text or f"HTTP {response.status_code}"

        if response.status_code == 401:
            raise AuthenticationError(detail, status_code=401)
        elif response.status_code == 403:
            if "plan limit" in detail.lower() or "upgrade" in detail.lower():
                raise PlanLimitError(detail, status_code=403)
            raise AuthenticationError(detail, status_code=403)
        elif response.status_code == 404:
            raise NotFoundError(detail, status_code=404)
        elif response.status_code == 422:
            raise ValidationError(detail, status_code=422)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                detail,
                status_code=429,
                retry_after=int(retry_after) if retry_after else None,
            )
        else:
            raise EolasFlowError(detail, status_code=response.status_code)

    async def get(self, path: str, params: Optional[Dict] = None) -> Any:
        response = await self._client.get(f"{self.base_url}{path}", params=params)
        return self._handle_response(response)

    async def post(self, path: str, json: Optional[Dict] = None) -> Any:
        response = await self._client.post(f"{self.base_url}{path}", json=json or {})
        return self._handle_response(response)

    async def patch(self, path: str, json: Optional[Dict] = None) -> Any:
        response = await self._client.patch(f"{self.base_url}{path}", json=json or {})
        return self._handle_response(response)

    async def delete(self, path: str) -> Any:
        response = await self._client.delete(f"{self.base_url}{path}")
        return self._handle_response(response)

    async def close(self):
        await self._client.aclose()
