"""
ICA Langflow Adapter
====================
Calls the IBM Consulting Advantage Langflow workflow API directly.

Auth: x-api-key header (from MCP server configuration).
URL:  https://langflow.servicesessentials.ibm.com/api/v1/run/<workflow-id>

Environment variables
---------------------
  ICA_WORKFLOW_URL   Required. Full run URL ending in /api/v1/run/<workflow-id>
  ICA_API_KEY        Required. Value of x-api-key from MCP server config.

Usage
-----
    adapter = ICAAdapter()
    answer  = await adapter.call("Which instances are idle?", "aws")
"""

import json
import logging
import os
from typing import Any

import httpx
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ---------------------------------------------------------------------------
# Cloud-provider context suffixes
# ---------------------------------------------------------------------------

_CLOUD_CONTEXT: dict[str, str] = {
    "all":   "Analyze across AWS, Azure and GCP.",
    "aws":   "Focus on Amazon Web Services only.",
    "azure": "Focus on Microsoft Azure only.",
    "gcp":   "Focus on Google Cloud Platform only.",
}

VALID_CLOUD_PROVIDERS = frozenset(_CLOUD_CONTEXT.keys())

# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class ICAAdapterError(Exception):
    """Raised when the ICA Langflow API cannot be reached or returns an error."""


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------


class ICAAdapter:
    """
    Adapter for the ICA Langflow workflow API.

    Sends POST /api/v1/run/<workflow-id> with:
      - x-api-key header (from ICA_API_KEY)
      - JSON body: {input_value, output_type, input_type}
    """

    def __init__(self) -> None:
        self._workflow_url: str = self._require_env("ICA_WORKFLOW_URL")
        self._api_key: str      = self._require_env("ICA_API_KEY")

        logger.info("ICAAdapter initialised:")
        logger.info("  Workflow URL: %s", self._workflow_url)
        logger.info("  API key     : %s…", self._api_key[:12])

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def build_payload(self, question: str, cloud_provider: str) -> dict[str, Any]:
        """
        Build the Langflow chat payload with cloud-provider context appended.

        Args:
            question:       Raw question text from the user.
            cloud_provider: One of ``all | aws | azure | gcp``.

        Returns:
            Dict with keys ``input_value``, ``output_type``, ``input_type``.
        """
        provider       = cloud_provider.lower()
        context_suffix = _CLOUD_CONTEXT.get(provider, _CLOUD_CONTEXT["all"])
        enriched       = f"{question.strip()} {context_suffix}"
        return {
            "input_value": enriched,
            "output_type": "chat",
            "input_type":  "chat",
        }

    def extract_response(self, data: dict[str, Any]) -> str:
        """
        Extract the AI response text from the Langflow API response body.

        Primary path:  outputs[0].outputs[0].results.message.text
        Fallback 1:    outputs[0].outputs[0].messages[0].message
        Fallback 2:    outputs[0].outputs[0].artifacts.message
        Fallback 3:    raw JSON dump (always succeeds)

        Logs WARNING on every failed extraction path.
        """
        # Primary
        try:
            text = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            if isinstance(text, str) and text.strip():
                logger.info("Extracted via PRIMARY path.")
                return text
            raise ValueError("empty")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            logger.warning("PRIMARY extraction failed: %s", exc)

        # Fallback 1
        try:
            text = data["outputs"][0]["outputs"][0]["messages"][0]["message"]
            if isinstance(text, str) and text.strip():
                logger.warning("Extracted via FALLBACK1.")
                return text
            raise ValueError("empty")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            logger.warning("FALLBACK1 extraction failed: %s", exc)

        # Fallback 2
        try:
            text = data["outputs"][0]["outputs"][0]["artifacts"]["message"]
            if isinstance(text, str) and text.strip():
                logger.warning("Extracted via FALLBACK2.")
                return text
            raise ValueError("empty")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            logger.warning("FALLBACK2 extraction failed: %s", exc)

        # Fallback 3: raw dump
        raw = json.dumps(data, indent=2, default=str)
        logger.warning("All extraction paths failed — returning raw dump.")
        return raw

    async def call(self, question: str, cloud_provider: str) -> str:
        """
        POST the question to the Langflow run endpoint and return the answer.

        Raises:
            ICAAdapterError: On 3xx redirect, non-2xx status, or invalid JSON.
        """
        payload = self.build_payload(question, cloud_provider)
        headers = {
            "x-api-key":      self._api_key,
            "Content-Type":   "application/json",
            "Accept":         "application/json",
        }

        logger.info(
            "Calling Langflow API — cloud=%s url=%s",
            cloud_provider, self._workflow_url,
        )
        logger.info("Payload input_value: %s", payload["input_value"][:120])

        async with httpx.AsyncClient(timeout=120.0, follow_redirects=False) as client:
            response = await client.post(
                self._workflow_url,
                headers=headers,
                json=payload,
            )

        status = response.status_code
        logger.info("HTTP %s", status)

        # Redirect = auth rejected
        if 300 <= status < 400:
            location = response.headers.get("location", "")
            logger.error("Redirected to: %s", location)
            raise ICAAdapterError(
                f"Request redirected (HTTP {status}) — API key may be wrong or expired.\n"
                f"Location: {location}\n"
                f"Check ICA_API_KEY in webapp/backend/.env"
            )

        # Non-2xx error
        if not response.is_success:
            logger.error("HTTP %s body: %s", status, response.text[:500])
            raise ICAAdapterError(
                f"Langflow API returned HTTP {status}: {response.text[:300]}"
            )

        # Parse JSON
        try:
            data: dict[str, Any] = response.json()
        except Exception as exc:
            raise ICAAdapterError(
                f"Langflow API response is not valid JSON: {exc}"
            ) from exc

        return self.extract_response(data)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _require_env(name: str) -> str:
        """Read a required environment variable; raise clearly if missing."""
        value = os.getenv(name, "").strip()
        if not value:
            raise EnvironmentError(
                f"Required environment variable '{name}' is not set. "
                f"Copy webapp/backend/.env.example to webapp/backend/.env "
                f"and fill in the value."
            )
        return value
