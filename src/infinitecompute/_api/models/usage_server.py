from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageServer")


@_attrs_define
class UsageServer:
    """
    Attributes:
        deleted (bool):
        gpu_count (int):
        gpu_hours (float):
        gpu_model (str): Display name of the GPU
        name (str):
        server_id (str):
        server_type (None | str | Unset):
        sku (None | str | Unset): Billing SKU, e.g. gpu:h100
    """

    deleted: bool
    gpu_count: int
    gpu_hours: float
    gpu_model: str
    name: str
    server_id: str
    server_type: None | str | Unset = UNSET
    sku: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted = self.deleted

        gpu_count = self.gpu_count

        gpu_hours = self.gpu_hours

        gpu_model = self.gpu_model

        name = self.name

        server_id = self.server_id

        server_type: None | str | Unset
        if isinstance(self.server_type, Unset):
            server_type = UNSET
        else:
            server_type = self.server_type

        sku: None | str | Unset
        if isinstance(self.sku, Unset):
            sku = UNSET
        else:
            sku = self.sku

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deleted": deleted,
                "gpu_count": gpu_count,
                "gpu_hours": gpu_hours,
                "gpu_model": gpu_model,
                "name": name,
                "server_id": server_id,
            }
        )
        if server_type is not UNSET:
            field_dict["server_type"] = server_type
        if sku is not UNSET:
            field_dict["sku"] = sku

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deleted = d.pop("deleted")

        gpu_count = d.pop("gpu_count")

        gpu_hours = d.pop("gpu_hours")

        gpu_model = d.pop("gpu_model")

        name = d.pop("name")

        server_id = d.pop("server_id")

        def _parse_server_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        server_type = _parse_server_type(d.pop("server_type", UNSET))

        def _parse_sku(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sku = _parse_sku(d.pop("sku", UNSET))

        usage_server = cls(
            deleted=deleted,
            gpu_count=gpu_count,
            gpu_hours=gpu_hours,
            gpu_model=gpu_model,
            name=name,
            server_id=server_id,
            server_type=server_type,
            sku=sku,
        )

        usage_server.additional_properties = d
        return usage_server

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
