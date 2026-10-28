from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MeKey")


@_attrs_define
class MeKey:
    """
    Attributes:
        expires_at (datetime.datetime):
        id (str): Key id (not secret)
        prefix (str): The key's visible prefix, as listed in the console
        scope (str): "read" or "read-write"
    """

    expires_at: datetime.datetime
    id: str
    prefix: str
    scope: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expires_at = self.expires_at.isoformat()

        id = self.id

        prefix = self.prefix

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expires_at": expires_at,
                "id": id,
                "prefix": prefix,
                "scope": scope,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        id = d.pop("id")

        prefix = d.pop("prefix")

        scope = d.pop("scope")

        me_key = cls(
            expires_at=expires_at,
            id=id,
            prefix=prefix,
            scope=scope,
        )

        me_key.additional_properties = d
        return me_key

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
