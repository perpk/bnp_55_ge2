infra:
	docker-compose up -d

run: venv/bin/activate
	./venv/bin/python3 sample/main-script.py

setup: requirements.txt
	pip install -r requirements.txt

clean:
	docker-compose down
	rm -rf __pycache__
	rm -rf venv

venv/bin/activate: requirements.txt
	python -m venv venv
	./venv/bin/pip install -r requirements.txt
