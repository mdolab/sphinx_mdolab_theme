# Standard Python modules
from contextlib import contextmanager

# External modules
import numpy as np


@contextmanager
def printoptions(*args, **kwds):
    """
    Context manager for setting numpy print options.
    Set print options for the scope of the `with` block, and restore the old
    options at the end. See `numpy.set_printoptions` for the full description of
    available options. If any invalid options are specified, they will be ignored.
    Parameters
    ----------
    *args : list
        Variable-length argument list.
    **kwds : dict
        Arbitrary keyword arguments.
    Examples
    --------
    >>> with printoptions(precision=2):
    ...     print(np.array([2.0])) / 3
    [0.67]
    The `as`-clause of the `with`-statement gives the current print options:
    >>> with printoptions(precision=2) as opts:
    ...      assert_equal(opts, np.get_printoptions())
    See Also
    --------
    set_printoptions, get_printoptions
    """
    opts = np.get_printoptions()

    # ignore any keyword args that are not valid in this version of numpy
    # e.g. numpy <=1.13 does not have the 'floatmode' option
    kw_opts = dict((key, val) for key, val in kwds.items() if key in opts)

    try:
        np.set_printoptions(*args, **kw_opts)
        yield np.get_printoptions()
    finally:
        np.set_printoptions(**opts)
