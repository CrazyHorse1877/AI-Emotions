.PHONY: install setup run train game reset

install:
	pip install -r requirements.txt
	pip install flask matplotlib scikit-learn livereload

setup:
	@mkdir -p models plots
	@echo "📁 Folders ready."

run:
	python live_dashboard.py

train:
	python train_agent.py

game:
	python main.py

reset:
	@rm -rf models/*
	@rm -rf plots/*
	@echo "🧹 All models and plots removed."
