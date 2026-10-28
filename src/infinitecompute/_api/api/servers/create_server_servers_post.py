from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.server import Server
from ...models.server_create import ServerCreate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ServerCreate,
    idempotency_key: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/servers",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Server:
    if response.status_code == 202:
        response_202 = Server.from_dict(response.json())

        return response_202

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Server]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ServerCreate,
    idempotency_key: None | str | Unset = UNSET,
) -> Response[ErrorResponse | Server]:
    """Create Server

     Launch a server. Send an Idempotency-Key header so retries are safe

    Args:
        idempotency_key (None | str | Unset): Any unique string, kept 24 hours
        body (ServerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Server]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ServerCreate,
    idempotency_key: None | str | Unset = UNSET,
) -> ErrorResponse | Server | None:
    """Create Server

     Launch a server. Send an Idempotency-Key header so retries are safe

    Args:
        idempotency_key (None | str | Unset): Any unique string, kept 24 hours
        body (ServerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Server
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ServerCreate,
    idempotency_key: None | str | Unset = UNSET,
) -> Response[ErrorResponse | Server]:
    """Create Server

     Launch a server. Send an Idempotency-Key header so retries are safe

    Args:
        idempotency_key (None | str | Unset): Any unique string, kept 24 hours
        body (ServerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Server]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ServerCreate,
    idempotency_key: None | str | Unset = UNSET,
) -> ErrorResponse | Server | None:
    """Create Server

     Launch a server. Send an Idempotency-Key header so retries are safe

    Args:
        idempotency_key (None | str | Unset): Any unique string, kept 24 hours
        body (ServerCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Server
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
