# id-cards-pad-challenge-api
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
This repo only provide a dummy implementation that returns a random score. To implement the API with your trained model, you should take a look at the file 'utils/processor.py'. In there, you'll find an interface IEvaluator with an abstract method 'run'. You should implement this interface to call your model predict method with the input image and return a dictionary with the challenge's required metadata.

NOTE: keep in mind that the API will run in an environment without internet access. Therefore, your model should be able to run without any external API. Make sure that all required dependencies are included in the requirements.txt file and your model's weights are inside the api folder.

## Build image for submission
Once you have implemented the IEvaluator interface to use your trained model, you need to build a docker image. There is a dockerfile that contains the instructions to build it. To do so, run the command:
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

## Test your image before submission
To run tests on your image, you can use the provided docker-compose.yml file that will build your api image and run a container with it along with a mock up of the evaluation worker:
```shell
docker compose up --build --abort-on-container-exit --exit-code-from worker
```
If everything is correct you should see an output similar to:
```
worker-1  | Sending request for file: dataset/logo.jpg
worker-1  | Response status code: 200
worker-1  | {'score': 0.57, 'width': 583, 'height': 825, 'filename': 'logo.jpg'}
worker-1 exited with code 0
```