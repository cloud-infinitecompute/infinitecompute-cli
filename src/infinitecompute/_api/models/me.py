from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.me_key import MeKey
    from ..models.me_user import MeUser


T = TypeVar("T", bound="Me")


@_attrs_define
class Me:
    """
    Attributes:
        key (MeKey):
        project_id (str): The project every call with this key acts in
        user (MeUser):
    """

    key: MeKey
    project_id: str
    user: MeUser
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key.to_dict()

        project_id = self.project_id

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "project_id": project_id,
                "user": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.me_key import MeKey  # noqa: PLC0415
        from ..models.me_user import MeUser  # noqa: PLC0415

        d = dict(src_dict)
        key = MeKey.from_dict(d.pop("key"))

        project_id = d.pop("project_id")

        user = MeUser.from_dict(d.pop("user"))

        me = cls(
            key=key,
            project_id=project_id,
            user=user,
        )

        me.additional_properties = d
        return me

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
