from pathlib import Path


class PathValidator:

    def __init__(self, path: Path, name: str) -> None:
        if isinstance(path, str):
            self.path = Path(path)
        elif isinstance(path, Path):
            self.path = path
        else:
            raise Exception("'{0}' is neither a string or Path!".format(path))

        self.name = name
        self.msg_prefix = "{0} '{1}' ".format(name, path)

    def exists(self):
        if not self.path.exists():
            print(self.__create_errmsg("doesn't exist!"))
            exit(1)
        return self

    def is_file(self):
        if not self.path.is_file():
            print(self.__create_errmsg("is not a regular file!"))
            exit(1)
        return self

    def is_dir(self):
        if not self.path.is_dir():
            print(self.__create_errmsg("is not a directory!"))
            exit(1)
        return self

    def get_path(self):
        return self.path

    def __create_errmsg(self, suffix):
        return self.msg_prefix + suffix
