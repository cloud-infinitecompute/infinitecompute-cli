from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.site import Site


T = TypeVar("T", bound="Volume")


@_attrs_define
class Volume:
    """
    Attributes:
        id (str):
        name (str):
        size_gb (int):
        status (str): creating, available, in_use, busy, deleting, error
        attached_to (list[str] | Unset): Server ids
        bootable (bool | Unset):  Default: False.
        created_at (datetime.datetime | None | Unset):
        image_id (None | str | Unset): Set when created from an image
        site (None | Site | Unset):
    """

    id: str
    name: str
    size_gb: int
    status: str
    attached_to: list[str] | Unset = UNSET
    bootable: bool | Unset = False
    created_at: datetime.datetime | None | Unset = UNSET
    image_id: None | str | Unset = UNSET
    site: None | Site | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.site import Site  # noqa: PLC0415

        id = self.id

        name = self.name

        size_gb = self.size_gb

        status = self.status

        attached_to: list[str] | Unset = UNSET
        if not isinstance(self.attached_to, Unset):
            attached_to = self.attached_to

        bootable = self.bootable

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        image_id: None | str | Unset
        if isinstance(self.image_id, Unset):
            image_id = UNSET
        else:
            image_id = self.image_id

        site: dict[str, Any] | None | Unset
        if isinstance(self.site, Unset):
            site = UNSET
        elif isinstance(self.site, Site):
            site = self.site.to_dict()
        else:
            site = self.site

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "size_gb": size_gb,
                "status": status,
            }
        )
        if attached_to is not UNSET:
            field_dict["attached_to"] = attached_to
        if bootable is not UNSET:
            field_dict["bootable"] = bootable
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if image_id is not UNSET:
            field_dict["image_id"] = image_id
        if site is not UNSET:
            field_dict["site"] = site

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.site import Site  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size_gb = d.pop("size_gb")

        status = d.pop("status")

        attached_to = cast(list[str], d.pop("attached_to", UNSET))

        bootable = d.pop("bootable", UNSET)

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

        def _parse_image_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_id = _parse_image_id(d.pop("image_id", UNSET))

        def _parse_site(data: object) -> None | Site | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                site_type_0 = Site.from_dict(data)

                return site_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Site | Unset, data)

        site = _parse_site(d.pop("site", UNSET))

        volume = cls(
            id=id,
            name=name,
            size_gb=size_gb,
            status=status,
            attached_to=attached_to,
            bootable=bootable,
            created_at=created_at,
            image_id=image_id,
            site=site,
        )

        volume.additional_properties = d
        return volume

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
