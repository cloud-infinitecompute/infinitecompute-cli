from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.price import Price
    from ..models.server_type_gpu import ServerTypeGpu
    from ..models.site import Site


T = TypeVar("T", bound="ServerType")


@_attrs_define
class ServerType:
    """
    Attributes:
        id (str):
        name (str): Use this as server_type when creating a server
        ram_gb (float):
        site (Site):
        vcpus (int):
        gpu (None | ServerTypeGpu | Unset): null for a CPU-only type
        price (None | Price | Unset): Current list price; null if not priced
    """

    id: str
    name: str
    ram_gb: float
    site: Site
    vcpus: int
    gpu: None | ServerTypeGpu | Unset = UNSET
    price: None | Price | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.price import Price  # noqa: PLC0415
        from ..models.server_type_gpu import ServerTypeGpu  # noqa: PLC0415

        id = self.id

        name = self.name

        ram_gb = self.ram_gb

        site = self.site.to_dict()

        vcpus = self.vcpus

        gpu: dict[str, Any] | None | Unset
        if isinstance(self.gpu, Unset):
            gpu = UNSET
        elif isinstance(self.gpu, ServerTypeGpu):
            gpu = self.gpu.to_dict()
        else:
            gpu = self.gpu

        price: dict[str, Any] | None | Unset
        if isinstance(self.price, Unset):
            price = UNSET
        elif isinstance(self.price, Price):
            price = self.price.to_dict()
        else:
            price = self.price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "ram_gb": ram_gb,
                "site": site,
                "vcpus": vcpus,
            }
        )
        if gpu is not UNSET:
            field_dict["gpu"] = gpu
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.price import Price  # noqa: PLC0415
        from ..models.server_type_gpu import ServerTypeGpu  # noqa: PLC0415
        from ..models.site import Site  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        ram_gb = d.pop("ram_gb")

        site = Site.from_dict(d.pop("site"))

        vcpus = d.pop("vcpus")

        def _parse_gpu(data: object) -> None | ServerTypeGpu | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gpu_type_0 = ServerTypeGpu.from_dict(data)

                return gpu_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ServerTypeGpu | Unset, data)

        gpu = _parse_gpu(d.pop("gpu", UNSET))

        def _parse_price(data: object) -> None | Price | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                price_type_0 = Price.from_dict(data)

                return price_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Price | Unset, data)

        price = _parse_price(d.pop("price", UNSET))

        server_type = cls(
            id=id,
            name=name,
            ram_gb=ram_gb,
            site=site,
            vcpus=vcpus,
            gpu=gpu,
            price=price,
        )

        server_type.additional_properties = d
        return server_type

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
