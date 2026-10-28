from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.usage import Usage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    month: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_month: None | str | Unset
    if isinstance(month, Unset):
        json_month = UNSET
    else:
        json_month = month
    params["month"] = json_month

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/usage",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Usage:
    if response.status_code == 200:
        response_200 = Usage.from_dict(response.json())

        return response_200

    response_default = ErrorResponse.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Usage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    month: None | str | Unset = UNSET,
) -> Response[ErrorResponse | Usage]:
    """Get Usage

     GPU-hours per server and rated charges for a UTC month

    Args:
        month (None | str | Unset): YYYY-MM (UTC); default this month

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Usage]
    """

    kwargs = _get_kwargs(
        month=month,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    month: None | str | Unset = UNSET,
) -> ErrorResponse | Usage | None:
    """Get Usage

     GPU-hours per server and rated charges for a UTC month

    Args:
        month (None | str | Unset): YYYY-MM (UTC); default this month

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Usage
    """

    return sync_detailed(
        client=client,
        month=month,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    month: None | str | Unset = UNSET,
) -> Response[ErrorResponse | Usage]:
    """Get Usage

     GPU-hours per server and rated charges for a UTC month

    Args:
        month (None | str | Unset): YYYY-MM (UTC); default this month

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Usage]
    """

    kwargs = _get_kwargs(
        month=month,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    month: None | str | Unset = UNSET,
) -> ErrorResponse | Usage | None:
    """Get Usage

     GPU-hours per server and rated charges for a UTC month

    Args:
        month (None | str | Unset): YYYY-MM (UTC); default this month

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Usage
    """

    return (
        await asyncio_detailed(
            client=client,
            month=month,
        )
    ).parsed
