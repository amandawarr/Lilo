import argparse
import shutil
from snakemake import snakemake
import os
import logging
from typing import Any
from importlib.resources import path
from ruamel.yaml import YAML

# Update nested keys in a dictionary
def update_nested_dict(d, keys, value):
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value

def update_config_file_with_comments(project_path: str, config_file_name: str, variable: str, new_value: Any) -> bool:
    """
    Update a specific variable in the config file.

    Parameters:
        project_path (str): The path to the project directory.
        config_file_name (str): The name of the config file to update.
        variable (str): The variable to update in the config file.
        new_value (Any): The new value to set for the variable.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    config_file_path = os.path.join(project_path, config_file_name)
    try:
        yaml = YAML()
        yaml.preserve_quotes = True
        with open(config_file_path, 'r') as f:
            config_data = yaml.load(f)

        update_nested_dict(config_data, variable.split('.'), new_value)

        with open(config_file_path, 'w') as f:
            yaml.dump(config_data, f)

        logging.info(f"Updated {variable} in config file to {new_value}.")
        return True
    except Exception as e:
        logging.error(f"Failed to update config file: {e}")
        return False

def init_config(args: Any) -> None:
    """
    Initialize the configuration and scheme files for the project.
    Also updates the copied config file with the new paths for scheme, reference, and primers.

    This function creates the project and scheme folders if they don't exist.
    It then copies a configuration file and scheme-specific files into the appropriate directories.

    Parameters:
    args (Any): Command-line arguments parsed via argparse.

    Returns:
    None
    """

    # Create the project folder if it doesn't exist
    project_folder_path = os.path.abspath(args.project_folder)
    if not os.path.exists(project_folder_path):
        os.makedirs(project_folder_path)
        logging.info(f"Created project folder: {project_folder_path}")

    # Create the scheme folder within the project folder if it doesn't exist
    scheme = args.scheme  # Move this line up here
    scheme_folder_path = os.path.join(project_folder_path, scheme)
    if not os.path.exists(scheme_folder_path):
        os.makedirs(scheme_folder_path)
        logging.info(f"Created scheme folder: {scheme_folder_path}")

    # Copy the config file to the project folder with scheme name included
    with path('lilo', 'config.file') as config_path:
        dest_config_path = os.path.join(project_folder_path, f"{scheme}_config.yaml")
        shutil.copy(config_path, dest_config_path)
        logging.info(f"Copied config file to {dest_config_path}")

    # Copy the scheme files based on the chosen scheme
    scheme_files = [
        f"{scheme}.primers.csv",
        f"{scheme}.reference.fasta",
        f"{scheme}.scheme.bed",
    ]

    with path('lilo', 'schemes') as schemes_path:
        for file in scheme_files:
            source_file = os.path.join(schemes_path, scheme, file)
            dest_file = os.path.join(scheme_folder_path, file)
            shutil.copy(source_file, dest_file)
            logging.info(f"Copied {file} to {dest_file}")

    # Define the new values based on the copied files' paths
    new_values = {
        'scheme': os.path.join(scheme_folder_path, f"{scheme}.scheme.bed"),
        'reference': os.path.join(scheme_folder_path, f"{scheme}.reference.fasta"),
        'primers': os.path.join(scheme_folder_path, f"{scheme}.primers.csv"),
    }

    # Update the config file
    config_file_name = f"{scheme}_config.yaml"
    for variable, new_value in new_values.items():
        success = update_config_file_with_comments(project_folder_path, config_file_name, variable, new_value)
        if not success:
            logging.error(f"Failed to update {variable} in {config_file_name}")

    # Update the medaka model in the config file
    success = update_config_file_with_comments(project_folder_path, config_file_name, "medaka", args.medaka)
    if not success:
        logging.error(f"Failed to update medaka in {config_file_name}")

    logging.info("Initialization and config update complete.")



def run_lilo():
    # Run snakemake programmatically
    snakemake(
        snakefile="path/to/Snakefile",
        configfile="config.yaml",
        cores=1,  # Number of cores
    )

from typing import Any
import logging


def run_expand_primers(args: Any) -> None:
    """
    Run the expand_primers function and write results to an output file.

    This function takes the input primer file and runs the expand_primers function
    to expand the primers. It then writes the expanded primers to the output file.

    Parameters:
    args (Any): Command-line arguments parsed via argparse, which include `input_file` and `output_file`.

    Returns:
    None
    """

    input_file = args.input_file
    output_file = args.output_file

    logging.info(f"Expanding primers from {input_file}.")

    # Run the expand_primers function
    results = expand_primers(input_file)

    logging.info(f"Writing expanded primers to {output_file}.")

    # Write results to the output file
    with open(output_file, 'w') as f:
        for line in results:
            f.write(f"{line}\n")

    logging.info("Expansion and writing to file completed.")



def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description="LILO: Stitch together Nanopore tiled amplicon data without polishing a reference")
    subparsers = parser.add_subparsers(dest="command")

    # Existing sub-commands
    parser_lilo = subparsers.add_parser("analyse", help="Run snakemake workflow")

    # Sub-command for initializing config
    parser_init = subparsers.add_parser("init", help="Initialize config file")
    parser_init.add_argument("--scheme", choices=["ASFV", "SCoV2"], required=True, help="Select the scheme")
    parser_init.add_argument("--project_folder", default=".", help="Project folder where files should be copied")
    parser_init.add_argument("--medaka", type=str, help="Medaka model", default="r941_min_sup_g507")

    # Sub-command for expand_primers
    parser_expand = subparsers.add_parser("expand_primers", help="Expand primers in a CSV file")
    parser_expand.add_argument("--input_file", help="Path to the input CSV file", required=True)
    parser_expand.add_argument("--output_file", help="Path to the output CSV file", required=True)

    args = parser.parse_args()

    if args.command == "init":
        init_config(args)
    elif args.command == "analyse":
        run_lilo()
    elif args.command == "expand_primers":
        run_expand_primers(args)
    else:
        print("Invalid command. Use --help for usage information.")

if __name__ == "__main__":
    main()
