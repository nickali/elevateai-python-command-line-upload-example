import sys
import os
import json
import time
import argparse
from ElevateAIPythonSDK import ElevateAI
from rich.live import Live
from rich.table import Table


def update_results(upload_results, config):
    updated_results = []
    for row in upload_results:
        response = ElevateAI.GetInteractionStatus(row[1], config["api_token"])
        response_json = response.json()
        new_row = (row[0], row[1], response_json["status"])
        updated_results.append(new_row)
    return updated_results


def generate_table(results) -> Table:
    table = Table()
    table.add_column("Filename")
    table.add_column("Identifier")
    table.add_column("Status")

    for row in results:
        table.add_row(row[0], row[1], row[2])

    return table


def process_args(args):
    parser = argparse.ArgumentParser(description='Upload audio files to ElevateAI.')
    parser.add_argument('-f', '--files', nargs='+', help='Audio files to upload')
    parser.add_argument('-c', '--config', default='config.json', help='Path to config.json file')
    arguments = parser.parse_args(args)

    if arguments.files is None:
        parser.print_help()
        sys.exit(0)

    return arguments.files, arguments.config


def check_files(config_file, audio_files):
    if not os.path.isfile(config_file):
        print(f"Config file '{config_file}' not found. A config.json file is required.")
        sys.exit(1)

    if not all(os.path.isfile(file) for file in audio_files):
        print("One or more audio files do not exist. Please check the file paths and try again.")
        sys.exit(1)

    with open(config_file) as f:
        config = json.load(f)

    return config


def upload_files(audio_files, config):
    upload_results = []
    for file in audio_files:
        response = upload_file(file, config)

        if response.status_code == 201:
            upload_results.append((file, response.json()["interactionIdentifier"], "Uploaded Successfully"))
        else:
            upload_results.append((file, response.json()["interactionIdentifier"], "Upload error"))

    return upload_results


def main(args):
    try:
        audio_files, config_file = process_args(args)
        config = check_files(config_file, audio_files)
        upload_results = upload_files(audio_files, config)

        with Live(generate_table(upload_results), refresh_per_second=4) as live:
            while True:
                time.sleep(15)
                upload_results = update_results(upload_results, config)
                live.update(generate_table(upload_results))
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


def upload_file(file_path, config):
    token = config['api_token']
    language_tag = "en-us"
    version = "default"
    transcription_mode = "highAccuracy"

    file_name = os.path.basename(file_path)

    declare_response = ElevateAI.DeclareAudioInteraction(language_tag, version, None, token, transcription_mode, False)
    declare_json = declare_response.json()
    interaction_id = declare_json["interactionIdentifier"]

    ElevateAI.UploadInteraction(interaction_id, token, file_path, file_name)
    return declare_response


if __name__ == "__main__":
    main(sys.argv[1:])


