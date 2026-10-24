from collections.abc import (
    Callable,
    Hashable,
    Iterator,
    Sequence,
)
import datetime as dt
from typing import (
    Any,
    Concatenate,
    Generic,
    Self,
    TypeAlias,
    overload,
)

from pandas import (
    DataFrame,
    Index,
    Series,
)
from pandas.core.indexers import BaseIndexer

from pandas._libs.tslibs import BaseOffset
from pandas._typing import (
    AggFuncTypeBase,
    AggFuncTypeFrame,
    AggFuncTypeSeriesToFrame,
    AxisInt,
    CalculationMethod,
    IntervalClosedType,
    NDFrameT,
    P,
    QuantileInterpolation,
    WindowingEngine,
    WindowingEngineKwargs,
    WindowingRankType,
)

class BaseWindow(Generic[NDFrameT]):
    on: str | Index | None
    closed: IntervalClosedType | None
    step: int | None
    window: int | dt.timedelta | str | BaseOffset | BaseIndexer | None
    min_periods: int | None
    center: bool | None
    win_type: str | None
    axis: AxisInt
    method: CalculationMethod
    def __getitem__(self, key: Hashable | Sequence[Hashable], /) -> Self: ...
    def __getattr__(self, attr: str, /) -> Self: ...
    def __iter__(self) -> Iterator[NDFrameT]: ...
    @overload
    def aggregate(  # pyright: ignore[reportOverlappingOverload]
        self: BaseWindow[Series],
        func: AggFuncTypeBase[...],
        *args: Any,
        **kwargs: Any,
    ) -> Series: ...
    @overload
    def aggregate(
        self: BaseWindow[Series],
        func: AggFuncTypeSeriesToFrame[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> DataFrame: ...
    @overload
    def aggregate(
        self: BaseWindow[DataFrame],
        func: AggFuncTypeFrame[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> DataFrame: ...
    agg = aggregate

class BaseWindowGroupby(BaseWindow[NDFrameT]): ...

class Window(BaseWindow[NDFrameT]):
    def sum(self, numeric_only: bool = False, **kwargs: Any) -> NDFrameT:
        """
Calculate the rolling weighted window sum.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

**kwargs
    Keyword arguments to configure the ``SciPy`` weighted window type.

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
Series.rolling : Calling rolling with Series data.
DataFrame.rolling : Calling rolling with DataFrames.
Series.sum : Aggregating sum for Series.
DataFrame.sum : Aggregating sum for DataFrame.

Examples
--------
>>> ser = pd.Series([0, 1, 5, 2, 8])

To get an instance of :class:`~pandas.core.window.rolling.Window` we need
to pass the parameter `win_type`.

>>> type(ser.rolling(2, win_type="gaussian"))
<class 'pandas.api.typing.Window'>

In order to use the `SciPy` Gaussian window we need to provide the parameters
`M` and `std`. The parameter `M` corresponds to 2 in our example.
We pass the second parameter `std` as a parameter of the following method
(`sum` in this case):

>>> ser.rolling(2, win_type="gaussian").sum(std=3)
0         NaN
1    0.986207
2    5.917243
3    6.903450
4    9.862071
dtype: float64
        """
        pass
    def mean(self, numeric_only: bool = False, **kwargs: Any) -> NDFrameT:
        """
Calculate the rolling weighted window mean.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

**kwargs
    Keyword arguments to configure the ``SciPy`` weighted window type.

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
Series.rolling : Calling rolling with Series data.
DataFrame.rolling : Calling rolling with DataFrames.
Series.mean : Aggregating mean for Series.
DataFrame.mean : Aggregating mean for DataFrame.

Examples
--------
>>> ser = pd.Series([0, 1, 5, 2, 8])

To get an instance of :class:`~pandas.core.window.rolling.Window` we need
to pass the parameter `win_type`.

>>> type(ser.rolling(2, win_type="gaussian"))
<class 'pandas.api.typing.Window'>

In order to use the `SciPy` Gaussian window we need to provide the parameters
`M` and `std`. The parameter `M` corresponds to 2 in our example.
We pass the second parameter `std` as a parameter of the following method:

>>> ser.rolling(2, win_type="gaussian").mean(std=3)
0    NaN
1    0.5
2    3.0
3    3.5
4    5.0
dtype: float64
        """
        pass
    def var(
        self, ddof: int = ..., numeric_only: bool = False, **kwargs: Any
    ) -> NDFrameT:
        """
Calculate the rolling weighted window variance.

Parameters
----------
ddof : int, default 1
    Delta Degrees of Freedom.  The divisor used in calculations
    is ``N - ddof``, where ``N`` represents the number of elements.
numeric_only : bool, default False
    Include only float, int, boolean columns.

**kwargs
    Keyword arguments to configure the ``SciPy`` weighted window type.

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
Series.rolling : Calling rolling with Series data.
DataFrame.rolling : Calling rolling with DataFrames.
Series.var : Aggregating var for Series.
DataFrame.var : Aggregating var for DataFrame.

Examples
--------
>>> ser = pd.Series([0, 1, 5, 2, 8])

To get an instance of :class:`~pandas.core.window.rolling.Window` we need
to pass the parameter `win_type`.

>>> type(ser.rolling(2, win_type="gaussian"))
<class 'pandas.api.typing.Window'>

In order to use the `SciPy` Gaussian window we need to provide the parameters
`M` and `std`. The parameter `M` corresponds to 2 in our example.
We pass the second parameter `std` as a parameter of the following method:

>>> ser.rolling(2, win_type="gaussian").var(std=3)
0     NaN
1     0.5
2     8.0
3     4.5
4    18.0
dtype: float64
        """
        pass
    def std(
        self, ddof: int = ..., numeric_only: bool = False, **kwargs: Any
    ) -> NDFrameT:
        """
Calculate the rolling weighted window standard deviation.

Parameters
----------
ddof : int, default 1
    Delta Degrees of Freedom.  The divisor used in calculations
    is ``N - ddof``, where ``N`` represents the number of elements.
numeric_only : bool, default False
    Include only float, int, boolean columns.

**kwargs
    Keyword arguments to configure the ``SciPy`` weighted window type.

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
Series.rolling : Calling rolling with Series data.
DataFrame.rolling : Calling rolling with DataFrames.
Series.std : Aggregating std for Series.
DataFrame.std : Aggregating std for DataFrame.

Examples
--------
>>> ser = pd.Series([0, 1, 5, 2, 8])

To get an instance of :class:`~pandas.core.window.rolling.Window` we need
to pass the parameter `win_type`.

>>> type(ser.rolling(2, win_type="gaussian"))
<class 'pandas.api.typing.Window'>

In order to use the `SciPy` Gaussian window we need to provide the parameters
`M` and `std`. The parameter `M` corresponds to 2 in our example.
We pass the second parameter `std` as a parameter of the following method:

>>> ser.rolling(2, win_type="gaussian").std(std=3)
0         NaN
1    0.707107
2    2.828427
3    2.121320
4    4.242641
dtype: float64
        """
        pass

_PipeCallable: TypeAlias = Callable[Concatenate[NDFrameT, P], Any]

class RollingAndExpandingMixin(BaseWindow[NDFrameT]):
    def count(self, numeric_only: bool = ...) -> NDFrameT: ...
    def apply(
        self,
        func: Callable[..., Any],
        raw: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
        args: tuple[Any, ...] | None = ...,
        kwargs: dict[str, Any] | None = ...,
    ) -> NDFrameT: ...
    def sum(
        self,
        numeric_only: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT: ...
    def max(
        self,
        numeric_only: bool = ...,
        *args: Any,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT: ...
    def min(
        self,
        numeric_only: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT: ...
    def mean(
        self,
        numeric_only: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT: ...
    def median(
        self,
        numeric_only: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT: ...
    def std(
        self,
        ddof: int = ...,
        numeric_only: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT: ...
    def var(
        self,
        ddof: int = ...,
        numeric_only: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT: ...
    def skew(self, numeric_only: bool = ...) -> NDFrameT: ...
    def sem(self, ddof: int = ..., numeric_only: bool = ...) -> NDFrameT: ...
    def kurt(self, numeric_only: bool = ...) -> NDFrameT: ...
    def quantile(
        self,
        q: float,
        interpolation: QuantileInterpolation = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT: ...
    def rank(
        self,
        method: WindowingRankType = ...,
        ascending: bool = ...,
        pct: bool = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT: ...
    def cov(
        self,
        other: DataFrame | Series | None = ...,
        pairwise: bool | None = ...,
        ddof: int = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT: ...
    def corr(
        self,
        other: DataFrame | Series | None = ...,
        pairwise: bool | None = ...,
        ddof: int = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT: ...
    def first(self, numeric_only: bool = False) -> NDFrameT: ...
    def last(self, numeric_only: bool = False) -> NDFrameT: ...
    def nunique(self, numeric_only: bool = False) -> NDFrameT: ...
    @overload
    def pipe(
        self, func: _PipeCallable[NDFrameT, P], *args: P.args, **kwargs: P.kwargs
    ) -> NDFrameT: ...
    @overload
    def pipe(
        self,
        func: tuple[_PipeCallable[NDFrameT, P], str],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> NDFrameT: ...

class Rolling(RollingAndExpandingMixin[NDFrameT]): ...
class RollingGroupby(BaseWindowGroupby[NDFrameT], Rolling[NDFrameT]): ...
