from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerTypeGpu")


@_attrs_define
class ServerTypeGpu:
    """
    Attributes:
        count (int):
        model (str): GPU model id, matched by images' gpu_models, e.g. h100
        name (str): Display name, e.g. NVIDIA H100 PCIe
        vram_gb (int | None | Unset): Memory per GPU
    """

    count: int
    model: str
    name: str
    vram_gb: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        model = self.model

        name = self.name

        vram_gb: int | None | Unset
        if isinstance(self.vram_gb, Unset):
            vram_gb = UNSET
        else:
            vram_gb = self.vram_gb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "model": model,
                "name": name,
            }
        )
        if vram_gb is not UNSET:
            field_dict["vram_gb"] = vram_gb

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        model = d.pop("model")

        name = d.pop("name")

        def _parse_vram_gb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        vram_gb = _parse_vram_gb(d.pop("vram_gb", UNSET))

        server_type_gpu = cls(
            count=count,
            model=model,
            name=name,
            vram_gb=vram_gb,
        )

        server_type_gpu.additional_properties = d
        return server_type_gpu

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
