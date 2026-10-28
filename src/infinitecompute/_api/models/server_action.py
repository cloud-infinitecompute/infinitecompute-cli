from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerAction")


@_attrs_define
class ServerAction:
    """
    Attributes:
        action (str): start, stop, reboot, park (frees the GPU, stops GPU billing, keeps the disk) or resume (from
            parked)
        hard (bool | Unset): reboot only: a hard reboot (power cycle) Default: False.
    """

    action: str
    hard: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        hard = self.hard

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "action": action,
            }
        )
        if hard is not UNSET:
            field_dict["hard"] = hard

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = d.pop("action")

        hard = d.pop("hard", UNSET)

        server_action = cls(
            action=action,
            hard=hard,
        )

        return server_action
