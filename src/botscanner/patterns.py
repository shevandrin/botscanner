# patterns.py
from __future__ import annotations

import os
import yaml
from dataclasses import dataclass
from importlib import resources
from typing import Any, Dict, Optional, Tuple
from copy import deepcopy

# Cache keyed by (user_path, user_dict_hash)
_PATTERNS_CACHE: Dict[Tuple[Optional[str], Optional[int]], Dict[str, Any]] = {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge override into base.
    - dict + dict: merge keys
    - anything else: override replaces base
    """
    out = deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = deepcopy(v)
    return out


def _load_yaml_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping (dict), got {type(data)}")
    return data


def _load_default_patterns() -> Dict[str, Any]:
    patterns_file_path = resources.files("botscanner.data").joinpath("patterns.yaml")
    with patterns_file_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Default patterns.yaml root must be a dict, got {type(data)}")
    return data


def load_patterns(
    user_yaml_path: Optional[str] = None,
    user_patterns: Optional[Dict[str, Any]] = None,
    *,
    use_cache: bool = True,
) -> Dict[str, Any]:
    """
    Load default patterns and optionally merge user-defined patterns.

    Precedence (highest wins):
      user_patterns (dict) > user_yaml_path (file) > package defaults
    """
    user_yaml_path = os.path.expanduser(user_yaml_path) if user_yaml_path else None
    user_dict_key = hash(repr(user_patterns)) if user_patterns is not None else None
    cache_key = (user_yaml_path, user_dict_key)

    if use_cache and cache_key in _PATTERNS_CACHE:
        return _PATTERNS_CACHE[cache_key]

    defaults = _load_default_patterns()
    merged = defaults

    if user_yaml_path:
        user_from_file = _load_yaml_file(user_yaml_path)
        merged = _deep_merge(merged, user_from_file)

    if user_patterns:
        merged = _deep_merge(merged, user_patterns)

    _PATTERNS_CACHE[cache_key] = merged
    return merged

def get_cookie_patterns(patterns: Dict[str, Any]) -> Dict[str, Any]:
    return patterns.get("detection", {}).get("cookie_consent", {})

def get_core_anchors_patterns(patterns: Dict[str, Any]) -> Dict[str, Any]:
    return patterns.get("detection", {}).get("core_anchors", {})

def get_chatbot_frameworks_patterns(patterns: Dict[str, Any]) -> Dict[str, Any]:
    return patterns.get("detection", {}).get("chatbot_frameworks", {})

def get_chatbot_windows_shadow_dom_patterns(patterns: Dict[str, Any]) -> Dict[str, Any]:
    return patterns.get("detection", {}).get("shadow_dom_indicators", {})

def get_chatbot_windows_hooks_patterns(patterns: Dict[str, Any]) -> Dict[str, Any]:
    return patterns.get("detection", {}).get("window_indicators", {})



#PATTERNS = load_patterns()
#COOKIE_PATTERNS = PATTERNS.get('detection', {}).get('cookie_consent', {})
#CORE_ANCHORS_PATTERNS = PATTERNS.get('detection', {}).get('core_anchors', {})
#CHATBOT_FRAMEWORKS_PATTERNS = PATTERNS.get('detection', {}).get('chatbot_frameworks', {})

#CHATBOT_WINDOWS_SHADOW_DOM_PATTERNS = PATTERNS.get('detection', {}).get('shadow_dom_indicators', {})
#CHATBOT_WINDOWS_HOOKS_PATTERNS = PATTERNS.get('detection', {}).get('window_indicators', {})