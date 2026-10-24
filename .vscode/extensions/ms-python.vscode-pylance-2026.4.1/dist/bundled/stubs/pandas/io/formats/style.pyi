from collections.abc import (
    Callable,
    Hashable,
    MutableMapping,
    Sequence,
)
from typing import (
    Any,
    Concatenate,
    Literal,
    Self,
    overload,
)

from matplotlib.colors import Colormap
from openpyxl.workbook.workbook import Workbook as OpenXlWorkbook
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from xlsxwriter import (  # pyright: ignore[reportMissingTypeStubs]
    Workbook as XlsxWorkbook,
)

from pandas._typing import (
    Axis,
    ExcelWriterMergeCells,
    FilePath,
    HashableT,
    HashableT1,
    HashableT2,
    IndexLabel,
    IntervalClosedType,
    Level,
    P,
    QuantileInterpolation,
    Scalar,
    StorageOptions,
    T,
    WriteBuffer,
    WriteExcelBuffer,
    np_ndarray,
    np_ndarray_str,
)

from pandas.io.excel import ExcelWriter
from pandas.io.formats.style_render import (
    CSSProperties,
    CSSStyles,
    ExtFormatter,
    StyleExportDict,
    StylerRenderer,
    Subset,
)

class Styler(StylerRenderer):
    def __init__(
        self,
        data: DataFrame | Series,
        precision: int | None = ...,
        table_styles: CSSStyles | None = ...,
        uuid: str | None = ...,
        caption: str | tuple[str, str] | None = ...,
        table_attributes: str | None = ...,
        cell_ids: bool = ...,
        na_rep: str | None = ...,
        uuid_len: int = ...,
        decimal: str | None = ...,
        thousands: str | None = ...,
        escape: str | None = ...,
        formatter: ExtFormatter | None = ...,
    ) -> None: ...
    def concat(self, other: Styler) -> Styler: ...
    def map(
        self,
        func: (
            Callable[[Scalar], str | None]
            | Callable[Concatenate[Scalar, ...], str | None]
        ),
        subset: Subset[Hashable] | None = ...,
        **kwargs: Any,
    ) -> Styler: ...
    def set_tooltips(
        self,
        ttips: DataFrame,
        props: CSSProperties | None = None,
        css_class: str | None = None,
        as_title_attribute: bool = False,
    ) -> Styler: ...
    def to_excel(
        self,
        excel_writer: (
            FilePath | WriteExcelBuffer | ExcelWriter[OpenXlWorkbook | XlsxWorkbook]
        ),
        sheet_name: str = "Sheet1",
        na_rep: str = "",
        float_format: str | None = None,
        columns: list[HashableT1] | None = None,
        header: list[HashableT2] | bool = True,
        index: bool = True,
        index_label: IndexLabel | None = None,
        startrow: int = 0,
        startcol: int = 0,
        engine: Literal["openpyxl", "xlsxwriter"] | None = None,
        merge_cells: ExcelWriterMergeCells = True,
        encoding: str | None = None,
        inf_rep: str = "inf",
        verbose: bool = True,
        freeze_panes: tuple[int, int] | None = None,
        storage_options: StorageOptions | None = None,
    ) -> None:
        """
Write Styler to an Excel sheet.

To write a single Styler to an Excel .xlsx file it is only necessary to
specify a target file name. To write to multiple sheets it is necessary to
create an `ExcelWriter` object with a target file name, and specify a sheet
in the file to write to.

Multiple sheets may be written to by specifying unique `sheet_name`.
With all data written to the file it is necessary to save the changes.
Note that creating an `ExcelWriter` object with a file name that already exists
will overwrite the existing file because the default mode is write.

Parameters
----------
excel_writer : path-like, file-like, or ExcelWriter object
    File path or existing ExcelWriter.
sheet_name : str, default 'Sheet1'
    Name of sheet which will contain DataFrame.
na_rep : str, default ''
    Missing data representation.
float_format : str, optional
    Format string for floating point numbers. For example
    ``float_format="%.2f"`` will format 0.1234 to 0.12.
columns : sequence or list of str, optional
    Columns to write.
header : bool or list of str, default True
    Write out the column names. If a list of string is given it is
    assumed to be aliases for the column names.
index : bool, default True
    Write row names (index).
index_label : str or sequence, optional
    Column label for index column(s) if desired. If not specified, and
    `header` and `index` are True, then the index names are used. A
    sequence should be given if the DataFrame uses MultiIndex.
startrow : int, default 0
    Upper left cell row to dump data frame.
startcol : int, default 0
    Upper left cell column to dump data frame.
engine : str, optional
    Write engine to use, 'openpyxl' or 'xlsxwriter'. You can also set this
    via the options ``io.excel.xlsx.writer`` or
    ``io.excel.xlsm.writer``.
merge_cells : bool or 'columns', default False
    If True, write MultiIndex index and columns as merged cells.
    If 'columns', merge MultiIndex column cells only.
encoding : str or None, default None
    Unused parameter, present for compatibility.
inf_rep : str, default 'inf'
    Representation for infinity (there is no native representation for
    infinity in Excel).
verbose : str, default True
    Optional unused parameter, present for compatibility.
freeze_panes : tuple of int (length 2), optional
    Specifies the one-based bottommost row and rightmost column that
    is to be frozen.
storage_options : dict, optional
    Extra options that make sense for a particular storage connection, e.g.
    host, port, username, password, etc. For HTTP(S) URLs the key-value pairs
    are forwarded to ``urllib.request.Request`` as header options. For other
    URLs (e.g. starting with "s3://", and "gcs://") the key-value pairs are
    forwarded to ``fsspec.open``. Please see ``fsspec`` and ``urllib`` for more
    details, and for more examples on storage options refer `here
    <https://pandas.pydata.org/docs/user_guide/io.html?
    highlight=storage_options#reading-writing-remote-files>`_.

autofilter : bool, default False
    If True, add automatic filters to all columns.

See Also
--------
to_csv : Write DataFrame to a comma-separated values (csv) file.
ExcelWriter : Class for writing DataFrame objects into excel sheets.
read_excel : Read an Excel file into a pandas DataFrame.
read_csv : Read a comma-separated values (csv) file into DataFrame.
io.formats.style.Styler.to_excel : Add styles to Excel sheet.

Notes
-----
For compatibility with :meth:`~DataFrame.to_csv`,
to_excel serializes lists and dicts to strings before writing.

Once a workbook has been saved it is not possible to write further
data without rewriting the whole workbook.

pandas will check the number of rows, columns,
and cell character count does not exceed Excel's limitations.
All other limitations must be checked by the user.

Examples
--------

Create, write to and save a workbook:

>>> df1 = pd.DataFrame(
...     [["a", "b"], ["c", "d"]],
...     index=["row 1", "row 2"],
...     columns=["col 1", "col 2"],
... )
>>> df1.to_excel("output.xlsx")  # doctest: +SKIP

To specify the sheet name:

>>> df1.to_excel("output.xlsx", sheet_name="Sheet_name_1")  # doctest: +SKIP

If you wish to write to more than one sheet in the workbook, it is
necessary to specify an ExcelWriter object:

>>> df2 = df1.copy()
>>> with pd.ExcelWriter("output.xlsx") as writer:  # doctest: +SKIP
...     df1.to_excel(writer, sheet_name="Sheet_name_1")
...     df2.to_excel(writer, sheet_name="Sheet_name_2")

ExcelWriter can also be used to append to an existing Excel file:

>>> with pd.ExcelWriter("output.xlsx", mode="a") as writer:  # doctest: +SKIP
...     df1.to_excel(writer, sheet_name="Sheet_name_3")

To set the library that is used to write the Excel file,
you can pass the `engine` keyword (the default engine is
automatically chosen depending on the file extension):

>>> df1.to_excel("output1.xlsx", engine="xlsxwriter")  # doctest: +SKIP
        """
        pass
    @overload
    def to_latex(
        self,
        buf: FilePath | WriteBuffer[str],
        *,
        column_format: str | None = ...,
        position: str | None = ...,
        position_float: Literal["centering", "raggedleft", "raggedright"] | None = ...,
        hrules: bool | None = ...,
        clines: (
            Literal["all;data", "all;index", "skip-last;data", "skip-last;index"] | None
        ) = ...,
        label: str | None = ...,
        caption: str | tuple[str, str] | None = ...,
        sparse_index: bool | None = ...,
        sparse_columns: bool | None = ...,
        multirow_align: Literal["c", "t", "b", "naive"] | None = ...,
        multicol_align: Literal["r", "c", "l", "naive-l", "naive-r"] | None = ...,
        siunitx: bool = ...,
        environment: str | None = ...,
        encoding: str | None = ...,
        convert_css: bool = ...,
    ) -> None: ...
    @overload
    def to_latex(
        self,
        buf: None = None,
        *,
        column_format: str | None = ...,
        position: str | None = ...,
        position_float: Literal["centering", "raggedleft", "raggedright"] | None = ...,
        hrules: bool | None = ...,
        clines: (
            Literal["all;data", "all;index", "skip-last;data", "skip-last;index"] | None
        ) = ...,
        label: str | None = ...,
        caption: str | tuple[str, str] | None = ...,
        sparse_index: bool | None = ...,
        sparse_columns: bool | None = ...,
        multirow_align: Literal["c", "t", "b", "naive"] | None = ...,
        multicol_align: Literal["r", "c", "l", "naive-l", "naive-r"] | None = ...,
        siunitx: bool = ...,
        environment: str | None = ...,
        encoding: str | None = ...,
        convert_css: bool = ...,
    ) -> str: ...
    @overload
    def to_typst(
        self,
        buf: FilePath | WriteBuffer[str],
        *,
        encoding: str | None = None,
        sparse_index: bool | None = None,
        sparse_columns: bool | None = None,
        max_rows: int | None = None,
        max_columns: int | None = None,
    ) -> None: ...
    @overload
    def to_typst(
        self,
        buf: None = None,
        *,
        encoding: str | None = None,
        sparse_index: bool | None = None,
        sparse_columns: bool | None = None,
        max_rows: int | None = None,
        max_columns: int | None = None,
    ) -> str: ...
    @overload
    def to_html(
        self,
        buf: FilePath | WriteBuffer[str],
        *,
        table_uuid: str | None = ...,
        table_attributes: str | None = ...,
        sparse_index: bool | None = ...,
        sparse_columns: bool | None = ...,
        bold_headers: bool = ...,
        caption: str | None = ...,
        max_rows: int | None = ...,
        max_columns: int | None = ...,
        encoding: str | None = ...,
        doctype_html: bool = ...,
        exclude_styles: bool = ...,
        **kwargs: Any,
    ) -> None: ...
    @overload
    def to_html(
        self,
        buf: None = None,
        *,
        table_uuid: str | None = ...,
        table_attributes: str | None = ...,
        sparse_index: bool | None = ...,
        sparse_columns: bool | None = ...,
        bold_headers: bool = ...,
        caption: str | None = ...,
        max_rows: int | None = ...,
        max_columns: int | None = ...,
        encoding: str | None = ...,
        doctype_html: bool = ...,
        exclude_styles: bool = ...,
        **kwargs: Any,
    ) -> str: ...
    @overload
    def to_string(
        self,
        buf: FilePath | WriteBuffer[str],
        *,
        encoding: str | None = ...,
        sparse_index: bool | None = ...,
        sparse_columns: bool | None = ...,
        max_rows: int | None = ...,
        max_columns: int | None = ...,
        delimiter: str = ...,
    ) -> None: ...
    @overload
    def to_string(
        self,
        buf: None = None,
        *,
        encoding: str | None = ...,
        sparse_index: bool | None = ...,
        sparse_columns: bool | None = ...,
        max_rows: int | None = ...,
        max_columns: int | None = ...,
        delimiter: str = ...,
    ) -> str: ...
    def set_td_classes(self, classes: DataFrame) -> Styler: ...
    def __copy__(self) -> Styler: ...
    def __deepcopy__(self, memo: MutableMapping[int, Any] | None, /) -> Styler: ...
    def clear(self) -> None: ...
    @overload
    def apply(
        self,
        func: (
            Callable[[Series], list[Any] | Series]
            | Callable[Concatenate[Series, ...], list[Any] | Series]
        ),
        axis: Axis = ...,
        subset: Subset[Hashable] | None = ...,
        **kwargs: Any,
    ) -> Styler: ...
    @overload
    def apply(
        self,
        func: (
            Callable[[DataFrame], np_ndarray | DataFrame]
            | Callable[Concatenate[DataFrame, ...], np_ndarray | DataFrame]
        ),
        axis: None,
        subset: Subset[Hashable] | None = ...,
        **kwargs: Any,
    ) -> Styler: ...
    def apply_index(
        self,
        func: (
            Callable[[Series], list[str] | np_ndarray_str | Series[str]]
            | Callable[
                Concatenate[Series, ...], list[str] | np_ndarray_str | Series[str]
            ]
        ),
        axis: Axis = ...,
        level: Level | list[Level] | None = ...,
        **kwargs: Any,
    ) -> Styler:
        """
Apply a CSS-styling function to the index or column headers, level-wise.

Updates the HTML representation with the result.

.. versionadded:: 2.1.0
   Styler.applymap_index was deprecated and renamed to Styler.map_index.

Parameters
----------
func : function
    ``func`` should take a Series and return a string array of the same length.
axis : {0, 1, "index", "columns"}
    The headers over which to apply the function.
level : int, str, list, optional
    If index is MultiIndex the level(s) over which to apply the function.
**kwargs : dict
    Pass along to ``func``.

Returns
-------
Styler
    Instance of class with CSS applied to its HTML representation.

See Also
--------
Styler.map_index: Apply a CSS-styling function to headers elementwise.
Styler.apply: Apply a CSS-styling function column-wise, row-wise, or table-wise.
Styler.map: Apply a CSS-styling function elementwise.

Notes
-----
Each input to ``func`` will be the index as a Series, if an Index, or a level
of a MultiIndex. The output of ``func`` should be an identically sized array
of CSS styles as strings, in the format
'attribute: value; attribute2: value2; ...' or, if nothing is to be applied
to that element, an empty string or ``None``.

Examples
--------
Basic usage to conditionally highlight values in the index.

>>> df = pd.DataFrame([[1, 2], [3, 4]], index=["A", "B"])
>>> def color_b(label):
...     return np.where(label == "B", "background-color: yellow;", "")
>>> df.style.apply_index(color_b)  # doctest: +SKIP

.. figure:: ../../_static/style/appmaphead1.png

Selectively applying to specific levels of MultiIndex columns.

>>> midx = pd.MultiIndex.from_product([["ix", "jy"], [0, 1], ["x3", "z4"]])
>>> df = pd.DataFrame([np.arange(8)], columns=midx)
>>> def highlight_x(label):
...     return ["background-color: yellow;" if "x" in v else "" for v in label]
>>> df.style.apply_index(
...     highlight_x, axis="columns", level=[0, 2]
... )  # doctest: +SKIP

.. figure:: ../../_static/style/appmaphead2.png
        """
        pass
    def map_index(
        self,
        func: (
            Callable[[Scalar], str | None]
            | Callable[Concatenate[Scalar, ...], str | None]
        ),
        axis: Axis = ...,
        level: Level | list[Level] | None = ...,
        **kwargs: Any,
    ) -> Styler:
        """
Apply a CSS-styling function to the index or column headers, elementwise.

Updates the HTML representation with the result.

.. versionadded:: 2.1.0
   Styler.applymap_index was deprecated and renamed to Styler.map_index.

Parameters
----------
func : function
    ``func`` should take a scalar and return a string.
axis : {0, 1, "index", "columns"}
    The headers over which to apply the function.
level : int, str, list, optional
    If index is MultiIndex the level(s) over which to apply the function.
**kwargs : dict
    Pass along to ``func``.

Returns
-------
Styler
    Instance of class with CSS applied to its HTML representation.

See Also
--------
Styler.apply_index: Apply a CSS-styling function to headers level-wise.
Styler.apply: Apply a CSS-styling function column-wise, row-wise, or table-wise.
Styler.map: Apply a CSS-styling function elementwise.

Notes
-----
Each input to ``func`` will be an index value, if an Index, or a level value of
a MultiIndex. The output of ``func`` should be CSS styles as a string, in the
format 'attribute: value; attribute2: value2; ...' or, if nothing is to be
applied to that element, an empty string or ``None``.

Examples
--------
Basic usage to conditionally highlight values in the index.

>>> df = pd.DataFrame([[1, 2], [3, 4]], index=["A", "B"])
>>> def color_b(label):
...     return "background-color: yellow;" if label == "B" else None
>>> df.style.map_index(color_b)  # doctest: +SKIP

.. figure:: ../../_static/style/appmaphead1.png

Selectively applying to specific levels of MultiIndex columns.

>>> midx = pd.MultiIndex.from_product([["ix", "jy"], [0, 1], ["x3", "z4"]])
>>> df = pd.DataFrame([np.arange(8)], columns=midx)
>>> def highlight_x(label):
...     return "background-color: yellow;" if "x" in label else None
>>> df.style.map_index(
...     highlight_x, axis="columns", level=[0, 2]
... )  # doctest: +SKIP

.. figure:: ../../_static/style/appmaphead2.png
        """
        pass
    def set_table_attributes(self, attributes: str) -> Styler: ...
    def export(self) -> StyleExportDict: ...
    def use(self, styles: StyleExportDict) -> Styler: ...
    def set_uuid(self, uuid: str) -> Styler: ...
    def set_caption(self, caption: str | tuple[str, str]) -> Styler: ...
    def set_sticky(
        self,
        axis: Axis = 0,
        pixel_size: int | None = None,
        levels: Level | list[Level] | None = None,
    ) -> Styler: ...
    def set_table_styles(
        self,
        table_styles: dict[HashableT, CSSStyles] | CSSStyles | None = None,
        axis: Axis = 0,
        overwrite: bool = True,
        css_class_names: dict[str, str] | None = None,
    ) -> Styler: ...
    def hide(
        self,
        subset: Subset[Hashable] | None = ...,
        axis: Axis = ...,
        level: Level | list[Level] | None = ...,
        names: bool = ...,
    ) -> Styler: ...
    def background_gradient(
        self,
        cmap: str | Colormap = "PuBu",
        low: float = 0,
        high: float = 0,
        axis: Axis | None = 0,
        subset: Subset[Hashable] | None = None,
        text_color_threshold: float = 0.408,
        vmin: float | None = None,
        vmax: float | None = None,
        gmap: (
            Sequence[float]
            | Sequence[Sequence[float]]
            | np_ndarray
            | DataFrame
            | Series
            | None
        ) = None,
    ) -> Styler:
        """
Color the background in a gradient style.

The background color is determined according
to the data in each column, row or frame, or by a given
gradient map. Requires matplotlib.

Parameters
----------
cmap : str or colormap
    Matplotlib colormap.
low : float
    Compress the color range at the low end. This is a multiple of the data
    range to extend below the minimum; good values usually in [0, 1],
    defaults to 0.
high : float
    Compress the color range at the high end. This is a multiple of the data
    range to extend above the maximum; good values usually in [0, 1],
    defaults to 0.
axis : {0, 1, "index", "columns", None}, default 0
    Apply to each column (``axis=0`` or ``'index'``), to each row
    (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
    with ``axis=None``.
subset : label, array-like, IndexSlice, optional
    A valid 2d input to `DataFrame.loc[<subset>]`, or, in the case of a 1d input
    or single key, to `DataFrame.loc[:, <subset>]` where the columns are
    prioritised, to limit ``data`` to *before* applying the function.
text_color_threshold : float or int
    Luminance threshold for determining text color in [0, 1]. Facilitates text
    visibility across varying background colors. All text is dark if 0, and
    light if 1, defaults to 0.408.
vmin : float, optional
    Minimum data value that corresponds to colormap minimum value.
    If not specified the minimum value of the data (or gmap) will be used.
vmax : float, optional
    Maximum data value that corresponds to colormap maximum value.
    If not specified the maximum value of the data (or gmap) will be used.
gmap : array-like, optional
    Gradient map for determining the background colors. If not supplied
    will use the underlying data from rows, columns or frame. If given as an
    ndarray or list-like must be an identical shape to the underlying data
    considering ``axis`` and ``subset``. If given as DataFrame or Series must
    have same index and column labels considering ``axis`` and ``subset``.
    If supplied, ``vmin`` and ``vmax`` should be given relative to this
    gradient map.

Returns
-------
Styler
    Instance of class with background colored in gradient style.

See Also
--------
Styler.text_gradient: Color the text in a gradient style.

Notes
-----
When using ``low`` and ``high`` the range
of the gradient, given by the data if ``gmap`` is not given or by ``gmap``,
is extended at the low end effectively by
`map.min - low * map.range` and at the high end by
`map.max + high * map.range` before the colors are normalized and determined.

If combining with ``vmin`` and ``vmax`` the `map.min`, `map.max` and
`map.range` are replaced by values according to the values derived from
``vmin`` and ``vmax``.

This method will preselect numeric columns and ignore non-numeric columns
unless a ``gmap`` is supplied in which case no preselection occurs.

Examples
--------
>>> df = pd.DataFrame(
...     columns=["City", "Temp (c)", "Rain (mm)", "Wind (m/s)"],
...     data=[
...         ["Stockholm", 21.6, 5.0, 3.2],
...         ["Oslo", 22.4, 13.3, 3.1],
...         ["Copenhagen", 24.5, 0.0, 6.7],
...     ],
... )

Shading the values column-wise, with ``axis=0``, preselecting numeric columns

>>> df.style.background_gradient(axis=0)  # doctest: +SKIP

.. figure:: ../../_static/style/bg_ax0.png

Shading all values collectively using ``axis=None``

>>> df.style.background_gradient(axis=None)  # doctest: +SKIP

.. figure:: ../../_static/style/bg_axNone.png

Compress the color map from the both ``low`` and ``high`` ends

>>> df.style.background_gradient(
...     axis=None, low=0.75, high=1.0
... )  # doctest: +SKIP

.. figure:: ../../_static/style/bg_axNone_lowhigh.png

Manually setting ``vmin`` and ``vmax`` gradient thresholds

>>> df.style.background_gradient(
...     axis=None, vmin=6.7, vmax=21.6
... )  # doctest: +SKIP

.. figure:: ../../_static/style/bg_axNone_vminvmax.png

Setting a ``gmap`` and applying to all columns with another ``cmap``

>>> df.style.background_gradient(axis=0, gmap=df["Temp (c)"], cmap="YlOrRd")
... # doctest: +SKIP

.. figure:: ../../_static/style/bg_gmap.png

Setting the gradient map for a dataframe (i.e. ``axis=None``), we need to
explicitly state ``subset`` to match the ``gmap`` shape

>>> gmap = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
>>> df.style.background_gradient(
...     axis=None,
...     gmap=gmap,
...     cmap="YlOrRd",
...     subset=["Temp (c)", "Rain (mm)", "Wind (m/s)"],
... )  # doctest: +SKIP

.. figure:: ../../_static/style/bg_axNone_gmap.png
        """
        pass
    def text_gradient(
        self,
        cmap: str | Colormap = "PuBu",
        low: float = 0,
        high: float = 0,
        axis: Axis | None = 0,
        subset: Subset[Hashable] | None = None,
        vmin: float | None = None,
        vmax: float | None = None,
        gmap: (
            Sequence[float]
            | Sequence[Sequence[float]]
            | np_ndarray
            | DataFrame
            | Series
            | None
        ) = None,
    ) -> Styler:
        """
Color the text in a gradient style.

The text color is determined according
to the data in each column, row or frame, or by a given
gradient map. Requires matplotlib.

Parameters
----------
cmap : str or colormap
    Matplotlib colormap.
low : float
    Compress the color range at the low end. This is a multiple of the data
    range to extend below the minimum; good values usually in [0, 1],
    defaults to 0.
high : float
    Compress the color range at the high end. This is a multiple of the data
    range to extend above the maximum; good values usually in [0, 1],
    defaults to 0.
axis : {0, 1, "index", "columns", None}, default 0
    Apply to each column (``axis=0`` or ``'index'``), to each row
    (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
    with ``axis=None``.
subset : label, array-like, IndexSlice, optional
    A valid 2d input to `DataFrame.loc[<subset>]`, or, in the case of a 1d input
    or single key, to `DataFrame.loc[:, <subset>]` where the columns are
    prioritised, to limit ``data`` to *before* applying the function.
vmin : float, optional
    Minimum data value that corresponds to colormap minimum value.
    If not specified the minimum value of the data (or gmap) will be used.
vmax : float, optional
    Maximum data value that corresponds to colormap maximum value.
    If not specified the maximum value of the data (or gmap) will be used.
gmap : array-like, optional
    Gradient map for determining the text colors. If not supplied
    will use the underlying data from rows, columns or frame. If given as an
    ndarray or list-like must be an identical shape to the underlying data
    considering ``axis`` and ``subset``. If given as DataFrame or Series must
    have same index and column labels considering ``axis`` and ``subset``.
    If supplied, ``vmin`` and ``vmax`` should be given relative to this
    gradient map.

Returns
-------
Styler
    Instance of class with background colored in gradient style.

See Also
--------
Styler.background_gradient: Color the background in a gradient style.

Notes
-----
When using ``low`` and ``high`` the range
of the gradient, given by the data if ``gmap`` is not given or by ``gmap``,
is extended at the low end effectively by
`map.min - low * map.range` and at the high end by
`map.max + high * map.range` before the colors are normalized and determined.

If combining with ``vmin`` and ``vmax`` the `map.min`, `map.max` and
`map.range` are replaced by values according to the values derived from
``vmin`` and ``vmax``.

This method will preselect numeric columns and ignore non-numeric columns
unless a ``gmap`` is supplied in which case no preselection occurs.

Examples
--------
>>> df = pd.DataFrame(
...     columns=["City", "Temp (c)", "Rain (mm)", "Wind (m/s)"],
...     data=[
...         ["Stockholm", 21.6, 5.0, 3.2],
...         ["Oslo", 22.4, 13.3, 3.1],
...         ["Copenhagen", 24.5, 0.0, 6.7],
...     ],
... )

Shading the values column-wise, with ``axis=0``, preselecting numeric columns

>>> df.style.text_gradient(axis=0)  # doctest: +SKIP

.. figure:: ../../_static/style/tg_ax0.png

Shading all values collectively using ``axis=None``

>>> df.style.text_gradient(axis=None)  # doctest: +SKIP

.. figure:: ../../_static/style/tg_axNone.png

Compress the color map from the both ``low`` and ``high`` ends

>>> df.style.text_gradient(axis=None, low=0.75, high=1.0)  # doctest: +SKIP

.. figure:: ../../_static/style/tg_axNone_lowhigh.png

Manually setting ``vmin`` and ``vmax`` gradient thresholds

>>> df.style.text_gradient(axis=None, vmin=6.7, vmax=21.6)  # doctest: +SKIP

.. figure:: ../../_static/style/tg_axNone_vminvmax.png

Setting a ``gmap`` and applying to all columns with another ``cmap``

>>> df.style.text_gradient(axis=0, gmap=df["Temp (c)"], cmap="YlOrRd")
... # doctest: +SKIP

.. figure:: ../../_static/style/tg_gmap.png

Setting the gradient map for a dataframe (i.e. ``axis=None``), we need to
explicitly state ``subset`` to match the ``gmap`` shape

>>> gmap = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
>>> df.style.text_gradient(
...     axis=None,
...     gmap=gmap,
...     cmap="YlOrRd",
...     subset=["Temp (c)", "Rain (mm)", "Wind (m/s)"],
... )  # doctest: +SKIP

.. figure:: ../../_static/style/tg_axNone_gmap.png
        """
        pass
    def set_properties(
        self, subset: Subset[Hashable] | None = ..., **kwargs: str | int
    ) -> Styler: ...
    def bar(
        self,
        subset: Subset[Hashable] | None = None,
        axis: Axis | None = 0,
        *,
        color: str | list[str] | tuple[str, str] | None = None,
        cmap: str | Colormap | None = None,
        width: float = 100,
        height: float = 100,
        align: (
            Literal["left", "right", "zero", "mid", "mean"]
            | float
            | Callable[[Series | np_ndarray | DataFrame], float]
        ) = "mid",
        vmin: float | None = None,
        vmax: float | None = None,
        props: str = "width: 10em;",
    ) -> Styler: ...
    def highlight_null(
        self,
        color: str | None = "red",
        subset: Subset[Hashable] | None = None,
        props: str | None = None,
    ) -> Styler: ...
    def highlight_max(
        self,
        subset: Subset[Hashable] | None = None,
        color: str = "yellow",
        axis: Axis | None = 0,
        props: str | None = None,
    ) -> Styler: ...
    def highlight_min(
        self,
        subset: Subset[Hashable] | None = None,
        color: str = "yellow",
        axis: Axis | None = 0,
        props: str | None = None,
    ) -> Styler: ...
    def highlight_between(
        self,
        subset: Subset[Hashable] | None = None,
        color: str = "yellow",
        axis: Axis | None = 0,
        left: Scalar | list[Scalar] | None = None,
        right: Scalar | list[Scalar] | None = None,
        inclusive: IntervalClosedType = "both",
        props: str | None = None,
    ) -> Styler: ...
    def highlight_quantile(
        self,
        subset: Subset[Hashable] | None = None,
        color: str = "yellow",
        axis: Axis | None = 0,
        q_left: float = 0,
        q_right: float = 1,
        interpolation: QuantileInterpolation = "linear",
        inclusive: IntervalClosedType = "both",
        props: str | None = None,
    ) -> Styler: ...
    @classmethod
    def from_custom_template(
        cls,
        searchpath: str | list[str],
        html_table: str | None = ...,
        html_style: str | None = ...,
    ) -> type[Styler]: ...
    def pipe(
        self,
        func: (
            Callable[Concatenate[Self, P], T]
            | tuple[Callable[Concatenate[Self, P], T], str]
        ),
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T: ...
    def format_index_names(
        self,
        formatter: ExtFormatter | None = None,
        axis: Axis = 0,
        level: Level | list[Level] | None = None,
        na_rep: str | None = None,
        precision: int | None = None,
        decimal: str = ".",
        thousands: str | None = None,
        escape: str | None = None,
        hyperlinks: str | None = None,
    ) -> StylerRenderer: ...
