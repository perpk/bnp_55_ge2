run: venv/bin/activate
	docker-compose up -d
	./venv/bin/python3 sample/__main__.py

setup: requirements.txt
	pip install -r requirements.txt

clean:
	docker-compose down
	rm -rf __pycache__
	rm -rf venv

venv/bin/activate: requirements.txt
	python -m venv venv
	./venv/bin/pip install -r requirements.txt
