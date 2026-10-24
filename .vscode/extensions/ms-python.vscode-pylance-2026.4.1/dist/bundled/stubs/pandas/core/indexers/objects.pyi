from collections.abc import Sequence
from typing import Any

from pandas.core.indexes.datetimes import DatetimeIndex

from pandas._libs.tslibs import BaseOffset
from pandas._typing import (
    np_1darray_intp,
    np_ndarray_intp,
)

class BaseIndexer:
    def __init__(
        self,
        index_array: Sequence[float] | np_ndarray_intp | None = None,
        window_size: int = 0,
        **kwargs: Any,
    ) -> None: ...
    def get_window_bounds(
        self,
        num_values: int,
        min_periods: int | None,
        center: bool | None,
        closed: str | None = None,
        step: int | None = None,
    ) -> tuple[np_1darray_intp, np_1darray_intp]:
        """
Computes the bounds of a window.

Parameters
----------
num_values : int, default 0
    number of values that will be aggregated over
window_size : int, default 0
    the number of rows in a window
min_periods : int, default None
    min_periods passed from the top level rolling API
center : bool, default None
    center passed from the top level rolling API
closed : str, default None
    closed passed from the top level rolling API
step : int, default None
    step passed from the top level rolling API
win_type : str, default None
    win_type passed from the top level rolling API

Returns
-------
A tuple of ndarray[int64]s, indicating the boundaries of each
window
        """
        pass

class FixedForwardWindowIndexer(BaseIndexer): ...

class VariableOffsetWindowIndexer(BaseIndexer):
    def __init__(
        self,
        index_array: np_ndarray_intp | None = None,
        window_size: int = 0,
        index: DatetimeIndex | None = None,
        offset: BaseOffset | None = None,
        **kwargs: Any,
    ) -> None: ...
