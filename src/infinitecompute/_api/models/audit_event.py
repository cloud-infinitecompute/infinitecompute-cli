from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_actor import AuditActor
    from ..models.audit_resource import AuditResource


T = TypeVar("T", bound="AuditEvent")


@_attrs_define
class AuditEvent:
    """
    Attributes:
        action (str): Our verb, e.g. server.create, volume.attach
        actor (AuditActor):
        id (str):
        outcome (str): "ok", "denied" or "error"
        project_id (str):
        time (datetime.datetime):
        via (str): "console" or "api"
        error_code (None | str | Unset): Set when outcome isn't ok
        request_id (None | str | Unset):
        resource (AuditResource | None | Unset):
        source_ip (None | str | Unset):
    """

    action: str
    actor: AuditActor
    id: str
    outcome: str
    project_id: str
    time: datetime.datetime
    via: str
    error_code: None | str | Unset = UNSET
    request_id: None | str | Unset = UNSET
    resource: AuditResource | None | Unset = UNSET
    source_ip: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_resource import AuditResource  # noqa: PLC0415

        action = self.action

        actor = self.actor.to_dict()

        id = self.id

        outcome = self.outcome

        project_id = self.project_id

        time = self.time.isoformat()

        via = self.via

        error_code: None | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        resource: dict[str, Any] | None | Unset
        if isinstance(self.resource, Unset):
            resource = UNSET
        elif isinstance(self.resource, AuditResource):
            resource = self.resource.to_dict()
        else:
            resource = self.resource

        source_ip: None | str | Unset
        if isinstance(self.source_ip, Unset):
            source_ip = UNSET
        else:
            source_ip = self.source_ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "actor": actor,
                "id": id,
                "outcome": outcome,
                "project_id": project_id,
                "time": time,
                "via": via,
            }
        )
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if resource is not UNSET:
            field_dict["resource"] = resource
        if source_ip is not UNSET:
            field_dict["source_ip"] = source_ip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_actor import AuditActor  # noqa: PLC0415
        from ..models.audit_resource import AuditResource  # noqa: PLC0415

        d = dict(src_dict)
        action = d.pop("action")

        actor = AuditActor.from_dict(d.pop("actor"))

        id = d.pop("id")

        outcome = d.pop("outcome")

        project_id = d.pop("project_id")

        time = datetime.datetime.fromisoformat(d.pop("time"))

        via = d.pop("via")

        def _parse_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        def _parse_resource(data: object) -> AuditResource | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                resource_type_0 = AuditResource.from_dict(data)

                return resource_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AuditResource | None | Unset, data)

        resource = _parse_resource(d.pop("resource", UNSET))

        def _parse_source_ip(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_ip = _parse_source_ip(d.pop("source_ip", UNSET))

        audit_event = cls(
            action=action,
            actor=actor,
            id=id,
            outcome=outcome,
            project_id=project_id,
            time=time,
            via=via,
            error_code=error_code,
            request_id=request_id,
            resource=resource,
            source_ip=source_ip,
        )

        audit_event.additional_properties = d
        return audit_event

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
