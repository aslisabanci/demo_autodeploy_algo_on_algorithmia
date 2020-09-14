from ubuntu:18.04


RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-setuptools \
    python3-pip


RUN pip3 install algorithmia&& \
    pip3 install algorithmia-api-client&& \
    pip3 install pyyaml&& \
    pip3 install jupyter&& \
    pip3 install nbformat&& \
    pip3 install nbconvert[execute]&& \
    pip3 install requests

COPY entrypoint.py /entrypoint.py
COPY src /src
RUN chmod +x /entrypoint.py
RUN pwd
RUN ls
ENTRYPOINT ["/entrypoint.py"]
