.PHONY: test
test:
	python -m unittest test.test_httpsrvpy

run:
	python main.py

docker_build:
	docker build -t httpsrvpy .

docker_run:
	docker run -d -p 8080:80 --name=httpsrvpy httpsrvpy

docker_stop:
	docker stop httpsrvpy && docker rm httpsrvpy
