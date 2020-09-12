import yaml


class ActionConfigUtils:
    def __init__(
        self, config_path="/github/workspace/.github/workflows/main.yml"
    ) -> None:
        self.action_config_path = config_path
        self.config = None
        with open(self.action_config_path, "r") as stream:
            self.config = yaml.safe_load(stream)

    def get_algoname(self):
        algo_name = self.config["jobs"]["algorithmia-ci"]["env"]["ALGORITHMIA_ALGONAME"]
        return algo_name

    def get_model_relativepath(self):
        model_relativepath = self.config["jobs"]["algorithmia-ci"]["steps"][2]["with"][
            "modelfile_relativepath"
        ]
        return model_relativepath
