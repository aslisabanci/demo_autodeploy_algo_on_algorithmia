import Algorithmia
import os
import json
from datetime import datetime


def upload_model(api_key, local_path, remote_path, commit_hash):
    _, model_name = os.path.split(local_path)
    name_before_ext, ext = tuple(os.path.splitext(model_name))
    unique_model_name = "{}_{}{}".format(name_before_ext, commit_hash, ext)
    print(
        "will upload {} from {} to {}".format(
            unique_model_name, local_path, remote_path
        )
    )
    algo_client = Algorithmia.client(api_key)
    if not algo_client.dir(remote_path).exists():
        algo_client.dir(remote_path).create()
    full_remote_path = "{}/{}".format(remote_path, unique_model_name)
    result = algo_client.file(full_remote_path).putFile(local_path)
    # TODO: Act on the result object, have a return value
    print(result)
    return full_remote_path


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
    else:
        # TODO: If model_config.json doesn't exist, create it from scratch
        pass
