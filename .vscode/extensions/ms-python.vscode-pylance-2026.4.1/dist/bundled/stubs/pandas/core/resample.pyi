from collections.abc import (
    Callable,
    Mapping,
)
from typing import (
    Any,
    Literal,
    Never,
    Self,
    TypeAlias,
    final,
    overload,
)

from pandas.core.frame import DataFrame
from pandas.core.groupby.generic import SeriesGroupBy
from pandas.core.groupby.groupby import BaseGroupBy
from pandas.core.groupby.grouper import Grouper
from pandas.core.series import Series
from typing_extensions import override

from pandas._libs.tslibs.timedeltas import Timedelta
from pandas._typing import (
    S1,
    Axis,
    HashableT,
    InterpolateOptions,
    NDFrameT,
    Scalar,
    TimeGrouperOrigin,
    TimestampConvention,
    np_ndarray_float,
)

_FrameGroupByFunc: TypeAlias = Callable[[DataFrame], Scalar | Series | DataFrame]
_FrameGroupByFuncTypes: TypeAlias = (
    _FrameGroupByFunc | str | list[_FrameGroupByFunc | str]
)

_SeriesGroupByFunc: TypeAlias = Callable[[Series], Scalar | Series]
_SeriesGroupByFuncTypes: TypeAlias = _SeriesGroupByFunc | str

