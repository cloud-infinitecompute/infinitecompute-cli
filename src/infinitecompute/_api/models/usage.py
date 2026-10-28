from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_server import UsageServer
    from ..models.usage_spend import UsageSpend


T = TypeVar("T", bound="Usage")


@_attrs_define
class Usage:
    """
    Attributes:
        end (datetime.datetime):
        generated_at (datetime.datetime):
        month (str): YYYY-MM (UTC)
        servers (list[UsageServer]):
        start (datetime.datetime):
        total_gpu_hours (float):
        spend (None | Unset | UsageSpend): Rated charges; null when the project has no billing account
    """

    end: datetime.datetime
    generated_at: datetime.datetime
    month: str
    servers: list[UsageServer]
    start: datetime.datetime
    total_gpu_hours: float
    spend: None | Unset | UsageSpend = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_spend import UsageSpend  # noqa: PLC0415

        end = self.end.isoformat()

        generated_at = self.generated_at.isoformat()

        month = self.month

        servers = []
        for servers_item_data in self.servers:
            servers_item = servers_item_data.to_dict()
            servers.append(servers_item)

        start = self.start.isoformat()

        total_gpu_hours = self.total_gpu_hours

        spend: dict[str, Any] | None | Unset
        if isinstance(self.spend, Unset):
            spend = UNSET
        elif isinstance(self.spend, UsageSpend):
            spend = self.spend.to_dict()
        else:
            spend = self.spend

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "end": end,
                "generated_at": generated_at,
                "month": month,
                "servers": servers,
                "start": start,
                "total_gpu_hours": total_gpu_hours,
            }
        )
        if spend is not UNSET:
            field_dict["spend"] = spend

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_server import UsageServer  # noqa: PLC0415
        from ..models.usage_spend import UsageSpend  # noqa: PLC0415

        d = dict(src_dict)
        end = datetime.datetime.fromisoformat(d.pop("end"))

        generated_at = datetime.datetime.fromisoformat(d.pop("generated_at"))

        month = d.pop("month")

        servers = []
        _servers = d.pop("servers")
        for servers_item_data in _servers:
            servers_item = UsageServer.from_dict(servers_item_data)

            servers.append(servers_item)

        start = datetime.datetime.fromisoformat(d.pop("start"))

        total_gpu_hours = d.pop("total_gpu_hours")

        def _parse_spend(data: object) -> None | Unset | UsageSpend:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                spend_type_0 = UsageSpend.from_dict(data)

                return spend_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UsageSpend, data)

        spend = _parse_spend(d.pop("spend", UNSET))

        usage = cls(
            end=end,
            generated_at=generated_at,
            month=month,
            servers=servers,
            start=start,
            total_gpu_hours=total_gpu_hours,
            spend=spend,
        )

        usage.additional_properties = d
        return usage

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
