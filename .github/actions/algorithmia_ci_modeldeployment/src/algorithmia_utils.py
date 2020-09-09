import Algorithmia
import os


def upload_model(api_key, local_path, remote_path, commit_hash):
    _, model_name = os.path.split(local_path)
    name_before_ext, ext = tuple(os.path.splitext(model_name))
    unique_model_name = "{}_{}.{}".format(name_before_ext, commit_hash, ext)
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
