#!/usr/bin/python3

import os
from src import algorithmia_utils, notebook_utils


if __name__ == "__main__":
    github_repo = os.getenv("GITHUB_REPOSITORY")
    workspace = os.getenv("GITHUB_WORKSPACE")
    commit_msg = os.getenv("HEAD_COMMIT_MSG")
    commit_hash = os.getenv("GITHUB_SHA")

    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    upload_path = os.getenv("INPUT_ALGORITHMIA_UPLOADPATH")
    model_rel_path = os.getenv("INPUT_MODELFILE_RELATIVEPATH")

    algo_name = os.getenv("ALGORITHMIA_ALGONAME")

    if not algorithmia_api_key:
        raise Exception("field 'algorithmia_api_key' not defined in workflow")
    # TODO: Implement missing key checks

    if os.path.exists(workspace):

        # TODO: Implement this as an optional step
        workspace_notebook_path = "{}/{}".format(workspace, notebook_path)
        print("workspace notebook path:", workspace_notebook_path)
        notebook_utils.run_notebook(
            notebook_path=workspace_notebook_path, execution_path=workspace
        )

        # TODO: Return an error if the model file doesn't exist
        model_full_path = "{}/{}".format(workspace, model_rel_path)
        algorithmia_model_path = algorithmia_utils.upload_model(
            algorithmia_api_key, model_full_path, upload_path, commit_hash
        )

        algo_dir = "{}/{}".format(workspace, algo_name)
        algorithmia_utils.update_algo_model_config(
            algo_dir, github_repo, commit_hash, commit_msg, algorithmia_model_path
        )
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )