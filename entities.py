from typing import NamedTuple, Any


class Size(NamedTuple):
    """
    Represents a size
    """

    width: int
    height: int


class Color(NamedTuple):
    """
    8-bit components of a color
    """

    r: int
    g: int
    b: int


class Shot(NamedTuple):
    """
    Represents a shot from Landsat. The asset is the output of the listing
    and the image contains details about the actual image.
    """

    asset: Any
    image: Any