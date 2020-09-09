#!/usr/bin/python3

import os
from datetime import datetime
import json
from os import PathLike
from typing import AnyStr
from src import algorithmia_utils, notebook_utils


def load_algo_model_config(base_path, config_rel_path="model_config.json"):
    full_path = "{}/{}".format(base_path, config_rel_path)
    with open(full_path) as json_file:
        config = json.load(json_file)
        print(config.keys(), config.values())
        return config


if __name__ == "__main__":
    # repo_name = os.getenv("INPUT_CURRENT_REPO")
    # repo_path = "/github/workspace/{}".format(repo_name)

    current_commit_hash = os.getenv("GITHUB_SHA")
    github_repo = os.getenv("GITHUB_REPOSITORY")
    utc_timestamp = datetime.utcnow()

    workspace: AnyStr[PathLike] = os.getenv("GITHUB_WORKSPACE")

    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    upload_path = os.getenv("INPUT_ALGORITHMIA_UPLOADPATH")
    model_rel_path = os.getenv("INPUT_MODELFILE_RELATIVEPATH")

    algo_name = os.getenv("ALGORITHMIA_ALGONAME")

    if not algorithmia_api_key:
        raise Exception("field 'algorithmia_api_key' not defined in workflow")
    # TODO: continue checks

    if os.path.exists(workspace):
        algo_dir = "{}/{}".format(workspace, algo_name)
        config = load_algo_model_config(algo_dir)
        print(config)

        workspace_notebook_path = "{}/{}".format(workspace, notebook_path)
        print("workspace notebook path:", workspace_notebook_path)
        notebook_utils.run_notebook(
            notebook_path=workspace_notebook_path, execution_path=workspace
        )

        model_full_path = "{}/{}".format(workspace, model_rel_path)
        algorithmia_utils.upload_model(
            algorithmia_api_key, model_full_path, upload_path
        )
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )