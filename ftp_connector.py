from ftplib import FTP
from datetime import datetime
import dotenv
import os

# Load env
dotenv.load_dotenv()

def connect_to_ftp(ip_address, username, password):
    """
    Establish a connection to an FTP server.

    Args:
        ip_address (str): The IP address of the FTP server.
        username (str): The username to use for authentication.
        password (str): The password to use for authentication.

    Returns:
        ftp (FTP): An FTP object representing the connection to the server.
    """
    try:
        # Create an FTP object
        ftp = FTP(ip_address)
        
        # Login to the FTP server
        ftp.login(user=username, passwd=password)
        
        print("Connected to the FTP server.")
        return ftp
    
    except Exception as e:
        print(f"Failed to connect to the FTP server: {e}")
        return None
    

def get_directories(ftp):
    """
    Get the list of directories (dates) in the current working directory.

    Args:
        ftp (FTP): An FTP object representing the connection to the server.

    Returns:
        directories (list): A list of directory names.
    """
    try:
        # Get the list of directories in the current working directory
        directories = ftp.nlst()
        
        return directories
    
    except Exception as e:
        print(f"Failed to get directories: {e}")
        return []


def get_files_in_directory(ftp, directory):
    """
    Get the list of files in a directory.

    Args:
        ftp (FTP): An FTP object representing the connection to the server.
        directory (str): The name of the directory.

    Returns:
        files (list): A list of file names.
    """
    try:
        # Change the current working directory
        ftp.cwd(directory)
        
        # Get the list of files in the current working directory
        files = ftp.nlst()
        
        # Change the current working directory back to the parent directory
        ftp.cwd('/')
        
        return files
    
    except Exception as e:
        print(f"Failed to get files in directory {directory}: {e}")
        return []
    

def get_file_size(ftp, directory, file):
    """
    Get the size of a file in bytes.

    Args:
        ftp (FTP): An FTP object representing the connection to the server.
        directory (str): The name of the directory containing the file.
        file (str): The name of the file.

    Returns:
        size (int): The size of the file in bytes.
    """
    try:
        # Change the current working directory
        ftp.cwd(directory)
        
        # Get the size of the file
        size = ftp.size(file)
        
        # Change the current working directory back to the parent directory
        ftp.cwd('/')
        
        return size
    
    except Exception as e:
        print(f"Failed to get size of file {file} in directory {directory}: {e}")
        return None


def parse_date(date_string):
    """
    Parse a date string in the format 'YYYYMMDD' into a datetime object.

    Args:
        date_string (str): The date string to parse.

    Returns:
        date (datetime): A datetime object representing the date.
    """
    try:
        date = datetime.strptime(date_string, '%Y%m%d')
        
        return date
    
    except Exception as e:
        print(f"Failed to parse date: {e}")
        return None


def download_file(ftp, directory, file, output_directory):
    """
    Download a file from the FTP server.

    Args:
        ftp (FTP): An FTP object representing the connection to the server.
        directory (str): The name of the directory containing the file.
        file (str): The name of the file.
        output_directory (str): The local directory to save the file to.
    """
    try:
        # Change the current working directory
        ftp.cwd(directory)
        
        # Open a local file for writing
        with open(os.path.join(output_directory, file), 'wb') as output_file:
            # Download the file from the FTP server
            ftp.retrbinary(f'RETR {file}', output_file.write)
        
        # Change the current working directory back to the parent directory
        ftp.cwd('/')
        
        print(f"Downloaded {file} to {output_directory}")
    
    except Exception as e:
        print(f"Failed to download {file} from directory {directory}: {e}")


def clear_directory(directory):
    """
    Clear the contents of a directory.

    Args:
        directory (str): The directory to clear.
    """
    try:
        # Get a list of files in the directory
        files = os.listdir(directory)
        
        # Iterate over each file
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(directory, file)
            
            # Check if the file is a file (not a directory)
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)
        
        print(f"Cleared {directory}")
    
    except Exception as e:
        print(f"Failed to clear {directory}: {e}")


def main():
    ip_address = os.getenv("FTP_IP_ADDRESS")
    username = os.getenv("FTP_USERNAME")
    password = os.getenv("FTP_PASSWORD")
    
    # Establish a connection to the FTP server
    ftp = connect_to_ftp(ip_address, username, password)
    
    if ftp is not None:
        # Get the list of directories (dates)
        directories = get_directories(ftp)
        
        # Parse the start and end dates from user input
        start_date_input = input("Enter the start date (YYYYMMDD): ")
        end_date_input = input("Enter the end date (YYYYMMDD): ")
        
        start_date = parse_date(start_date_input)
        end_date = parse_date(end_date_input)
        
        # Check if the start and end dates are valid
        if start_date is not None and end_date is not None:
            # Get the output directory
            output_directory = os.path.join(os.getcwd(), 'Recordings')
            
            # Check if the output directory exists
            if not os.path.exists(output_directory):
                # Create the output directory
                os.makedirs(output_directory)
            
            # Clear the contents of the output directory
            clear_directory(output_directory)
            
            # Iterate over each directory (date)
            for directory in directories:
                # Parse the date from the directory name
                directory_date = parse_date(directory)
                
                # Check if the directory date is within the user-specified range
                if start_date <= directory_date <= end_date:
                    # Get the list of files in the directory
                    files = get_files_in_directory(ftp, directory)
                    
                    # Iterate over each file
                    for file in files:
                        file_size = get_file_size(ftp, directory, file)
                        
                        # Check if the file size is valid
                        if file_size is not None:
                            # Check if the file meets the conditions
                            # if ("i" in file and "0381998408" in file) or file.endswith("405") or file.endswith("400"):
                            if ("i" in file and "0381998408" in file):
                                # Check if the file is under 1 MB
                                if file_size < 1000 * 1024:
                                    # Download the file
                                    download_file(ftp, directory, file, output_directory)
        
        
        # Close the FTP connection
        ftp.quit()

if __name__ == "__main__":
    ftp_main()