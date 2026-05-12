"""AI Agent Interview Assistant backend package."""

from __future__ import annotations

import os


def _prefer_certifi_ssl_bundle() -> None:
    """Use certifi's CA bundle when the env does not override it.

    Avoids TLS failures (e.g. macOS Python.org builds) when optional
    dependencies download assets at runtime.
    """
    try:
        import certifi
    except ImportError:
        return
    ca = certifi.where()
    if not os.environ.get("SSL_CERT_FILE"):
        os.environ["SSL_CERT_FILE"] = ca
    if not os.environ.get("REQUESTS_CA_BUNDLE"):
        os.environ["REQUESTS_CA_BUNDLE"] = ca


_prefer_certifi_ssl_bundle()

