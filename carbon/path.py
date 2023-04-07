import json as _json
import os as _os
import typing as _typing

from carbon.utils import (
    printer as _printer
)


class Json:

    @staticmethod
    def guarantee(__pth: str, /) -> None:
        """the file `__pth` must be a json-type and exist."""

        pth = _os.path.normpath(__pth)

        if not _os.path.isfile(pth):
            raise FileNotFoundError(f'Not a file: {repr(__pth)}.')

        if not pth.lower().endswith('.json'):
            raise AssertionError(f'Not a json file: {repr(__pth)}.')

        return pth

    @staticmethod
    def read(__pth: str, /) -> _typing.Any:

        pth = Json.guarantee(__pth)

        with open(pth, 'r') as fp:
            out = _json.load(fp)

        return out

    @staticmethod
    def write(__pth: str, __obj: _typing.Any, /, do_log: bool = True) -> None:

        pth = _os.path.normpath(__pth)

        if not pth.lower().endswith('.json'):
            raise AssertionError(f'Not a json file: {repr(__pth)}.')

        if not _os.path.isdir(_os.path.dirname(pth)):
            raise NotADirectoryError(f'The directory does not exist: {repr(__pth)}.')

        if _os.path.exists(pth):
            raise FileExistsError(f'File already exists: {repr(__pth)}.')

        with open(pth, 'w') as fp:
            _json.dump(__obj, fp)
        
        if do_log:
            _printer(f'json written: {repr(__pth)}.')

    @staticmethod
    def rewrite(__pth: str, __obj: _typing.Any, /, do_log: bool = True) -> None:

        pth = Json.guarantee(__pth)

        tmp = f'{pth}.tmp'
        if _os.path.exists(tmp):
            raise FileExistsError(f'Temporary file exists: {repr(tmp)}.')

        bak = f'{pth}.bak'
        if _os.path.exists(bak):
            raise FileExistsError(f'Backup file exists: {repr(bak)}.')

        ## writing the new as temp
        with open(tmp, 'w') as fp:
            _json.dump(__obj, fp)

        _os.rename(pth, bak)  # backup the previous
        _os.rename(tmp, pth)  # rename temp to new
        _os.remove(bak)  # delete the previous

        if do_log:
            _printer(f'json rewritten: {repr(__pth)}.')