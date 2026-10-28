from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="VolumeCreate")


@_attrs_define
class VolumeCreate:
    """
    Attributes:
        name (str):
        site (str): Site id (see GET /server-types); attach only to servers there
        size_gb (int):
    """

    name: str
    site: str
    size_gb: int

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        site = self.site

        size_gb = self.size_gb

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "site": site,
                "size_gb": size_gb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        site = d.pop("site")

        size_gb = d.pop("size_gb")

        volume_create = cls(
            name=name,
            site=site,
            size_gb=size_gb,
        )

        return volume_create
