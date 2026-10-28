from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Backup")


@_attrs_define
class Backup:
    """
    Attributes:
        id (str):
        name (str):
        size_gb (int):
        status (str): creating, available, restoring, busy, deleting, error
        volume_id (str):
        created_at (datetime.datetime | None | Unset):
        data_timestamp (datetime.datetime | None | Unset): The point in time the backup holds
        incremental (bool | Unset):  Default: False.
    """

    id: str
    name: str
    size_gb: int
    status: str
    volume_id: str
    created_at: datetime.datetime | None | Unset = UNSET
    data_timestamp: datetime.datetime | None | Unset = UNSET
    incremental: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        size_gb = self.size_gb

        status = self.status

        volume_id = self.volume_id

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        data_timestamp: None | str | Unset
        if isinstance(self.data_timestamp, Unset):
            data_timestamp = UNSET
        elif isinstance(self.data_timestamp, datetime.datetime):
            data_timestamp = self.data_timestamp.isoformat()
        else:
            data_timestamp = self.data_timestamp

        incremental = self.incremental

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "size_gb": size_gb,
                "status": status,
                "volume_id": volume_id,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if data_timestamp is not UNSET:
            field_dict["data_timestamp"] = data_timestamp
        if incremental is not UNSET:
            field_dict["incremental"] = incremental

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size_gb = d.pop("size_gb")

        status = d.pop("status")

        volume_id = d.pop("volume_id")

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_data_timestamp(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_timestamp_type_0 = datetime.datetime.fromisoformat(data)

                return data_timestamp_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        data_timestamp = _parse_data_timestamp(d.pop("data_timestamp", UNSET))

        incremental = d.pop("incremental", UNSET)

        backup = cls(
            id=id,
            name=name,
            size_gb=size_gb,
            status=status,
            volume_id=volume_id,
            created_at=created_at,
            data_timestamp=data_timestamp,
            incremental=incremental,
        )

        backup.additional_properties = d
        return backup

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
