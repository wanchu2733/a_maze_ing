class Config:
    def __init__(self) -> None:
        self._width: int = 0
        self._height: int = 0
        self._entry: list[int] = [0, 0]
        self._exit: list[int] = [0, 0]
        self._output_file: str = ""
        self._perfect: bool = False
        self._seed: int = 0
        self._algorithm: str = "dfs"

    @staticmethod
    def load_config_1(ln: str, config: "Config") -> None:
        """Load config helper

        Args:
            ln: config line, must be valid
            config: the config content to write to

        Returns:
            None
        """
        k, v = ln.split("=")
        an = f"_{k.strip().lower()}"
        rv = v.strip()
        if hasattr(config, an):
            cv = getattr(config, an)
            setattr(
                config,
                an,
                [int(n) for n in rv.split(",")]
                if isinstance(cv, list) else type(cv)(rv)
            )

    @staticmethod
    def load_config(path: str) -> "Config":
        """Load config from path

        Args:
            path: the path to config file, default config.txt

        Returns:
            Config
        """
        config = Config()
        try:
            with open(path) as file:
                data = file.readlines()
                for ln in data:
                    if not ln or ln.startswith("#"):
                        continue
                    Config.load_config_1(ln, config)
        except FileNotFoundError as e:
            print(e)
        return config
