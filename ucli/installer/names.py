"""Helpers for deriving MCP server names from install specs."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import unquote, urlparse


@dataclass(frozen=True)
class InstallSpec:
    """Resolved names for a user-provided install spec."""

    raw: str
    local_name: str
    lookup_names: tuple[str, ...]


def resolve_install_spec(server_spec: str) -> InstallSpec:
    """Resolve a user install spec into local and lookup names."""
    raw = server_spec.strip()
    if not raw:
        return InstallSpec(raw=raw, local_name=raw, lookup_names=())

    path = _path_from_spec(raw)
    segments = _path_segments(path)
    path_name = "/".join(segments)
    local_name = (segments[-1] if segments else raw).removesuffix(".git")

    lookup_names: list[str] = []
    _append_unique(lookup_names, raw)
    if path_name and path_name != raw:
        _append_unique(lookup_names, path_name)
    if len(segments) >= 2:
        _append_unique(lookup_names, "-".join(segments[-2:]))
    _append_unique(lookup_names, local_name)

    return InstallSpec(
        raw=raw,
        local_name=local_name,
        lookup_names=tuple(lookup_names),
    )


def _path_from_spec(spec: str) -> str:
    if spec.startswith("git@"):
        return spec.partition(":")[2]

    parsed = urlparse(spec)
    if parsed.scheme and parsed.netloc:
        return parsed.path

    return spec


def _path_segments(path: str) -> list[str]:
    cleaned = unquote(path).split("?", 1)[0].split("#", 1)[0].strip("/")
    if not cleaned:
        return []
    return [part.removesuffix(".git") for part in cleaned.split("/") if part]


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)
