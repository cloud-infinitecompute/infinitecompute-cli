from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.backup_list import BackupList
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    volume_id: str,
    *,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

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
        "url": "/volumes/{volume_id}/backups".format(
            volume_id=quote(str(volume_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BackupList | ErrorResponse:
    if response.status_code == 200:
        response_200 = BackupList.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BackupList | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    volume_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[BackupList | ErrorResponse]:
    """List Backups

     Backups the project took of this volume, newest first

    Args:
        volume_id (str):
        limit (int | Unset): Items per page Default: 50.
        cursor (None | str | Unset): next_cursor from the previous page

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackupList | ErrorResponse]
    """

    kwargs = _get_kwargs(
        volume_id=volume_id,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    volume_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> BackupList | ErrorResponse | None:
    """List Backups

     Backups the project took of this volume, newest first

    Args:
        volume_id (str):
        limit (int | Unset): Items per page Default: 50.
        cursor (None | str | Unset): next_cursor from the previous page

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackupList | ErrorResponse
    """

    return sync_detailed(
        volume_id=volume_id,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    volume_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[BackupList | ErrorResponse]:
    """List Backups

     Backups the project took of this volume, newest first

    Args:
        volume_id (str):
        limit (int | Unset): Items per page Default: 50.
        cursor (None | str | Unset): next_cursor from the previous page

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackupList | ErrorResponse]
    """

    kwargs = _get_kwargs(
        volume_id=volume_id,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    volume_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> BackupList | ErrorResponse | None:
    """List Backups

     Backups the project took of this volume, newest first

    Args:
        volume_id (str):
        limit (int | Unset): Items per page Default: 50.
        cursor (None | str | Unset): next_cursor from the previous page

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackupList | ErrorResponse
    """

    return (
        await asyncio_detailed(
            volume_id=volume_id,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
