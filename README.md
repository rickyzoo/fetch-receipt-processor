# Receipt Processor

Welcome to **Receipt Processor**! This local Dockerized application written in Python follows the FastAPI framework to process Receipt information represented in JSON and returns the number of points earned according to a set of rules applied to the purchase details. This project completes the Take-home portion of the Backend Engineer role at **Fetch Rewards**, _America's Rewards App_.

## Setup

### Initial setup

This app runs on Python version 3.9.13. Please visit [this link](https://www.python.org/downloads/release/python-3913/) to install it on your machine if you don't have it already.

Clone this repository onto your machine and `cd` into the `fetch-receipt-processor` Project root directory.

Once Python v3.9.13 is successfully installed on your machine and you're in the Project's root directory, create a Python virtual environment by running `python3 -m venv .venv`

- To verify you have the correct Python version installed, run `which python` in your terminal.

Run `source .venv/bin/activate` to activate the virtual environment in the Project's root directory

Assuming you have Docker installed, please start your Docker engine.
Run `docker-compose up --build` in the Project root directory in a new terminal window.

Once the Docker container finishes building and composing, scan the logs and visit the link associated with the `Documentation` tag to iteract with the API endpoints! It should be http://0.0.0.0:8000/docs

### Testing

You can test this web service using the Documentation link as mentioned earlier. Expand the `POST` and `GET` API endpoint cards and click the `Try it out` button located in the top-right corner.

There also exists a `test_api.py` file in `fetch-receipt-processor/app/tests`.
In a new terminal window `cd` into the `tests` subdirectory and run `pytest -s` to run the test suite. Feel free to utilize this file to add other necessary tests.

### Other

`Ctrl + C` and then run `docker-compose down` to kill the Docker containers.

Simply run `docker-compose up` to reboot this app if you've already successfully ran `docker-compose up --build`.

ALWAYS REMEMBER to activate your virtual environment before editing or running code.

Run `deactivate` to deactivate the Python virtual environment when you're done.

Hope you earned more points than you expected!

## Python-to-Golang

While Go is the explicitly stated backend language of choice at Fetch Rewards, I come with limited Go experience (I'm familiar with some concepts). Python has been my main programming language since I started coding 3 years ago and was the backend language of choice for the app I worked on while working as a Full-stack engineer at my previous role. In order to properly capture my engineering and programming knowledge I chose to complete this project using Python and the FastAPI Framework. However, detailed below are a few notable things I would do if I were to refactor my solution from Python to Go.


