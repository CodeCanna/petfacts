import os, getpass

class Parser:
    @classmethod
    def get_win_path(self, path: str) -> str:
        return path.replace('<USERNAME>', os.getlogin()).strip()

    @classmethod
    def get_linux_path(self, path: str) -> str:
        #return path.replace('$USER', os.getlogin()).strip()
        return path.replace('$USER', getpass.getuser()).strip()

    @classmethod
    def get_mac_path(self, path: str) -> str:
        return path.replace('$USER', os.getlogin()).strip()

    @classmethod
    def get_extension(self, url: str) -> str:
        (root, extension) = os.path.splitext(url)
        return extension