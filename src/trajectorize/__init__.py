from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("trajectorize")
except PackageNotFoundError:
    __version__ = "unknown version"
