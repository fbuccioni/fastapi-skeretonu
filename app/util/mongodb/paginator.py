import asyncio
from typing import Optional, Mapping, Any

from fastapi_contrib.serializers.common import Serializer
from fastapi_pagination.api import create_page, resolve_params
from fastapi_pagination.bases import AbstractPage, AbstractParams


async def contrib_paginate(
    serializer_class: Serializer,
    filter_kwargs: Mapping[str, Any] = {},
    params: Optional[AbstractParams] = None,
    sort=None
) -> AbstractPage[dict]:
    params = resolve_params(params)
    raw_params = params.to_raw_params()
    model = serializer_class.Meta.model

    get_list = model.list(
        _limit=raw_params.limit,
        _offset=raw_params.offset,
        _sort=sort,
        raw=True,
        **filter_kwargs
    )

    get_count = model.count(**filter_kwargs)
    count, _list = await asyncio.gather(get_count, get_list)

    return create_page(
        serializer_class.sanitize_list(_list), count, params
    )


__all__ = ["contrib_paginate"]
