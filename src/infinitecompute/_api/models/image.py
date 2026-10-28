from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Image")


@_attrs_define
class Image:
    """
    Attributes:
        gpu_models (list[str]): What the image is built for: GPU models (see server type gpu.model), or none for CPU-
            only types. An image with an empty list can't be launched
        id (str):
        name (str):
        status (str): active when usable
        visibility (str): public, or project (your project's own)
        created_at (datetime.datetime | None | Unset):
        login_user (None | str | Unset): The default SSH user, e.g. ubuntu
        min_disk_gb (int | Unset):  Default: 0.
        os_distro (None | str | Unset):
        os_version (None | str | Unset):
        size_bytes (int | None | Unset):
    """

    gpu_models: list[str]
    id: str
    name: str
    status: str
    visibility: str
    created_at: datetime.datetime | None | Unset = UNSET
    login_user: None | str | Unset = UNSET
    min_disk_gb: int | Unset = 0
    os_distro: None | str | Unset = UNSET
    os_version: None | str | Unset = UNSET
    size_bytes: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gpu_models = self.gpu_models

        id = self.id

        name = self.name

        status = self.status

        visibility = self.visibility

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        login_user: None | str | Unset
        if isinstance(self.login_user, Unset):
            login_user = UNSET
        else:
            login_user = self.login_user

        min_disk_gb = self.min_disk_gb

        os_distro: None | str | Unset
        if isinstance(self.os_distro, Unset):
            os_distro = UNSET
        else:
            os_distro = self.os_distro

        os_version: None | str | Unset
        if isinstance(self.os_version, Unset):
            os_version = UNSET
        else:
            os_version = self.os_version

        size_bytes: int | None | Unset
        if isinstance(self.size_bytes, Unset):
            size_bytes = UNSET
        else:
            size_bytes = self.size_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gpu_models": gpu_models,
                "id": id,
                "name": name,
                "status": status,
                "visibility": visibility,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if login_user is not UNSET:
            field_dict["login_user"] = login_user
        if min_disk_gb is not UNSET:
            field_dict["min_disk_gb"] = min_disk_gb
        if os_distro is not UNSET:
            field_dict["os_distro"] = os_distro
        if os_version is not UNSET:
            field_dict["os_version"] = os_version
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gpu_models = cast(list[str], d.pop("gpu_models"))

        id = d.pop("id")

        name = d.pop("name")

        status = d.pop("status")

        visibility = d.pop("visibility")

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

        def _parse_login_user(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        login_user = _parse_login_user(d.pop("login_user", UNSET))

        min_disk_gb = d.pop("min_disk_gb", UNSET)

        def _parse_os_distro(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        os_distro = _parse_os_distro(d.pop("os_distro", UNSET))

        def _parse_os_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        os_version = _parse_os_version(d.pop("os_version", UNSET))

        def _parse_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes", UNSET))

        image = cls(
            gpu_models=gpu_models,
            id=id,
            name=name,
            status=status,
            visibility=visibility,
            created_at=created_at,
            login_user=login_user,
            min_disk_gb=min_disk_gb,
            os_distro=os_distro,
            os_version=os_version,
            size_bytes=size_bytes,
        )

        image.additional_properties = d
        return image

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
