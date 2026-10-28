from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="VolumeAttach")


@_attrs_define
class VolumeAttach:
    """
    Attributes:
        server_id (str):
    """

    server_id: str

    def to_dict(self) -> dict[str, Any]:
        server_id = self.server_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "server_id": server_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_id = d.pop("server_id")

        volume_attach = cls(
            server_id=server_id,
        )

        return volume_attach
