from collections.abc import Callable

from pandas._typing import TypeT

class PandasDelegate: ...

def register_dataframe_accessor(name: str) -> Callable[[TypeT], TypeT]:
    """
Register a custom accessor on DataFrame objects.

Parameters
----------
name : str
    Name under which the accessor should be registered. A warning is issued
    if this name conflicts with a preexisting attribute.

Returns
-------
callable
    A class decorator.

See Also
--------
register_dataframe_accessor : Register a custom accessor on DataFrame objects.
register_series_accessor : Register a custom accessor on Series objects.
register_index_accessor : Register a custom accessor on Index objects.

Notes
-----
This function allows you to register a custom-defined accessor class for DataFrame.
The requirements for the accessor class are as follows:

* Must contain an init method that:

  * accepts a single DataFrame object

  * raises an AttributeError if the DataFrame object does not have correctly
    matching inputs for the accessor

* Must contain a method for each access pattern.

  * The methods should be able to take any argument signature.

  * Accessible using the @property decorator if no additional arguments are
    needed.

Examples
--------
An accessor that only accepts integers could
have a class defined like this:

>>> @pd.api.extensions.register_dataframe_accessor("int_accessor")
... class IntAccessor:
...     def __init__(self, pandas_obj):
...         if not all(
...             pandas_obj[col].dtype == "int64" for col in pandas_obj.columns
...         ):
...             raise AttributeError("All columns must contain integer values only")
...         self._obj = pandas_obj
...
...     def sum(self):
...         return self._obj.sum()
>>> df = pd.DataFrame([[1, 2], ["x", "y"]])
>>> df.int_accessor
Traceback (most recent call last):
...
AttributeError: All columns must contain integer values only.
>>> df = pd.DataFrame([[1, 2], [3, 4]])
>>> df.int_accessor.sum()
0    4
1    6
dtype: int64
    """
    pass
def register_series_accessor(name: str) -> Callable[[TypeT], TypeT]:
    """
Register a custom accessor on Series objects.

Parameters
----------
name : str
    Name under which the accessor should be registered. A warning is issued
    if this name conflicts with a preexisting attribute.

Returns
-------
callable
    A class decorator.

See Also
--------
register_dataframe_accessor : Register a custom accessor on DataFrame objects.
register_series_accessor : Register a custom accessor on Series objects.
register_index_accessor : Register a custom accessor on Index objects.

Notes
-----
This function allows you to register a custom-defined accessor class for Series.
The requirements for the accessor class are as follows:

* Must contain an init method that:

  * accepts a single Series object

  * raises an AttributeError if the Series object does not have correctly
    matching inputs for the accessor

* Must contain a method for each access pattern.

  * The methods should be able to take any argument signature.

  * Accessible using the @property decorator if no additional arguments are
    needed.

Examples
--------
An accessor that only accepts integers could
have a class defined like this:

>>> @pd.api.extensions.register_series_accessor("int_accessor")
... class IntAccessor:
...     def __init__(self, pandas_obj):
...         if not pandas_obj.dtype == "int64":
...             raise AttributeError("The series must contain integer data only")
...         self._obj = pandas_obj
...
...     def sum(self):
...         return self._obj.sum()
>>> df = pd.Series([1, 2, "x"])
>>> df.int_accessor
Traceback (most recent call last):
...
AttributeError: The series must contain integer data only.
>>> df = pd.Series([1, 2, 3])
>>> df.int_accessor.sum()
6
    """
    pass
def register_index_accessor(name: str) -> Callable[[TypeT], TypeT]:
    """
Register a custom accessor on Index objects.

Parameters
----------
name : str
    Name under which the accessor should be registered. A warning is issued
    if this name conflicts with a preexisting attribute.

Returns
-------
callable
    A class decorator.

See Also
--------
register_dataframe_accessor : Register a custom accessor on DataFrame objects.
register_series_accessor : Register a custom accessor on Series objects.
register_index_accessor : Register a custom accessor on Index objects.

Notes
-----
This function allows you to register a custom-defined accessor class for Index.
The requirements for the accessor class are as follows:

* Must contain an init method that:

  * accepts a single Index object

  * raises an AttributeError if the Index object does not have correctly
    matching inputs for the accessor

* Must contain a method for each access pattern.

  * The methods should be able to take any argument signature.

  * Accessible using the @property decorator if no additional arguments are
    needed.

Examples
--------
An accessor that only accepts integers could
have a class defined like this:

>>> @pd.api.extensions.register_index_accessor("int_accessor")
... class IntAccessor:
...     def __init__(self, pandas_obj):
...         if not all(isinstance(x, int) for x in pandas_obj):
...             raise AttributeError("The index must only be an integer value")
...         self._obj = pandas_obj
...
...     def even(self):
...         return [x for x in self._obj if x % 2 == 0]
>>> df = pd.DataFrame.from_dict(
...     {"row1": {"1": 1, "2": "a"}, "row2": {"1": 2, "2": "b"}}, orient="index"
... )
>>> df.index.int_accessor
Traceback (most recent call last):
...
AttributeError: The index must only be an integer value.
>>> df = pd.DataFrame(
...     {"col1": [1, 2, 3, 4], "col2": ["a", "b", "c", "d"]}, index=[1, 2, 5, 8]
... )
>>> df.index.int_accessor.even()
[2, 8]
    """
    pass

class DirNamesMixin: ...
