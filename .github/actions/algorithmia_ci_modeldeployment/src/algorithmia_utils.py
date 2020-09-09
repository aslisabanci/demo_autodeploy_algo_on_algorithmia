import Algorithmia
import os


def upload_model(api_key, local_path, remote_path):
    _, model_name = os.path.split(local_path)
    print("will upload {} from {} to {}".format(model_name, local_path, remote_path))
    algo_client = Algorithmia.client(api_key)
    if not algo_client.dir(remote_path).exists():
        algo_client.dir(remote_path).create()
    full_path = "{}/{}".format(remote_path, model_name)
    result = algo_client.file(full_path).putFile(local_path)
    # TODO: Act on the result object, have a return value
    print(result)