class Resampler(BaseGroupBy[NDFrameT]):
    def __getattr__(self, attr: str, /) -> SeriesGroupBy[Any, Any]: ...
    @overload
    def aggregate(
        self: Resampler[DataFrame],
        func: (
            _FrameGroupByFuncTypes | Mapping[HashableT, _FrameGroupByFuncTypes] | None
        ) = None,
        *args: Any,
        **kwargs: Any,
    ) -> DataFrame:
        """
Aggregate using one or more operations over the specified axis.

Parameters
----------
func : function, str, list or dict
    Function to use for aggregating the data. If a function, must either
    work when passed a DataFrame or when passed to DataFrame.apply.

    Accepted combinations are:

    - function
    - string function name
    - list of functions and/or function names, e.g. ``[np.sum, 'mean']``
    - dict of axis labels -> functions, function names or list of such.
*args
    Positional arguments to pass to `func`.
**kwargs
    Keyword arguments to pass to `func`.

Returns
-------
scalar, Series or DataFrame

    The return can be:

    * scalar : when Series.agg is called with single function
    * Series : when DataFrame.agg is called with a single function
    * DataFrame : when DataFrame.agg is called with several functions

See Also
--------
DataFrame.groupby.aggregate : Aggregate using callable, string, dict,
    or list of string/callables.
DataFrame.resample.transform : Transforms the Series on each group
    based on the given function.
DataFrame.aggregate: Aggregate using one or more
    operations over the specified axis.

Notes
-----
The aggregation operations are always performed over an axis, either the
index (default) or the column axis. This behavior is different from
`numpy` aggregation functions (`mean`, `median`, `prod`, `sum`, `std`,
`var`), where the default is to compute the aggregation of the flattened
array, e.g., ``numpy.mean(arr_2d)`` as opposed to
``numpy.mean(arr_2d, axis=0)``.

`agg` is an alias for `aggregate`. Use the alias.

Functions that mutate the passed object can produce unexpected
behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
for more details.

A passed user-defined-function will be passed a Series for evaluation.

If ``func`` defines an index relabeling, ``axis`` must be ``0`` or ``index``.

Examples
--------
>>> s = pd.Series(
...     [1, 2, 3, 4, 5], index=pd.date_range("20130101", periods=5, freq="s")
... )
>>> s
2013-01-01 00:00:00    1
2013-01-01 00:00:01    2
2013-01-01 00:00:02    3
2013-01-01 00:00:03    4
2013-01-01 00:00:04    5
Freq: s, dtype: int64

>>> r = s.resample("2s")

>>> r.agg("sum")
2013-01-01 00:00:00    3
2013-01-01 00:00:02    7
2013-01-01 00:00:04    5
Freq: 2s, dtype: int64

>>> r.agg(["sum", "mean", "max"])
                    sum  mean  max
2013-01-01 00:00:00    3   1.5    2
2013-01-01 00:00:02    7   3.5    4
2013-01-01 00:00:04    5   5.0    5

>>> r.agg({"result": lambda x: x.mean() / x.std(), "total": "sum"})
                    result  total
2013-01-01 00:00:00  2.121320      3
2013-01-01 00:00:02  4.949747      7
2013-01-01 00:00:04       NaN      5

>>> r.agg(average="mean", total="sum")
                        average  total
2013-01-01 00:00:00      1.5      3
2013-01-01 00:00:02      3.5      7
2013-01-01 00:00:04      5.0      5
        """
        pass
    @overload
    def aggregate(
        self: Resampler[Series],
        func: _SeriesGroupByFuncTypes | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Series: ...
    @overload
    def aggregate(
        self: Resampler[Series],
        func: (
            Mapping[HashableT, _SeriesGroupByFuncTypes] | list[_SeriesGroupByFuncTypes]
        ),
        *args: Any,
        **kwargs: Any,
    ) -> DataFrame: ...
    agg = aggregate
    apply = aggregate
    @overload
    def transform(
        self: Resampler[Series],
        arg: Callable[[Series], Series[S1]],
        *args: Any,
        **kwargs: Any,
    ) -> Series[S1]: ...
    @overload
    def transform(
        self: Resampler[DataFrame],
        arg: Callable[[Series], Series[S1]],
        *args: Any,
        **kwargs: Any,
    ) -> DataFrame: ...
    @final
    def ffill(self, limit: int | None = ...) -> NDFrameT: ...
    @final
    def nearest(self, limit: int | None = ...) -> NDFrameT: ...
    @final
    def bfill(self, limit: int | None = ...) -> NDFrameT: ...
    @overload
    def interpolate(
        self,
        method: InterpolateOptions = ...,
        *,
        axis: Axis = ...,
        limit: int | None = ...,
        limit_direction: Literal["forward", "backward", "both"] = ...,
        limit_area: Literal["inside", "outside"] | None = ...,
        inplace: bool,
        **kwargs: Any,
    ) -> Never: ...
    @overload
    def interpolate(
        self,
        method: InterpolateOptions = ...,
        *,
        axis: Axis = ...,
        limit: int | None = ...,
        limit_direction: Literal["forward", "backward", "both"] = ...,
        limit_area: Literal["inside", "outside"] | None = ...,
        **kwargs: Any,
    ) -> NDFrameT: ...
    @final
    def asfreq(self, fill_value: Scalar | None = ...) -> NDFrameT: ...
    @final
    def sum(self, numeric_only: bool = False, min_count: int = 0) -> NDFrameT: ...
    @final
    def prod(self, numeric_only: bool = False, min_count: int = 0) -> NDFrameT: ...
    @final
    def min(self, numeric_only: bool = ..., min_count: int = ...) -> NDFrameT: ...
    @final
    def max(self, numeric_only: bool = ..., min_count: int = ...) -> NDFrameT: ...
    @final
    def first(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
        skipna: bool = True,
    ) -> NDFrameT:
        """
Compute the first non-null entry of each column.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.
min_count : int, default 0
    The required number of valid values to perform the operation. If fewer
    than ``min_count`` non-NA values are present the result will be NA.
skipna : bool, default True
    Exclude NA/null values. If an entire group is NA, the result will be NA.

Returns
-------
Series or DataFrame
    First values within each group.

See Also
--------
core.resample.Resampler.last : Compute the last non-null value in each group.
core.resample.Resampler.mean : Compute mean of groups, excluding missing values.

Examples
--------
>>> s = pd.Series(
...     [1, 2, 3, 4],
...     index=pd.DatetimeIndex(
...         ["2023-01-01", "2023-01-15", "2023-02-01", "2023-02-15"]
...     ),
... )
>>> s
2023-01-01    1
2023-01-15    2
2023-02-01    3
2023-02-15    4
dtype: int64
>>> s.resample("MS").first()
2023-01-01    1
2023-02-01    3
Freq: MS, dtype: int64
        """
        pass
    @final
    def last(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
        skipna: bool = True,
    ) -> NDFrameT:
        """
Compute the last non-null entry of each column.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.
min_count : int, default 0
    The required number of valid values to perform the operation. If fewer
    than ``min_count`` non-NA values are present the result will be NA.
skipna : bool, default True
    Exclude NA/null values. If an entire group is NA, the result will be NA.

Returns
-------
Series or DataFrame
    Last of values within each group.

See Also
--------
core.resample.Resampler.first : Compute the first non-null value in each group.
core.resample.Resampler.mean : Compute mean of groups, excluding missing values.

Examples
--------
>>> s = pd.Series(
...     [1, 2, 3, 4],
...     index=pd.DatetimeIndex(
...         ["2023-01-01", "2023-01-15", "2023-02-01", "2023-02-15"]
...     ),
... )
>>> s
2023-01-01    1
2023-01-15    2
2023-02-01    3
2023-02-15    4
dtype: int64
>>> s.resample("MS").last()
2023-01-01    2
2023-02-01    4
Freq: MS, dtype: int64
        """
        pass
    @final
    def median(self, numeric_only: bool = False) -> NDFrameT:
        """
Compute median of groups, excluding missing values.

For multiple groupings, the result index will be a MultiIndex

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionchanged:: 2.0.0

        numeric_only no longer accepts ``None`` and defaults to False.

Returns
-------
Series or DataFrame
    Median of values within each group.

See Also
--------
Series.groupby : Apply a function groupby to a Series.
DataFrame.groupby : Apply a function groupby to each row or column of a
    DataFrame.

Examples
--------

>>> ser = pd.Series(
...     [1, 2, 3, 3, 4, 5],
...     index=pd.DatetimeIndex(
...         [
...             "2023-01-01",
...             "2023-01-10",
...             "2023-01-15",
...             "2023-02-01",
...             "2023-02-10",
...             "2023-02-15",
...         ]
...     ),
... )
>>> ser.resample("MS").median()
2023-01-01    2.0
2023-02-01    4.0
Freq: MS, dtype: float64
        """
        pass
    @final
    def mean(self, numeric_only: bool = False) -> NDFrameT: ...
    @final
    def std(self, ddof: int = 1, numeric_only: bool = False) -> NDFrameT: ...
    @final
    def var(self, ddof: int = 1, numeric_only: bool = False) -> NDFrameT: ...
    @final
    def sem(self, ddof: int = 1, numeric_only: bool = False) -> NDFrameT:
        """
Compute standard error of the mean of groups, excluding missing values.

For multiple groupings, the result index will be a MultiIndex.

Parameters
----------
ddof : int, default 1
    Degrees of freedom.

numeric_only : bool, default False
    Include only `float`, `int` or `boolean` data.

    .. versionchanged:: 2.0.0

        numeric_only now defaults to ``False``.

Returns
-------
Series or DataFrame
    Standard error of the mean of values within each group.

See Also
--------
DataFrame.sem : Return unbiased standard error of the mean over requested axis.
Series.sem : Return unbiased standard error of the mean over requested axis.

Examples
--------

>>> ser = pd.Series(
...     [1, 3, 2, 4, 3, 8],
...     index=pd.DatetimeIndex(
...         [
...             "2023-01-01",
...             "2023-01-10",
...             "2023-01-15",
...             "2023-02-01",
...             "2023-02-10",
...             "2023-02-15",
...         ]
...     ),
... )
>>> ser.resample("MS").sem()
2023-01-01    0.577350
2023-02-01    1.527525
Freq: MS, dtype: float64
        """
        pass
    @final
    def ohlc(self) -> DataFrame:
        """
Compute open, high, low and close values of a group, excluding missing values.

Returns
-------
DataFrame
    Open, high, low and close values within each group.

See Also
--------
DataFrame.agg : Aggregate using one or more operations over the specified axis.
DataFrame.resample : Resample time-series data.
DataFrame.groupby : Group DataFrame using a mapper or by a Series of columns.

Examples
--------
>>> ser = pd.Series(
...     [1, 3, 2, 4, 3, 5],
...     index=pd.DatetimeIndex(
...         [
...             "2023-01-01",
...             "2023-01-10",
...             "2023-01-15",
...             "2023-02-01",
...             "2023-02-10",
...             "2023-02-15",
...         ]
...     ),
... )
>>> ser.resample("MS").ohlc()
            open  high  low  close
2023-01-01     1     3    1      2
2023-02-01     4     5    3      5
        """
        pass
    @overload
    def nunique(self: Resampler[Series]) -> Series[int]:
        """
Return number of unique elements in the group.

Returns
-------
Series
    Number of unique values within each group.

See Also
--------
core.groupby.SeriesGroupBy.nunique : Method nunique for SeriesGroupBy.

Examples
--------
>>> ser = pd.Series(
...     [1, 2, 3, 3],
...     index=pd.DatetimeIndex(
...         ["2023-01-01", "2023-01-15", "2023-02-01", "2023-02-15"]
...     ),
... )
>>> ser
2023-01-01    1
2023-01-15    2
2023-02-01    3
2023-02-15    3
dtype: int64
>>> ser.resample("MS").nunique()
2023-01-01    2
2023-02-01    1
Freq: MS, dtype: int64
        """
        pass
    @overload
    def nunique(self: Resampler[DataFrame]) -> DataFrame: ...
    @final
    def size(self) -> Series[int]:
        """
Compute group sizes.

Returns
-------
Series
    Number of rows in each group.

See Also
--------
Series.groupby : Apply a function groupby to a Series.
DataFrame.groupby : Apply a function groupby to each row
    or column of a DataFrame.

Examples
--------
>>> ser = pd.Series(
...     [1, 2, 3],
...     index=pd.DatetimeIndex(["2023-01-01", "2023-01-15", "2023-02-01"]),
... )
>>> ser
2023-01-01    1
2023-01-15    2
2023-02-01    3
dtype: int64
>>> ser.resample("MS").size()
2023-01-01    2
2023-02-01    1
Freq: MS, dtype: int64
        """
        pass
    @overload
    def count(self: Resampler[Series]) -> Series[int]:
        """
Compute count of group, excluding missing values.

Returns
-------
Series or DataFrame
    Count of values within each group.

See Also
--------
Series.groupby : Apply a function groupby to a Series.
DataFrame.groupby : Apply a function groupby to each row
    or column of a DataFrame.

Examples
--------
>>> ser = pd.Series(
...     [1, 2, 3, 4],
...     index=pd.DatetimeIndex(
...         ["2023-01-01", "2023-01-15", "2023-02-01", "2023-02-15"]
...     ),
... )
>>> ser
2023-01-01    1
2023-01-15    2
2023-02-01    3
2023-02-15    4
dtype: int64
>>> ser.resample("MS").count()
2023-01-01    2
2023-02-01    2
Freq: MS, dtype: int64
        """
        pass
    @overload
    def count(self: Resampler[DataFrame]) -> DataFrame: ...
    @final
    def quantile(
        self,
        q: float | list[float] | np_ndarray_float | Series[float] = 0.5,
        **kwargs: Any,
    ) -> NDFrameT: ...

# We lie about inheriting from Resampler because at runtime inherits all Resampler
# attributes via setattr
class _GroupByMixin(Resampler[NDFrameT]):
    key: str | list[str] | None
    @override
    def __getitem__(self, key: str | list[str] | None, /) -> Self: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]

