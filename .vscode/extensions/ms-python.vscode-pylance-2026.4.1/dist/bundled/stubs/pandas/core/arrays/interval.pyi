from collections.abc import Sequence
from typing import (
    Any,
    Self,
    TypeAlias,
    overload,
)

from pandas._stubs_only import OrderableT
from pandas.core.arrays.base import ExtensionArray as ExtensionArray
from pandas.core.indexes.base import Index
from pandas.core.series import Series
import pyarrow as pa
from typing_extensions import override

from pandas._libs.interval import (
    Interval as Interval,
    IntervalMixin as IntervalMixin,
)
from pandas._typing import (
    AnyArrayLike,
    DtypeArg,
    IntervalClosedType,
    NpDtype,
    Scalar,
    ScalarIndexer,
    SequenceIndexer,
    TakeIndexer,
    np_1darray_bool,
    np_1darray_object,
    np_ndarray,
)

from pandas.core.dtypes.dtypes import IntervalDtype

IntervalOrNA: TypeAlias = Interval | float

class IntervalArray(IntervalMixin, ExtensionArray):
    can_hold_na: bool = True
    def __new__(
        cls,
        data: Sequence[Interval[OrderableT]] | AnyArrayLike,
        closed: IntervalClosedType | None = None,
        dtype: DtypeArg | None = None,
        copy: bool = False,
        verify_integrity: bool = True,
    ) -> Self: ...
    @classmethod
    def from_breaks(
        cls,
        breaks: (
            Sequence[OrderableT]
            | np_ndarray
            | ExtensionArray
            | Index[OrderableT]
            | Series[OrderableT]
        ),
        closed: str = "right",
        copy: bool = False,
        dtype: DtypeArg | None = None,
    ) -> Self:
        """
Construct an IntervalArray from an array of splits.

Parameters
----------
breaks : array-like (1-dimensional)
    Left and right bounds for each interval.
closed : {'left', 'right', 'both', 'neither'}, default 'right'
    Whether the intervals are closed on the left-side, right-side, both
    or neither.
copy : bool, default False
    Copy the data.
dtype : dtype or None, default None
    If None, dtype will be inferred.

Returns
-------
IntervalArray

See Also
--------
interval_range : Function to create a fixed frequency IntervalIndex.
IntervalArray.from_arrays : Construct from a left and right array.
IntervalArray.from_tuples : Construct from a sequence of tuples.

Examples
--------
>>> pd.arrays.IntervalArray.from_breaks([0, 1, 2, 3])
<IntervalArray>
[(0, 1], (1, 2], (2, 3]]
Length: 3, dtype: interval[int64, right]
        """
        pass
    @classmethod
    def from_arrays(
        cls,
        left: (
            Sequence[OrderableT]
            | np_ndarray
            | ExtensionArray
            | Index[OrderableT]
            | Series[OrderableT]
        ),
        right: (
            Sequence[OrderableT]
            | np_ndarray
            | ExtensionArray
            | Index[OrderableT]
            | Series[OrderableT]
        ),
        closed: IntervalClosedType = "right",
        copy: bool = False,
        dtype: DtypeArg | None = None,
    ) -> Self:
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
copy : bool, default False
    Copy the data.
dtype : dtype, optional
    If None, dtype will be inferred.

Returns
-------
IntervalArray

Raises
------
ValueError
    When a value is missing in only one of `left` or `right`.
    When a value in `left` is greater than the corresponding value
    in `right`.

See Also
--------
interval_range : Function to create a fixed frequency IntervalIndex.
IntervalArray.from_breaks : Construct an IntervalArray from an array of
    splits.
IntervalArray.from_tuples : Construct an IntervalArray from an
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
>>> pd.arrays.IntervalArray.from_arrays([0, 1, 2], [1, 2, 3])
<IntervalArray>
[(0, 1], (1, 2], (2, 3]]
Length: 3, dtype: interval[int64, right]
        """
        pass
    @classmethod
    def from_tuples(
        cls,
        data: Sequence[tuple[OrderableT, OrderableT]] | np_ndarray,
        closed: IntervalClosedType = "right",
        copy: bool = False,
        dtype: DtypeArg | None = None,
    ) -> Self:
        """
Construct an IntervalArray from an array-like of tuples.

