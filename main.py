import os
import dotenv
import ftp_connector 
import random
import logging
from transcribe import speech_to_text, categorise_participents, \
    review_call


# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def update_ftp_files():
    """Update FTP files if user chooses to do so"""
    update_ftp = input("Do you want to update FTP files? (y/n): ")
    if update_ftp.lower() == 'y':
        ftp_connector.main()
    elif update_ftp.lower() == 'n':
        print("Skipping FTP update.")
    else:
        print("Invalid input. Defaulting to skipping FTP update.")

def clear_notes_directory():
    """Clear the Notes directory if user chooses to do so"""
    clear_notes_dir = input("Do you want to clear the Notes directory? (y/n): ")
    notes_dir = 'Notes'
    if clear_notes_dir.lower() == 'y':
        if os.path.exists(notes_dir):
            for filename in os.listdir(notes_dir):
                os.remove(os.path.join(notes_dir, filename))
                logging.info(f"Deleted file: {filename}")
            logging.info(f"Cleared Notes directory: {notes_dir}")
        else:
            os.makedirs(notes_dir)
            logging.info(f"Created Notes directory: {notes_dir}")

def get_files_to_process():
    """Get a list of all files in the Recordings directory"""
    filenames = os.listdir('Recordings')
    return random.sample(filenames, min(len(filenames), 10))

def get_summarization_method():
    """Ask user if they want to use local or OpenAI API for summarization and classification"""
    while True:
        local_or_remote_llm = input("Do you want to use local whisper model and LLM or OpenAI API for summarization and classification? (l/r): ")
        if local_or_remote_llm.lower() in ['l', 'r']:
            return local_or_remote_llm.lower()
        else:
            print("Invalid input. Please enter 'l' for local whisper model and LLM or 'r' for OpenAI API: ")

def process_file(filename, local_or_remote_llm):
    """Process a file by transcribing it, summarizing it, and reviewing it with LLM"""
    try:
        print(f"Processing file: {filename}")
        logging.info(f"Processing file: {filename}")
        filepath = os.path.join('Recordings', filename)
        transcription = speech_to_text(filepath, local_or_remote_llm)
        conversation = categorise_participents(transcription, local_or_remote_llm)
        print(f"Transcription: {conversation}")
        logging.info(f"Transcription: {conversation}")
        review = review_call(conversation, local_or_remote_llm)
        print(f"LLM Call review: {review}")
        logging.info(f"LLM Call review: {review}")
        with open(os.path.join('Notes', f"{filename.split('.')[0]}.txt"), "w") as f:
            f.write(f"Transcription: {conversation}\n\nReviewed Transcription: {review}")
    except Exception as e:
        logging.error(f"Error processing file: {filename} - {e}")

def main():
    """Main function that calls all other functions"""
    dotenv.load_dotenv()
    update_ftp_files()
    clear_notes_directory()
    files_to_process = get_files_to_process()
    summarization_method = get_summarization_method()
    for i, filename in enumerate(files_to_process):
        print(f"{i}: {filename}")
        process_file(filename, summarization_method)

if __name__ == "__main__":
    main()