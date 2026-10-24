from collections.abc import (
    Hashable,
    Sequence,
)
import datetime as dt
from typing import (
    Literal,
    Never,
    TypeAlias,
    overload,
    type_check_only,
)

import numpy as np
from numpy import typing as npt
import pandas as pd
from pandas import Index
from pandas._stubs_only import (
    OrderableScalarT,
    OrderableT,
    OrderableTimesT,
)
from pandas.core.indexes.extension import ExtensionIndex
from typing_extensions import override

from pandas._libs.interval import (
    Interval as Interval,
    IntervalMixin,
)
from pandas._libs.tslibs.timedeltas import Timedelta
from pandas._typing import (
    DatetimeLike,
    DtypeArg,
    Frequency,
    IntervalClosedType,
    IntervalT,
    MaskType,
    np_1darray_bool,
    np_ndarray_anyint,
    np_ndarray_bool,
    np_ndarray_dt,
    np_ndarray_int64,
    np_ndarray_intp,
    np_ndarray_td,
)

from pandas.core.dtypes.dtypes import IntervalDtype as IntervalDtype

_EdgesInt: TypeAlias = (
    Sequence[int]
    | np_ndarray_int64
    | npt.NDArray[np.int32]
    | np_ndarray_intp
    | pd.Series[int]
    | Index[int]
)
_EdgesFloat: TypeAlias = (
    Sequence[float] | npt.NDArray[np.float64] | pd.Series[float] | Index[float]
)
_EdgesTimestamp: TypeAlias = (
    Sequence[DatetimeLike] | np_ndarray_dt | pd.Series[pd.Timestamp] | pd.DatetimeIndex
)
_EdgesTimedelta: TypeAlias = (
    Sequence[pd.Timedelta] | np_ndarray_td | pd.Series[pd.Timedelta] | pd.TimedeltaIndex
)
_TimestampLike: TypeAlias = pd.Timestamp | np.datetime64 | dt.datetime
_TimedeltaLike: TypeAlias = pd.Timedelta | np.timedelta64 | dt.timedelta

@type_check_only
class _LengthDescriptor:
    @overload
    def __get__(
        self,
        instance: IntervalIndex[Interval[OrderableScalarT]],
        owner: type[IntervalIndex],
        /,
    ) -> Index[OrderableScalarT]: ...
    @overload
    def __get__(
        self,
        instance: IntervalIndex[Interval[OrderableTimesT]],
        owner: type[IntervalIndex],
        /,
    ) -> Index[Timedelta]: ...

@type_check_only
class _MidDescriptor:
    @overload
    def __get__(
        self, instance: IntervalIndex[Interval[int]], owner: type[IntervalIndex], /
    ) -> Index[float]: ...
    @overload
    def __get__(
        self,
        instance: IntervalIndex[Interval[OrderableT]],
        owner: type[IntervalIndex],
        /,
    ) -> Index[OrderableT]: ...

