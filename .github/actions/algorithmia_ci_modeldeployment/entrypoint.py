#!/usr/bin/python3

import os
from src import algorithmia_utils, notebook_utils


if __name__ == "__main__":
    current_commit_hash = os.getenv("GITHUB_SHA")
    github_repo = os.getenv("GITHUB_REPOSITORY")
    workspace = os.getenv("GITHUB_WORKSPACE")
    github_context = os.getenv("GITHUB_CONTEXT")
    commit_msg = ""
    try:
        commit_msg = github_context["event"]["head_commit"]["message"]
        print(commit_msg)
    except KeyError:
        print(
            f"Cannot get the commit message for the trigger event out of our GITHUB_CONTEXT: {github_context}"
        )

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
            algorithmia_api_key, model_full_path, upload_path, current_commit_hash
        )

        algo_dir = "{}/{}".format(workspace, algo_name)
        algorithmia_utils.update_algo_model_config(
            algo_dir, github_repo, current_commit_hash, algorithmia_model_path
        )
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )