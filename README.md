# ElevateAI Python File Uploading

This is an example where multiple files can be uploaded through the command line. A table is displayed with the current state of the files (processing, processed). Ctrl-C will exit but if the files have been uploaded, they will still be processed by the ElevateAI platform.

## Setup

A config.json is needed to define two parameters: api_token and api_url. The api_url in config.json.sample does not need to be changed currently.

## Usage

This app was made using the sample.wav and sample2.wav as the test audio files.

Here are the steps to run the example.

### Clone this repository and submodule

```sh
git clone --recursive https://github.com/nickali/elevateai-python-command-line-upload-example.git
cd elevate-python-command-line-upload-example
```

### Create config.json

Copy config.json.sample to config.json and replace the api_key. If you don't have an API key, visit the [ElevateAI website](https://www.elevateai.com).

### Run the command

To upload individual files:

```sh
python app.py -f sample.wav sample2.wav
```

To upload all files in a directory

```sh
python app.py -d input_dir
```

### Verify status

Visit the [dashboard](https://app.elevateai.com/Interactions) to check if the files have been uploaded and their current state.

### Docker

Build the image

```sh
docker build -t elevateai:latest .
```

Place the audio files in a directory. Pass in the audio files directory and config.json.

```sh
docker run --tty --rm --name elevateai \
  --volume $PWD/config.json:/usr/elevateai/config.json \
  --volume $PWD/input:/usr/elevateai/input elevateai:latest
```

