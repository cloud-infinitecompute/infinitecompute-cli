from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerCreate")


@_attrs_define
class ServerCreate:
    """
    Attributes:
        image (str): An image id or name built for the type's GPU: its gpu_models include the type's gpu.model, or none
            for a CPU type (see /images)
        name (str):
        server_type (str): A server type's name or id (see /server-types)
        ssh_key (str): The name of one of your SSH keys (see /ssh-keys)
        delete_disk_with_server (bool | Unset): Delete the system disk when the server is deleted Default: True.
        disk_gb (int | None | Unset): System disk size; default 50, at least the image's
        user_data (None | str | Unset): cloud-init user data as text (e.g. #cloud-config), at most 48 KiB
    """

    image: str
    name: str
    server_type: str
    ssh_key: str
    delete_disk_with_server: bool | Unset = True
    disk_gb: int | None | Unset = UNSET
    user_data: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        name = self.name

        server_type = self.server_type

        ssh_key = self.ssh_key

        delete_disk_with_server = self.delete_disk_with_server

        disk_gb: int | None | Unset
        if isinstance(self.disk_gb, Unset):
            disk_gb = UNSET
        else:
            disk_gb = self.disk_gb

        user_data: None | str | Unset
        if isinstance(self.user_data, Unset):
            user_data = UNSET
        else:
            user_data = self.user_data

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "image": image,
                "name": name,
                "server_type": server_type,
                "ssh_key": ssh_key,
            }
        )
        if delete_disk_with_server is not UNSET:
            field_dict["delete_disk_with_server"] = delete_disk_with_server
        if disk_gb is not UNSET:
            field_dict["disk_gb"] = disk_gb
        if user_data is not UNSET:
            field_dict["user_data"] = user_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image = d.pop("image")

        name = d.pop("name")

        server_type = d.pop("server_type")

        ssh_key = d.pop("ssh_key")

        delete_disk_with_server = d.pop("delete_disk_with_server", UNSET)

        def _parse_disk_gb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        disk_gb = _parse_disk_gb(d.pop("disk_gb", UNSET))

        def _parse_user_data(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_data = _parse_user_data(d.pop("user_data", UNSET))

        server_create = cls(
            image=image,
            name=name,
            server_type=server_type,
            ssh_key=ssh_key,
            delete_disk_with_server=delete_disk_with_server,
            disk_gb=disk_gb,
            user_data=user_data,
        )

        return server_create
