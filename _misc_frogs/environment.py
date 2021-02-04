
import pathlib
import inspect
import platform


def get_runtime_env():
    if "amzn2" in platform.platform().lower():
        return "aws1"
    elif "bionic" in platform.platform().lower():
        # Linux-4.19.112+-x86_64-with-Ubuntu-18.04-bionic
        return "colab"
    else:
        return "local"


def runs_remote():
    return get_runtime_env() != "local"


def get_data_source_root_folder():
    if get_runtime_env() == "local":
        return FolderGetterLocal.get_data_source_root_folder()
    elif get_runtime_env() == "aws1":
        return FolderGetterAws1.get_data_source_root_folder()
    elif get_runtime_env() == "colab":
        return FolderGetterColab.get_data_source_root_folder()
    else:
        raise ValueError("not supported")


def get_data_dump_root_folder(environment=None):
    if environment is None:
        environment = get_runtime_env()
    if environment == 'local':
        return FolderGetterLocal.get_data_dump_root_folder()
    elif environment == 'localcolab':
        return FolderGetterLocalColab.get_data_dump_root_folder()
    elif environment == 'aws1':
        return FolderGetterAws1.get_data_dump_root_folder()
    elif environment == 'localaws1':
        return FolderGetterLocalAws1.get_data_dump_root_folder()
    elif environment == 'colab':
        return FolderGetterColab.get_data_dump_root_folder()
    else:
        raise ValueError("not supported")


class FolderGetterLocal:

    @classmethod
    def get_data_source_root_folder(cls):
        data_in_root = cls._get_root_folder("10_data_in")
        return data_in_root

    @classmethod
    def get_data_dump_root_folder(cls):
        data_in_root = cls._get_root_folder("30_data_out")
        return data_in_root.joinpath("local")

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


class FolderGetterLocalColab(FolderGetterLocal):

    @classmethod
    def get_data_dump_root_folder(cls):
        data_in_root = cls._get_root_folder("30_data_out")
        return data_in_root.joinpath("colab")


class FolderGetterColab:

    @classmethod
    def get_data_source_root_folder(cls):
        return pathlib.Path("/content/gdrive/My Drive/Colab/DataFrogDataSource")

    @classmethod
    def get_data_dump_root_folder(cls):
        return pathlib.Path("/content/gdrive/My Drive/Colab/DataFrogDump")


class FolderGetterLocalAws1(FolderGetterLocal):

    @classmethod
    def get_data_dump_root_folder(cls):
        data_in_root = cls._get_root_folder("30_data_out")
        return data_in_root.joinpath("aws1")


class FolderGetterAws1:

    @classmethod
    def get_data_source_root_folder(cls):
        return pathlib.Path("/home/ec2-user/workspace/data_in")

    @classmethod
    def get_data_dump_root_folder(cls):
        return pathlib.Path("/home/ec2-user/workspace/data_out")
