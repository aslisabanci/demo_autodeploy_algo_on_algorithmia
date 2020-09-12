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
    upload_path = None
    try:
        if not algo_client.dir(remote_path).exists():
            algo_client.dir(remote_path).create()
        full_remote_path = "{}/{}".format(remote_path, unique_model_name)
        if algo_client.file(full_remote_path).exists():
            print(f"File with the same name exists, overriding: {full_remote_path}")
        result = algo_client.file(full_remote_path).putFile(local_path)
        if result.path:
            print(f"File successfully uploaded at: {full_remote_path}")
            upload_path = result.path
    except Exception as e:
        print(f"An exception occurred while uploading model file to Algorithmia: {e}")
    return upload_path


def update_algo_model_config(
    base_path,
    github_repo,
    commit_hash,
    commit_msg,
    model_filepath,
    config_rel_path="model_config.json",
):
    full_path = "{}/{}".format(base_path, config_rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as config_file:
            config = json.load(config_file)
            print("old hash", config["model_origin_commit_hash"])

        config["model_filepath"] = model_filepath
        config["model_origin_commit_hash"] = commit_hash
        config["model_origin_commit_msg"] = commit_msg
        config["model_origin_repo"] = github_repo
        config["model_uploaded_utc"] = datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        with open(full_path, "w") as new_config_file:
            print("new hash", config["model_origin_commit_hash"])
            json.dump(config, new_config_file)
    else:
        # TODO: If model_config.json doesn't exist, create it from scratch
        pass


# TODO: Update the notebook with new walk through text.
# TODO: Add another example with an algorithm hosted on Github, instead of Algorithmia.
# TODO: Rename action steps