Parameters
----------
data : array-like (1-dimensional)
    Array of tuples.
closed : {'left', 'right', 'both', 'neither'}, default 'right'
    Whether the intervals are closed on the left-side, right-side, both
    or neither.
copy : bool, default False
    By-default copy the data, this is compat only and ignored.
dtype : dtype or None, default None
    If None, dtype will be inferred.

Returns
-------
IntervalArray

See Also
--------
interval_range : Function to create a fixed frequency IntervalIndex.
IntervalArray.from_arrays : Construct an IntervalArray from a left and
                            right array.
IntervalArray.from_breaks : Construct an IntervalArray from an array of
                            splits.

Examples
--------
>>> pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 2)])
<IntervalArray>
[(0, 1], (1, 2]]
Length: 2, dtype: interval[int64, right]
        """
        pass
    def __array__(
        self, dtype: NpDtype | None = None, copy: bool | None = None
    ) -> np_1darray_object: ...
    @overload
    @override
    def __getitem__(self, item: ScalarIndexer, /) -> IntervalOrNA: ...
    @overload
    def __getitem__(self, item: SequenceIndexer, /) -> Self: ...
    @override
    def __eq__(self, other: object, /) -> np_1darray_bool: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-override] # ty: ignore[invalid-method-override]
    @override
    def __ne__(self, other: object, /) -> np_1darray_bool: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-override] # ty: ignore[invalid-method-override]
    @property
    @override
    def dtype(self) -> IntervalDtype: ...
    @override
    def shift(self, periods: int = 1, fill_value: object = ...) -> IntervalArray: ...
    @override
    def take(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-param-name-override] # ty: ignore[invalid-method-override]
        self,
        indices: TakeIndexer,
        *,
        allow_fill: bool = False,
        fill_value: Interval | None = None,
        axis: None = None,  # only for compatibility, does nothing
        **kwargs: Any,
    ) -> Self: ...
    @property
    def left(self) -> Index: ...
    @property
    def right(self) -> Index: ...
    @property
    def closed(self) -> bool: ...
    def set_closed(self, closed: IntervalClosedType) -> Self:
        """
Return an identical IntervalArray closed on the specified side.

Parameters
----------
closed : {'left', 'right', 'both', 'neither'}
    Whether the intervals are closed on the left-side, right-side, both
    or neither.

Returns
-------
IntervalArray
    A new IntervalArray with the specified side closures.

See Also
--------
IntervalArray.closed : Returns inclusive side of the Interval.
arrays.IntervalArray.closed : Returns inclusive side of the IntervalArray.

Examples
--------
>>> index = pd.arrays.IntervalArray.from_breaks(range(4))
>>> index
<IntervalArray>
[(0, 1], (1, 2], (2, 3]]
Length: 3, dtype: interval[int64, right]
>>> index.set_closed("both")
<IntervalArray>
[[0, 1], [1, 2], [2, 3]]
Length: 3, dtype: interval[int64, both]
        """
        pass
    @property
    def length(self) -> Index: ...
    @property
    def mid(self) -> Index: ...
    @property
    def is_non_overlapping_monotonic(self) -> bool:
        """
Return a boolean whether the IntervalArray/IntervalIndex        is non-overlapping and monotonic.

Non-overlapping means (no Intervals share points), and monotonic means
either monotonic increasing or monotonic decreasing.

See Also
--------
overlaps : Check if two IntervalIndex objects overlap.

Examples
--------
For arrays:

>>> interv_arr = pd.arrays.IntervalArray([pd.Interval(0, 1), pd.Interval(1, 5)])
>>> interv_arr
<IntervalArray>
[(0, 1], (1, 5]]
Length: 2, dtype: interval[int64, right]
>>> interv_arr.is_non_overlapping_monotonic
True

>>> interv_arr = pd.arrays.IntervalArray(
...     [pd.Interval(0, 1), pd.Interval(-1, 0.1)]
... )
>>> interv_arr
<IntervalArray>
[(0.0, 1.0], (-1.0, 0.1]]
Length: 2, dtype: interval[float64, right]
>>> interv_arr.is_non_overlapping_monotonic
False

For Interval Index:

>>> interv_idx = pd.interval_range(start=0, end=2)
>>> interv_idx
IntervalIndex([(0, 1], (1, 2]], dtype='interval[int64, right]')
>>> interv_idx.is_non_overlapping_monotonic
True

