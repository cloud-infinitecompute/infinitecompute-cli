from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.server_address import ServerAddress
    from ..models.site import Site


T = TypeVar("T", bound="Server")


@_attrs_define
class Server:
    """
    Attributes:
        id (str):
        name (str):
        status (str): building, active, busy, stopped, parked, deleting, error
        addresses (list[ServerAddress] | Unset):
        created_at (datetime.datetime | None | Unset):
        error_reason (None | str | Unset): Set when status is error
        image_id (None | str | Unset): The image the system disk came from
        server_type (None | str | Unset): The server type's name
        site (None | Site | Unset):
        ssh_key (None | str | Unset):
        updated_at (datetime.datetime | None | Unset):
        volume_ids (list[str] | Unset): Attached volumes, system disk included
    """

    id: str
    name: str
    status: str
    addresses: list[ServerAddress] | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    error_reason: None | str | Unset = UNSET
    image_id: None | str | Unset = UNSET
    server_type: None | str | Unset = UNSET
    site: None | Site | Unset = UNSET
    ssh_key: None | str | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    volume_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.site import Site  # noqa: PLC0415

        id = self.id

        name = self.name

        status = self.status

        addresses: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.addresses, Unset):
            addresses = []
            for addresses_item_data in self.addresses:
                addresses_item = addresses_item_data.to_dict()
                addresses.append(addresses_item)

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        error_reason: None | str | Unset
        if isinstance(self.error_reason, Unset):
            error_reason = UNSET
        else:
            error_reason = self.error_reason

        image_id: None | str | Unset
        if isinstance(self.image_id, Unset):
            image_id = UNSET
        else:
            image_id = self.image_id

        server_type: None | str | Unset
        if isinstance(self.server_type, Unset):
            server_type = UNSET
        else:
            server_type = self.server_type

        site: dict[str, Any] | None | Unset
        if isinstance(self.site, Unset):
            site = UNSET
        elif isinstance(self.site, Site):
            site = self.site.to_dict()
        else:
            site = self.site

        ssh_key: None | str | Unset
        if isinstance(self.ssh_key, Unset):
            ssh_key = UNSET
        else:
            ssh_key = self.ssh_key

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        volume_ids: list[str] | Unset = UNSET
        if not isinstance(self.volume_ids, Unset):
            volume_ids = self.volume_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "status": status,
            }
        )
        if addresses is not UNSET:
            field_dict["addresses"] = addresses
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if error_reason is not UNSET:
            field_dict["error_reason"] = error_reason
        if image_id is not UNSET:
            field_dict["image_id"] = image_id
        if server_type is not UNSET:
            field_dict["server_type"] = server_type
        if site is not UNSET:
            field_dict["site"] = site
        if ssh_key is not UNSET:
            field_dict["ssh_key"] = ssh_key
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if volume_ids is not UNSET:
            field_dict["volume_ids"] = volume_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.server_address import ServerAddress  # noqa: PLC0415
        from ..models.site import Site  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        status = d.pop("status")

        _addresses = d.pop("addresses", UNSET)
        addresses: list[ServerAddress] | Unset = UNSET
        if _addresses is not UNSET:
            addresses = []
            for addresses_item_data in _addresses:
                addresses_item = ServerAddress.from_dict(addresses_item_data)

                addresses.append(addresses_item)

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

        def _parse_error_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_reason = _parse_error_reason(d.pop("error_reason", UNSET))

        def _parse_image_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_id = _parse_image_id(d.pop("image_id", UNSET))

        def _parse_server_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        server_type = _parse_server_type(d.pop("server_type", UNSET))

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

        def _parse_ssh_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ssh_key = _parse_ssh_key(d.pop("ssh_key", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        volume_ids = cast(list[str], d.pop("volume_ids", UNSET))

        server = cls(
            id=id,
            name=name,
            status=status,
            addresses=addresses,
            created_at=created_at,
            error_reason=error_reason,
            image_id=image_id,
            server_type=server_type,
            site=site,
            ssh_key=ssh_key,
            updated_at=updated_at,
            volume_ids=volume_ids,
        )

        server.additional_properties = d
        return server

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
