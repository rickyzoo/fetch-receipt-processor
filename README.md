# Receipt Processor

Welcome to **Receipt Processor**! This local Dockerized application written in Python uses the FastAPI framework to process Receipt information represented in JSON and returns the number of points earned according to a set of rules applied to the purchase details. This project completes the Take-home portion of the Backend Engineer role at **Fetch Rewards**, _America's Rewards App_.

## Setup

### Initial setup

This app runs on Python version 3.9.13. Please visit [this link](https://www.python.org/downloads/release/python-3913/) to install it on your machine if you don't have it already.

Clone this repository onto your machine and `cd` into the `fetch-receipt-processor` Project root directory.

- [Click here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for more information on how to Clone a Git repository.

Once Python v3.9.13 is successfully installed on your machine and you're in the Project's root directory, create a Python virtual environment by running `python3 -m venv .venv`

- To verify you have the correct Python version installed, run `which python` in your terminal.

Run `source .venv/bin/activate` to activate the virtual environment in the Project's root directory

Assuming you have Docker installed, please start your Docker engine.
Run `docker-compose up --build` in the Project root directory in a new terminal window.

Once the Docker container finishes building and composing, scan the logs and visit the link associated with the `Documentation` tag to iteract with the API endpoints! The link should be http://0.0.0.0:8000/docs

### Testing

You can test this web service using the Documentation link as mentioned earlier. Expand the `POST` and `GET` API endpoint cards and click the `Try it out` button located in the top-right corner.

There also exists a `test_api.py` file in `fetch-receipt-processor/app/tests`.
In a new terminal window `cd` into the `tests` subdirectory and run `pytest -s` to run the test suite. Feel free to utilize this file to add other necessary tests.

### Other

`Ctrl + C` and then run `docker-compose down` to kill the Docker containers.

Simply run `docker-compose up` to reboot this app if you've already successfully ran `docker-compose up --build`.

**ALWAYS REMEMBER** to activate your virtual environment before editing or running code.

Run `deactivate` to deactivate the Python virtual environment when you're done.

Hope you earned more points than you expected!

## Python-to-Golang

While Go is the explicitly stated backend language of choice at Fetch Rewards, I come with limited Go experience (I'm familiar with some concepts). Python has been my main programming language since I started coding 3 years ago and was the backend language of choice for the app I worked on while working as a Full-stack engineer at my previous role. In order to properly capture my engineering and programming knowledge I chose to complete this project using Python and the FastAPI Framework. However, detailed below are a few notable things I would do if I were to refactor my solution from Python to Go.

### Data schemas with field validation

To process JSON data in Go I would define structs with JSON tags to map the JSON fields to Go struct fields. I would implement nested structs to handle the Item-to-Receipt object relationship specified in the API Spec.

A function would be defined to process and transform the relevant string numerical fields into float or integer data types for further calculation such as the string "price" and "total" fields coming in from the JSON input. This function would use `strconv.ParseFloat()`. Separate structs defining the key-value pairs with the desired data types would be created and used as the Return value of said function. This function will also explicitly return an error when necessary.

To add Regex pattern validation to the relevant fields I would import a package such as `regexp`, create a const that maps each field to its associated Regex pattern, instantiate structs for each validation rule along with a Validator struct that holds all validation rules using a **map**, and define a Validator function that uses the elements previously defined. A function that is used to process the actual incoming JSON would call the Validator function.

The basic data schema structs would live in a separate `models` subdirectory while the field validation code would live in a separate subdirectory called `services` or some equivalent.

### Points calculation

The points calculation file would live in the same `services` subdirectory as the data processing file. The points calculation file will be called after the data processing file is called. More on this later. For simplicity within the scope of this project, I would create one singular `CalculatePoints` function where the input is the post-processed Receipt struct where each field is set to the appropriate data type for the necessary calculation. This file would import relevant packages such as `math`, `strings` and `time`.

### In-memory storage

A `memory_store` file would live in a `storage` subdirectory. This file would define a `MemoryStore` struct with key-value pairs. One pair would map the uniqueID string value to the Receipt data model and the other pair would map the uniqueID string value to the points earned (as an integer) for a given Receipt. Functions would also be defined to Store and Retrieve data from the cache. More specifically, a `StoreReceipt`, a `StorePoints` and a `GetPoints` function would be defined, each using `mutex.Lock()` and `defer mutex.Unlock()` to make sure only one Goroutine can access a given variable at a time. A function that returns the address of the `MemoryStore` would also be defined in this file to be used in the main.go file.

### API Handlers