>>> interv_idx = pd.interval_range(start=0, end=2, closed="both")
>>> interv_idx
IntervalIndex([[0, 1], [1, 2]], dtype='interval[int64, both]')
>>> interv_idx.is_non_overlapping_monotonic
False
        """
        pass
    def __arrow_array__(
        self, type: DtypeArg | None = None
    ) -> pa.ExtensionArray[Any]: ...
    def to_tuples(self, na_tuple: bool = True) -> np_1darray_object:
        """
Return an ndarray (if self is IntervalArray) or Index         (if self is IntervalIndex) of tuples of the form (left, right).

Parameters
----------
na_tuple : bool, default True
    If ``True``, return ``NA`` as a tuple ``(nan, nan)``. If ``False``,
    just return ``NA`` as ``nan``.

Returns
-------
ndarray or Index
    An ndarray of tuples representing the intervals
        if `self` is an IntervalArray.
    An Index of tuples representing the intervals
        if `self` is an IntervalIndex.

See Also
--------
IntervalArray.to_list : Convert IntervalArray to a list of tuples.
IntervalArray.to_numpy : Convert IntervalArray to a numpy array.
IntervalArray.unique : Find unique intervals in an IntervalArray.

Examples
--------
For :class:`pandas.IntervalArray`:

>>> idx = pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 2)])
>>> idx
<IntervalArray>
[(0, 1], (1, 2]]
Length: 2, dtype: interval[int64, right]
>>> idx.to_tuples()
array([(np.int64(0), np.int64(1)), (np.int64(1), np.int64(2))],
      dtype=object)

For :class:`pandas.IntervalIndex`:

>>> idx = pd.interval_range(start=0, end=2)
>>> idx
IntervalIndex([(0, 1], (1, 2]], dtype='interval[int64, right]')
>>> idx.to_tuples()
Index([(0, 1), (1, 2)], dtype='object')
        """
        pass
    @overload
    def contains(self, other: Series) -> Series[bool]:
        """
Check elementwise if the Intervals contain the value.

Return a boolean mask whether the value is contained in the Intervals
of the IntervalArray.

Parameters
----------
other : scalar
    The value to check whether it is contained in the Intervals.

Returns
-------
boolean array
    A boolean mask whether the value is contained in the Intervals.

See Also
--------
Interval.contains : Check whether Interval object contains value.
IntervalArray.overlaps : Check if an Interval overlaps the values in the
    IntervalArray.

Examples
--------
>>> intervals = pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 3), (2, 4)])
>>> intervals
<IntervalArray>
[(0, 1], (1, 3], (2, 4]]
Length: 3, dtype: interval[int64, right]

>>> intervals.contains(0.5)
array([ True, False, False])
        """
        pass
    @overload
    def contains(
        self, other: Scalar | ExtensionArray | Index | np_ndarray
    ) -> np_1darray_bool: ...
    def overlaps(self, other: Interval) -> np_1darray_bool:
        """
Check elementwise if an Interval overlaps the values in the IntervalArray.

Two intervals overlap if they share a common point, including closed
endpoints. Intervals that only have an open endpoint in common do not
overlap.

Parameters
----------
other : IntervalArray
    Interval to check against for an overlap.

Returns
-------
ndarray
    Boolean array positionally indicating where an overlap occurs.

See Also
--------
Interval.overlaps : Check whether two Interval objects overlap.

Examples
--------
>>> data = [(0, 1), (1, 3), (2, 4)]
>>> intervals = pd.arrays.IntervalArray.from_tuples(data)
>>> intervals
<IntervalArray>
[(0, 1], (1, 3], (2, 4]]
Length: 3, dtype: interval[int64, right]

>>> intervals.overlaps(pd.Interval(0.5, 1.5))
array([ True,  True, False])

Intervals that share closed endpoints overlap:

>>> intervals.overlaps(pd.Interval(1, 3, closed="left"))
array([ True,  True, True])

Intervals that only have an open endpoint in common do not overlap:

>>> intervals.overlaps(pd.Interval(1, 2, closed="right"))
array([False,  True, False])
        """
        pass
    @property
    @override
    def is_empty(self) -> np_1darray_bool: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride] # pyrefly: ignore[bad-override]