class IntervalIndex(ExtensionIndex[IntervalT, np.object_], IntervalMixin):
    closed: IntervalClosedType

    def __new__(
        cls,
        data: Sequence[IntervalT],
        closed: IntervalClosedType | None = None,
        dtype: IntervalDtype | None = None,
        copy: bool = False,
        name: Hashable = None,
        verify_integrity: bool = True,
    ) -> IntervalIndex[IntervalT]: ...
    @overload
    @classmethod
    def from_breaks(  # pyright: ignore[reportOverlappingOverload]
        cls,
        breaks: _EdgesInt,
        closed: IntervalClosedType | None = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[int]]:
        """
Construct an IntervalIndex from an array of splits.

Parameters
----------
breaks : array-like (1-dimensional)
    Left and right bounds for each interval.
closed : {'left', 'right', 'both', 'neither'}, default 'right'
    Whether the intervals are closed on the left-side, right-side, both
    or neither.
name : str, optional
    Name of the resulting IntervalIndex.
copy : bool, default False
    Copy the data.
dtype : dtype or None, default None
    If None, dtype will be inferred.

Returns
-------
IntervalIndex

See Also
--------
interval_range : Function to create a fixed frequency IntervalIndex.
IntervalIndex.from_arrays : Construct from a left and right array.
IntervalIndex.from_tuples : Construct from a sequence of tuples.

Examples
--------
>>> pd.IntervalIndex.from_breaks([0, 1, 2, 3])
IntervalIndex([(0, 1], (1, 2], (2, 3]],
              dtype='interval[int64, right]')
        """
        pass
    @overload
    @classmethod
    def from_breaks(
        cls,
        breaks: _EdgesFloat,
        closed: IntervalClosedType | None = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[float]]: ...
    @overload
    @classmethod
    def from_breaks(
        cls,
        breaks: _EdgesTimestamp,
        closed: IntervalClosedType | None = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[pd.Timestamp]]: ...
    @overload
    @classmethod
    def from_breaks(
        cls,
        breaks: _EdgesTimedelta,
        closed: IntervalClosedType | None = None,
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[pd.Timedelta]]: ...
    @overload
    @classmethod
    def from_arrays(  # pyright: ignore[reportOverlappingOverload]
        cls,
        left: _EdgesInt,
        right: _EdgesInt,
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[int]]:
        """
Construct from two arrays defining the left and right bounds.

Parameters
----------
left : array-like (1-dimensional)
    Left bounds for each interval.
right : array-like (1-dimensional)
    Right bounds for each interval.
closed : {'left', 'right', 'both', 'neither'}, default 'right'
    Whether the intervals are closed on the left-side, right-side, both
    or neither.
name : str, optional
    Name of the resulting IntervalIndex.
copy : bool, default False
    Copy the data.
dtype : dtype, optional
    If None, dtype will be inferred.

Returns
-------
IntervalIndex

Raises
------
ValueError
    When a value is missing in only one of `left` or `right`.
    When a value in `left` is greater than the corresponding value
    in `right`.

See Also
--------
interval_range : Function to create a fixed frequency IntervalIndex.
IntervalIndex.from_breaks : Construct an IntervalIndex from an array of
    splits.
IntervalIndex.from_tuples : Construct an IntervalIndex from an
    array-like of tuples.

Notes
-----
Each element of `left` must be less than or equal to the `right`
element at the same position. If an element is missing, it must be
missing in both `left` and `right`. A TypeError is raised when
using an unsupported type for `left` or `right`. At the moment,
'category', 'object', and 'string' subtypes are not supported.

Examples
--------
>>> pd.IntervalIndex.from_arrays([0, 1, 2], [1, 2, 3])
IntervalIndex([(0, 1], (1, 2], (2, 3]],
              dtype='interval[int64, right]')
        """
        pass
    @overload
    @classmethod
    def from_arrays(
        cls,
        left: _EdgesFloat,
        right: _EdgesFloat,
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[float]]: ...
    @overload
    @classmethod
    def from_arrays(
        cls,
        left: _EdgesTimestamp,
        right: _EdgesTimestamp,
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[pd.Timestamp]]: ...
    @overload
    @classmethod
    def from_arrays(
        cls,
        left: _EdgesTimedelta,
        right: _EdgesTimedelta,
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[Interval[pd.Timedelta]]: ...
    @overload
    @classmethod
    def from_tuples(  # pyright: ignore[reportOverlappingOverload]
        cls,
        data: Sequence[tuple[int, int]],
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[pd.Interval[int]]:
        """
Construct an IntervalIndex from an array-like of tuples.

Parameters
----------
data : array-like (1-dimensional)
    Array of tuples.
closed : {'left', 'right', 'both', 'neither'}, default 'right'
    Whether the intervals are closed on the left-side, right-side, both
    or neither.
name : str, optional
    Name of the resulting IntervalIndex.
copy : bool, default False
    By-default copy the data, this is compat only and ignored.
dtype : dtype or None, default None
    If None, dtype will be inferred.

Returns
-------
IntervalIndex

See Also
--------
interval_range : Function to create a fixed frequency IntervalIndex.
IntervalIndex.from_arrays : Construct an IntervalIndex from a left and
                            right array.
IntervalIndex.from_breaks : Construct an IntervalIndex from an array of
                            splits.

Examples
--------
>>> pd.IntervalIndex.from_tuples([(0, 1), (1, 2)])
IntervalIndex([(0, 1], (1, 2]],
               dtype='interval[int64, right]')
        """
        pass
    # Ignore misc here due to intentional overlap between int and float
    @overload
    @classmethod
    def from_tuples(
        cls,
        data: Sequence[tuple[float, float]],
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[pd.Interval[float]]: ...
    @overload
    @classmethod
    def from_tuples(
        cls,
        data: Sequence[
            tuple[pd.Timestamp, pd.Timestamp]
            | tuple[dt.datetime, dt.datetime]
            | tuple[np.datetime64, np.datetime64]
        ],
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[pd.Interval[pd.Timestamp]]: ...
    @overload
    @classmethod
    def from_tuples(
        cls,
        data: Sequence[
            tuple[pd.Timedelta, pd.Timedelta]
            | tuple[dt.timedelta, dt.timedelta]
            | tuple[np.timedelta64, np.timedelta64]
        ],
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: IntervalDtype | None = None,
    ) -> IntervalIndex[pd.Interval[pd.Timedelta]]: ...
    def to_tuples(self, na_tuple: bool = True) -> pd.Index: ...
    @overload
    @override
    def __contains__(self, key: IntervalT, /) -> bool: ...  # type: ignore[overload-overlap]
    @overload
    def __contains__(  # pyright: ignore[reportOverlappingOverload]
        self, key: object, /
    ) -> Literal[False]: ...
    @override
    def astype(self, dtype: DtypeArg, copy: bool = True) -> IntervalIndex: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-override] # ty: ignore[invalid-method-override]
    @property
    def is_overlapping(self) -> bool: ...
    @property
    def left(self: IntervalIndex[Interval[OrderableT]]) -> Index[OrderableT]: ...
    @property
    def right(self: IntervalIndex[Interval[OrderableT]]) -> Index[OrderableT]: ...
    mid = _MidDescriptor()
    length = _LengthDescriptor()
    @overload  # type: ignore[override]
    @override
    def __getitem__(  # pyrefly: ignore[bad-override]
        self,
        idx: (
            slice
            | np_ndarray_anyint
            | Sequence[int]
            | Index
            | MaskType
            | np_ndarray_bool
        ),
        /,
    ) -> IntervalIndex[IntervalT]: ...
    @overload
    def __getitem__(  # pyright: ignore[reportIncompatibleMethodOverride] # ty: ignore[invalid-method-override]
        self, idx: int, /
    ) -> IntervalT: ...
    @overload  # type: ignore[override]
    @override
    def __gt__(
        self, other: IntervalT | IntervalIndex[IntervalT], /
    ) -> np_1darray_bool: ...
    @overload
    def __gt__(  # pyright: ignore[reportIncompatibleMethodOverride] # ty: ignore[invalid-method-override]
        self, other: pd.Series[IntervalT], /
    ) -> pd.Series[bool]: ...
    @overload  # type: ignore[override]
    @override
    def __ge__(
        self, other: IntervalT | IntervalIndex[IntervalT], /
    ) -> np_1darray_bool: ...
    @overload
    def __ge__(  # pyright: ignore[reportIncompatibleMethodOverride] # ty: ignore[invalid-method-override]
        self, other: pd.Series[IntervalT], /
    ) -> pd.Series[bool]: ...
    @overload  # type: ignore[override]
    @override
    def __le__(
        self, other: IntervalT | IntervalIndex[IntervalT], /
    ) -> np_1darray_bool: ...
    @overload
    def __le__(  # pyright: ignore[reportIncompatibleMethodOverride] # ty: ignore[invalid-method-override]
        self, other: pd.Series[IntervalT], /
    ) -> pd.Series[bool]: ...
    @overload  # type: ignore[override]
    @override
    def __lt__(
        self, other: IntervalT | IntervalIndex[IntervalT], /
    ) -> np_1darray_bool: ...
    @overload
    def __lt__(  # pyright: ignore[reportIncompatibleMethodOverride] # ty: ignore[invalid-method-override]
        self, other: pd.Series[IntervalT], /
    ) -> pd.Series[bool]: ...
    @overload  # type: ignore[override]
    @override
    def __eq__(self, other: IntervalT | IntervalIndex[IntervalT], /) -> np_1darray_bool: ...  # type: ignore[overload-overlap] # pyrefly: ignore[bad-override]
    @overload
    def __eq__(self, other: pd.Series[IntervalT], /) -> pd.Series[bool]: ...  # type: ignore[overload-overlap]
    @overload
    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride,reportOverlappingOverload] # ty: ignore[invalid-method-override]
        self, other: object, /
    ) -> Literal[False]: ...
    @overload  # type: ignore[override]
    @override
    def __ne__(self, other: IntervalT | IntervalIndex[IntervalT], /) -> np_1darray_bool: ...  # type: ignore[overload-overlap] # pyrefly: ignore[bad-override]
    @overload
    def __ne__(self, other: pd.Series[IntervalT], /) -> pd.Series[bool]: ...  # type: ignore[overload-overlap]
    @overload
    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride,reportOverlappingOverload] # ty: ignore[invalid-method-override]
        self, other: object, /
    ) -> Literal[True]: ...
    @override
    def diff(self, periods: int = 1) -> Never: ...

