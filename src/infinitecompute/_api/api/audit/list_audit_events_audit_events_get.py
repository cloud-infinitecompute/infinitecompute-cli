import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.audit_event_page import AuditEventPage
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    person: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    since: datetime.datetime | None | Unset = UNSET,
    until: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_person: None | str | Unset
    if isinstance(person, Unset):
        json_person = UNSET
    else:
        json_person = person
    params["person"] = json_person

    json_action: None | str | Unset
    if isinstance(action, Unset):
        json_action = UNSET
    else:
        json_action = action
    params["action"] = json_action

    json_since: None | str | Unset
    if isinstance(since, Unset):
        json_since = UNSET
    elif isinstance(since, datetime.datetime):
        json_since = since.isoformat()
    else:
        json_since = since
    params["since"] = json_since

    json_until: None | str | Unset
    if isinstance(until, Unset):
        json_until = UNSET
    elif isinstance(until, datetime.datetime):
        json_until = until.isoformat()
    else:
        json_until = until
    params["until"] = json_until

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/audit-events",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuditEventPage | ErrorResponse:
    if response.status_code == 200:
        response_200 = AuditEventPage.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuditEventPage | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    person: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    since: datetime.datetime | None | Unset = UNSET,
    until: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[AuditEventPage | ErrorResponse]:
    """List Audit Events

     Who changed what in this project, newest first (project owners' keys only)

    Args:
        person (None | str | Unset): Only this user id's actions
        action (None | str | Unset): An action ("server.create") or a resource ("server")
        since (datetime.datetime | None | Unset): RFC 3339, inclusive
        until (datetime.datetime | None | Unset): RFC 3339, exclusive
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditEventPage | ErrorResponse]
    """

    kwargs = _get_kwargs(
        person=person,
        action=action,
        since=since,
        until=until,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    person: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    since: datetime.datetime | None | Unset = UNSET,
    until: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> AuditEventPage | ErrorResponse | None:
    """List Audit Events

     Who changed what in this project, newest first (project owners' keys only)

    Args:
        person (None | str | Unset): Only this user id's actions
        action (None | str | Unset): An action ("server.create") or a resource ("server")
        since (datetime.datetime | None | Unset): RFC 3339, inclusive
        until (datetime.datetime | None | Unset): RFC 3339, exclusive
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditEventPage | ErrorResponse
    """

    return sync_detailed(
        client=client,
        person=person,
        action=action,
        since=since,
        until=until,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    person: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    since: datetime.datetime | None | Unset = UNSET,
    until: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[AuditEventPage | ErrorResponse]:
    """List Audit Events

     Who changed what in this project, newest first (project owners' keys only)

    Args:
        person (None | str | Unset): Only this user id's actions
        action (None | str | Unset): An action ("server.create") or a resource ("server")
        since (datetime.datetime | None | Unset): RFC 3339, inclusive
        until (datetime.datetime | None | Unset): RFC 3339, exclusive
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditEventPage | ErrorResponse]
    """

    kwargs = _get_kwargs(
        person=person,
        action=action,
        since=since,
        until=until,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    person: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    since: datetime.datetime | None | Unset = UNSET,
    until: datetime.datetime | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> AuditEventPage | ErrorResponse | None:
    """List Audit Events

     Who changed what in this project, newest first (project owners' keys only)

    Args:
        person (None | str | Unset): Only this user id's actions
        action (None | str | Unset): An action ("server.create") or a resource ("server")
        since (datetime.datetime | None | Unset): RFC 3339, inclusive
        until (datetime.datetime | None | Unset): RFC 3339, exclusive
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditEventPage | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            person=person,
            action=action,
            since=since,
            until=until,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
