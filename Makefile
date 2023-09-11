install:
	pip install -q -r requirements.txt

build:
	docker build -t llama-api .

run:
	docker run -it --rm -p  5000:5000 llama-api

flask:
	flask run --host=0.0.0.0