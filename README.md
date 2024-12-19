# Artefact Repository REST API

## Overview

This project provides a REST API for managing artefacts in a repository. An artefact is any file that can be stored on disk (e.g., images, documents, source code). The API allows users to organize artefacts in directories and perform operations such as listing, adding, retrieving, and deleting artefacts.

## File Structure

- **api.py**: Main file containing the application logic.
- **artefacts/**: Directory where uploaded artefacts are stored.
- **requirements.txt**: Contains the list of dependencies needed to run the application.
- **README.md**: This documentation file.

## Requirements

- **Python 3.8 or higher**
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python api.py
   ```
2. Access the API at `http://127.0.0.1:5000`.

## API Endpoints

### Artefact Management

- **GET /artefacts/**: Returns a list of available directories.
- **GET /artefacts/\<directory\_id>**: Returns a list of all artefacts in the specified directory.
- **POST /artefacts/\<directory\_id>/\<artefact\_id>**: Uploads an artefact to the specified directory.
- **GET /artefact/\<directory\_id>/\<artefact\_id>**: Retrieves an artefact by ID from the specified directory.
- **DELETE /artefacts/\<directory\_id>**: Deletes a directory and all its artefacts.
- **DELETE /artefacts/\<directory\_id>/\<artefact\_id>**: Deletes an artefact from the specified directory.
- **PUT /artefacts/\<directory\_id>/\<artefact\_id>**: Replaces an existing artefact with a new version.
