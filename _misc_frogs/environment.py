
import sys
import pathlib
import inspect


def get_runtime_env():
    if "linux" in sys.platform.lower():
        return "colab"
    else:
        return "local"


def get_data_source_root_folder():
    if get_runtime_env() == "local":
        return FolderGetterLocal.get_data_source_root_folder()
    else:
        return FolderGetterColab.get_data_source_root_folder()


def get_data_dump_root_folder():
    if get_runtime_env() == "local":
        return FolderGetterLocal.get_data_dump_root_folder()
    else:
        return FolderGetterColab.get_data_dump_root_folder()


class FolderGetterLocal:

    @classmethod
    def get_data_source_root_folder(cls):
        data_in_root = cls._get_root_folder("10_data_in")
        return data_in_root

    @classmethod
    def get_data_dump_root_folder(cls):
        data_in_root = cls._get_root_folder("30_data_out")
        return data_in_root

    @staticmethod
    def _get_root_folder(dir_to_search):
        myfile = inspect.getabsfile(lambda: None)
        lastdir = pathlib.Path(myfile).parent
        cdir = lastdir
        while True:
            r_path = cdir.joinpath(dir_to_search)
            if r_path.is_dir():
                break
            r_path = None
            cdir = cdir.parent
            if cdir == lastdir:
                break
            lastdir = cdir
        if r_path is not None:
            return r_path


class FolderGetterColab:

    @classmethod
    def get_data_source_root_folder(cls):
        return "/content/gdrive/My Drive/Colab/DataFrogDataSource"

    @classmethod
    def get_data_dump_root_folder(cls):
        return "/content/gdrive/My Drive/Colab/DataFrogDump"