# misc here because int and float overlap but interval has distinct types
# int gets hit first and so the correct type is returned
@overload
def interval_range(  # pyright: ignore[reportOverlappingOverload]
    start: int | None = None,
    end: int | None = None,
    periods: int | None = None,
    freq: int | None = None,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[int]]: ...
@overload
def interval_range(
    start: float | None = None,
    end: float | None = None,
    periods: int | None = None,
    freq: int | None = None,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[float]]: ...
@overload
def interval_range(
    start: _TimestampLike,
    end: _TimestampLike | None = None,
    periods: int | None = None,
    freq: Frequency | dt.timedelta | None = None,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[pd.Timestamp]]: ...
@overload
def interval_range(
    start: None = None,
    *,
    end: _TimestampLike,
    periods: int | None = None,
    freq: Frequency | dt.timedelta | None = None,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[pd.Timestamp]]: ...
@overload
def interval_range(
    start: None,
    end: _TimestampLike,
    periods: int,
    freq: Frequency | dt.timedelta,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[pd.Timestamp]]: ...
@overload
def interval_range(
    start: _TimedeltaLike,
    end: _TimedeltaLike | None = None,
    periods: int | None = None,
    freq: Frequency | dt.timedelta | None = None,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[pd.Timedelta]]: ...
@overload
def interval_range(
    start: None,
    end: _TimedeltaLike,
    periods: int,
    freq: Frequency | dt.timedelta,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[pd.Timedelta]]: ...
@overload
def interval_range(
    start: None = None,
    *,
    end: _TimedeltaLike,
    periods: int | None = None,
    freq: Frequency | dt.timedelta | None = None,
    name: Hashable = None,
    closed: IntervalClosedType = "right",
) -> IntervalIndex[Interval[pd.Timedelta]]: ...
