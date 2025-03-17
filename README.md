# IJCB PAD ID-Card Challenge
This repo contains the base code needed to prepare your submission for the challenge. In folder '/api' you will find the python base script that will run an uvicorn server with the API. To run it manually you should first create a virtual environment and install dependencies:
```shell
python -m venv /my_env
source my_env/bin/activate
pip install --upgrade pip setuptools
pip install -r api/requirements.txt
```
After installing dependencies you can use the command:
```shell
fastapi run api/main.py --host 127.0.0.1 --port 8001
```
And it will run the server on port 8001, then you can open your browser and access the url http://localhost:8001/docs to view the swagger UI and test the API.

## Adding your trained model
This repo only provides a dummy implementation that returns a random score. To implement the API with your trained model, you should take a look at the file 'utils/processor.py'. In there, you'll find an interface IEvaluator with an abstract method 'run'. You should implement this interface to call your model predict method with the input image and return a dictionary with the challenge's required metadata:
- score: a single continuous floating point score output in the range [0.0, 1.0] where 0.0 means the model identifies the sample as an Attack and 1.0 as a Bonafide.

If you need some python packages, you should add them to the api/requirements.txt file.

> [!IMPORTANT]
> Keep in mind that the API will run in an environment without internet access. Therefore, your model should be able to run without any external API. Make sure that all required dependencies are included in the requirements.txt file and your model's weights are inside the api folder. Only the contents of the api folder will be accessible inside the docker image.

## Test your image before submission
To run tests on your image, you can use the provided docker-compose.yml file that will build your api image and run a container with it along with a mock up of the evaluation worker:
```shell
docker compose up --build --abort-on-container-exit --exit-code-from worker
```
or use the provided shell script 'test_docker_image.sh' that executes the previous command:
```shell
./test_docker_image.sh
```
If everything is correct you should see an output similar to:
```
worker-1  | Checking API availability...
worker-1  | API is now available.
worker-1  | Sending request for file: dataset/test.JPEG
worker-1  | Response status code: 200
worker-1  | {'score': 0.037924911826848984, 'width': 334, 'height': 183, 'filename': 'test.JPEG'}
worker-1  | Sending request for file: dataset/test.png
worker-1  | Response status code: 200
worker-1  | {'score': 0.13558907806873322, 'width': 334, 'height': 183, 'filename': 'test.png'}
worker-1 exited with code 0
```
If not, check whether all required python packages along with the proper version are indicated in the requirements.txt. If needed, you can install ubuntu packages in the image modifying the dockerfile. To do so, open the dockerfile and add installation commands like apt update and apt install in the following section:
```
# Install the application dependencies
# If you need to install ubuntu packages, add the commands here
COPY api ./api
RUN python -m ensurepip --upgrade
RUN pip install --upgrade pip setuptools --no-cache-dir
RUN pip install --no-cache-dir -r ./api/requirements.txt
RUN rm -rf /root/.cache/pip
```

## Build image for submission
Once you have implemented the IEvaluator interface to use your trained model and tested the docker image, you need to build the docker image and prepare it for submission. To do so, run the command:
```shell
docker build -t <team_name>/<algorithm_name>:<version> --network=host .
```
For example:
```shell
docker build -t my_team/my_algorithm:v1 --network=host .
```
This command will build the docker image and will tag it with the specified name. Now you'll need to create a tgz file to be able to upload it to the challenge:
```shell
docker save <team_name>/<algorithm_name>:<version> | gzip > <team_name>_<algorithm_name>_<version>.tgz
```
This is the file you should upload to the challenge.

You can also use the shell script 'prepare_submission.sh' to perform all the steps for you, simply run it as:
```shell
./prepare_submission.sh <team_name> <algorithm_name> <version>
```

## Contact
If you have any questions regarding the implementation of the docker image, you can create an issue in this repo or contact marionieto@facephi.com
