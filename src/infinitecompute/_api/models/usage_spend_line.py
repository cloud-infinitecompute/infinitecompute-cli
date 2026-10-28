from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UsageSpendLine")


@_attrs_define
class UsageSpendLine:
    """
    Attributes:
        amount (str): Decimal string, in currency
        quantity (str): Decimal string
        sku (str):
        unit (str): e.g. gpu_hour
    """

    amount: str
    quantity: str
    sku: str
    unit: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        quantity = self.quantity

        sku = self.sku

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "quantity": quantity,
                "sku": sku,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

        quantity = d.pop("quantity")

        sku = d.pop("sku")

        unit = d.pop("unit")

        usage_spend_line = cls(
            amount=amount,
            quantity=quantity,
            sku=sku,
            unit=unit,
        )

        usage_spend_line.additional_properties = d
        return usage_spend_line

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
