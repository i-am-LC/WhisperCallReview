# Support Call Review System

## Features

* Transcribes audio files using Whisper speech-to-text.
* Identifies participants in the conversation using categorisation LLM.
* Reviews conversations with either local LLM or OpenAI API for summarisation and classification.

## Requirements

* Python 3.x
* `dotenv` library for loading environment variables
* `transcribe.py` script for speech-to-text functionality
* `chatopenai` and `chattoollama` libraries for LLM interactions

## Installation

1. Clone the repository: `git clone https://github.com/your-username/support-call-review-system.git`
2. Create a `.env` file in the root directory with your OpenAI API key and FTP server details
3. Install dependencies using `pip install -r requirements.txt`

## Usage

1. Run the `main.py` script to start the review process
2. Choose whether to use local LLM or OpenAI API for summarization and classification
3. Select the file(s) to be reviewed
4. The system will transcribe, categorize, and review the conversations using either local LLM or OpenAI API
