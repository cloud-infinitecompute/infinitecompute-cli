from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_spend_line import UsageSpendLine


T = TypeVar("T", bound="UsageSpend")


@_attrs_define
class UsageSpend:
    """
    Attributes:
        amount (str): Decimal string: this project's rated charges
        currency (str):
        lines (list[UsageSpendLine]):
        rated_until (datetime.datetime | None | Unset): Usage after this isn't rated yet
    """

    amount: str
    currency: str
    lines: list[UsageSpendLine]
    rated_until: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        currency = self.currency

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        rated_until: None | str | Unset
        if isinstance(self.rated_until, Unset):
            rated_until = UNSET
        elif isinstance(self.rated_until, datetime.datetime):
            rated_until = self.rated_until.isoformat()
        else:
            rated_until = self.rated_until

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "currency": currency,
                "lines": lines,
            }
        )
        if rated_until is not UNSET:
            field_dict["rated_until"] = rated_until

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_spend_line import UsageSpendLine  # noqa: PLC0415

        d = dict(src_dict)
        amount = d.pop("amount")

        currency = d.pop("currency")

        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = UsageSpendLine.from_dict(lines_item_data)

            lines.append(lines_item)

        def _parse_rated_until(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rated_until_type_0 = datetime.datetime.fromisoformat(data)

                return rated_until_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        rated_until = _parse_rated_until(d.pop("rated_until", UNSET))

        usage_spend = cls(
            amount=amount,
            currency=currency,
            lines=lines,
            rated_until=rated_until,
        )

        usage_spend.additional_properties = d
        return usage_spend

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
