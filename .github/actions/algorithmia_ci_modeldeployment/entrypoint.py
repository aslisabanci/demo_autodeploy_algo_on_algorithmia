#!/usr/bin/python3

import os
from datetime import datetime
import json
from pyexpat import model
from src import algorithmia_utils, notebook_utils


# TODO: If model_config.json doesn't exist, create it from scratch
def update_algo_model_config(
    base_path,
    github_repo,
    commit_hash,
    model_filepath,
    config_rel_path="model_config.json",
):
    full_path = "{}/{}".format(base_path, config_rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as config_file:
            config = json.load(config_file)
            print("old hash", config["model_origin_commitHash"])

        config["model_filePath"] = model_filepath
        config["model_origin_commitHash"] = commit_hash
        config["model_origin_repo"] = github_repo
        config["model_uploadedAt_UTC"] = datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        with open(full_path, "w") as new_config_file:
            print("new hash", config["model_origin_commitHash"])
            json.dump(config, new_config_file)


if __name__ == "__main__":
    # repo_name = os.getenv("INPUT_CURRENT_REPO")
    # repo_path = "/github/workspace/{}".format(repo_name)

    current_commit_hash = os.getenv("GITHUB_SHA")
    github_repo = os.getenv("GITHUB_REPOSITORY")
    utc_timestamp = datetime.utcnow()

    workspace = os.getenv("GITHUB_WORKSPACE")

    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    upload_path = os.getenv("INPUT_ALGORITHMIA_UPLOADPATH")
    model_rel_path = os.getenv("INPUT_MODELFILE_RELATIVEPATH")

    algo_name = os.getenv("ALGORITHMIA_ALGONAME")

    if not algorithmia_api_key:
        raise Exception("field 'algorithmia_api_key' not defined in workflow")
    # TODO: continue checks

    if os.path.exists(workspace):
        # workspace_notebook_path = "{}/{}".format(workspace, notebook_path)
        # print("workspace notebook path:", workspace_notebook_path)
        # notebook_utils.run_notebook(
        #     notebook_path=workspace_notebook_path, execution_path=workspace
        # )

        model_full_path = "{}/{}".format(workspace, model_rel_path)
        algorithmia_model_path = algorithmia_utils.upload_model(
            algorithmia_api_key, model_full_path, upload_path, current_commit_hash
        )

        algo_dir = "{}/{}".format(workspace, algo_name)
        update_algo_model_config(
            algo_dir, github_repo, current_commit_hash, algorithmia_model_path
        )
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )