"""
Models package for the Netflix Ads domain.

This package provides access to all domain models, schemas, enums, and utilities
through a centralized registry system.
"""

from __future__ import annotations

# Import only the registry system
from .registry import Registry, registry

# Export only the registry components
__all__ = [
    'Registry',
    'registry',
]