class DatetimeIndexResampler(Resampler[NDFrameT]): ...

class _InterpolateMixin:
    def interpolate(
        self,
        method: InterpolateOptions = ...,
        *,
        axis: Axis = ...,
        limit: int | None = ...,
        limit_direction: Literal["forward", "backward", "both"] = ...,
        limit_area: Literal["inside", "outside"] | None = ...,
        **kwargs: Any,
    ) -> Never: ...

class DatetimeIndexResamplerGroupby(
    _InterpolateMixin, _GroupByMixin[NDFrameT], DatetimeIndexResampler[NDFrameT]
):
    @final
    @override
    def __getattr__(self, attr: str, /) -> Self: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-override] # ty: ignore[invalid-method-override]

class PeriodIndexResampler(DatetimeIndexResampler[NDFrameT]): ...

class PeriodIndexResamplerGroupby(
    _InterpolateMixin, _GroupByMixin[NDFrameT], PeriodIndexResampler[NDFrameT]
):
    @final
    @override
    def __getattr__(self, attr: str, /) -> Self: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-override] # ty: ignore[invalid-method-override]

class TimedeltaIndexResampler(DatetimeIndexResampler[NDFrameT]): ...

class TimedeltaIndexResamplerGroupby(
    _InterpolateMixin, _GroupByMixin[NDFrameT], TimedeltaIndexResampler[NDFrameT]
):
    @final
    @override
    def __getattr__(self, attr: str, /) -> Self: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-override] # ty: ignore[invalid-method-override]

class TimeGrouper(Grouper):
    closed: Literal["left", "right"]
    label: Literal["left", "right"]
    kind: str | None
    convention: TimestampConvention
    how: str
    fill_method: str | None
    limit: int | None
    group_keys: bool
    origin: TimeGrouperOrigin
    offset: Timedelta | None
