import yaml


class ActionConfigUtils:
    def __init__(self, config_path) -> None:
        self.action_config_path = config_path
        self.config = None
        with open(self.action_config_path, "r") as stream:
            self.config = yaml.safe_load(stream)

    def get_algoname(self, default_name):
        algo_name = default_name
        try:
            algo_name = self.config["jobs"]["algorithmia-ci"]["env"][
                "ALGORITHMIA_ALGONAME"
            ]
        except KeyError as e:
            print(
                f"Required keys for algorithm name do not exist in workflow YAML file: {e}"
            )
        return algo_name

    def get_model_relativepath(self, default_path):
        model_relativepath = default_path
        try:
            ci_steps = self.config["jobs"]["algorithmia-ci"]["steps"]
            for step in ci_steps:
                if step["name"] == "Deploy to Algorithmia":
                    model_relativepath = step["with"]["modelfile_relativepath"]
                    break
        except KeyError as e:
            print(
                f"Required keys for model file relative path do not exist in workflow YAML file: {e}"
            )
        return model_relativepath

    def get_algorithmia_filepaths(self, algo_name, inference_script_name=None):
        if not inference_script_name:
            inference_script_name = algo_name
        algo_script_path = (
            f"/github/workspace/{algo_name}/src/{inference_script_name}.py"
        )
        algo_requirements_path = f"/github/workspace/{algo_name}/requirements.txt"
        return algo_script_path, algo_requirements_path
