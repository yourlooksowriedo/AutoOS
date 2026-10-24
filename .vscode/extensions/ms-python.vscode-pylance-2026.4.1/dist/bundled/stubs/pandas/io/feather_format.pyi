from pandas import DataFrame

from pandas._libs.lib import NoDefault
from pandas._typing import (
    DtypeBackend,
    FilePath,
    HashableT,
    ReadBuffer,
    StorageOptions,
)

def read_feather(
    path: FilePath | ReadBuffer[bytes],
    columns: list[HashableT] | None = None,
    use_threads: bool = True,
    storage_options: StorageOptions = None,
    dtype_backend: DtypeBackend | NoDefault = "numpy_nullable",
) -> DataFrame:
    """
Load a feather-format object from the file path.

Feather is particularly useful for scenarios that require efficient
serialization and deserialization of tabular data. It supports
schema preservation, making it a reliable choice for use cases
such as sharing data between Python and R, or persisting intermediate
results during data processing pipelines. This method provides additional
flexibility with options for selective column reading, thread parallelism,
and choosing the backend for data types.

Parameters
----------
path : str, path object, or file-like object
    String, path object (implementing ``os.PathLike[str]``), or file-like
    object implementing a binary ``read()`` function. The string could be a URL.
    Valid URL schemes include http, ftp, s3, gs and file. For file URLs, a host is
    expected. A local file could be: ``file://localhost/path/to/table.feather``.
columns : sequence, default None
    If not provided, all columns are read.
use_threads : bool, default True
    Whether to parallelize reading using multiple threads.
storage_options : dict, optional
    Extra options that make sense for a particular storage connection, e.g.
    host, port, username, password, etc. For HTTP(S) URLs the key-value pairs
    are forwarded to ``urllib.request.Request`` as header options. For other
    URLs (e.g. starting with "s3://", and "gcs://") the key-value pairs are
    forwarded to ``fsspec.open``. Please see ``fsspec`` and ``urllib`` for more
    details, and for more examples on storage options refer `here
    <https://pandas.pydata.org/docs/user_guide/io.html?
    highlight=storage_options#reading-writing-remote-files>`_.

dtype_backend : {'numpy_nullable', 'pyarrow'}
    Back-end data type applied to the resultant :class:`DataFrame`
    (still experimental). If not specified, the default behavior
    is to not use nullable data types. If specified, the behavior
    is as follows:

    * ``"numpy_nullable"``: returns nullable-dtype-backed :class:`DataFrame`.
    * ``"pyarrow"``: returns pyarrow-backed nullable
      :class:`ArrowDtype` :class:`DataFrame`

    .. versionadded:: 2.0

Returns
-------
type of object stored in file
    DataFrame object stored in the file.

See Also
--------
read_csv : Read a comma-separated values (csv) file into a pandas DataFrame.
read_excel : Read an Excel file into a pandas DataFrame.
read_spss : Read an SPSS file into a pandas DataFrame.
read_orc : Load an ORC object into a pandas DataFrame.
read_sas : Read SAS file into a pandas DataFrame.

Examples
--------
>>> df = pd.read_feather("path/to/file.feather")  # doctest: +SKIP
    """
    pass
