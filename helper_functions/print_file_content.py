

import os


def print_file_content(selected_file_path: str) -> str:
    """Process the selected file with comprehensive error handling"""
    
    if not selected_file_path:
        print("Error: No file path provided")
        return
    
    print(f"Processing file: {selected_file_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(selected_file_path):
            raise FileNotFoundError(f"File not found: {selected_file_path}")
        
        # Check if it's actually a file
        if not os.path.isfile(selected_file_path):
            raise IsADirectoryError(f"Path is a directory, not a file: {selected_file_path}")
        
        # Check file size before reading (optional safety measure)
        file_size = os.path.getsize(selected_file_path)
        if file_size > 100 * 1024 * 1024:  # 100MB limit
            print(f"Warning: File is large ({file_size / (1024*1024):.2f} MB). Consider processing in chunks.")
        
        # Read file content with multiple encoding fallbacks
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(selected_file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    print(f"File content (read with {encoding}):\n{content}")
                    # Do something with the content
                    break  # Successfully read, exit the loop
            except UnicodeDecodeError:
                if encoding == encodings[-1]:  # Last encoding attempt
                    raise UnicodeDecodeError(
                        f"Unable to decode file with any of the attempted encodings: {encodings}"
                    )
                continue  # Try next encoding
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        
    except IsADirectoryError as e:
        print(f"Error: Path is a directory - {e}")
        
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        
    except UnicodeDecodeError as e:
        print(f"Error: Unable to decode file - {e}")
        print("The file may be binary or use an uncommon encoding")
        
    except IOError as e:
        print(f"Error: I/O operation failed - {e}")
        
    except OSError as e:
        print(f"Error: OS-related error - {e}")
        
    except MemoryError as e:
        print(f"Error: File too large to read into memory - {e}")
        
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        # You might want to log this for debugging
        import traceback
        print(f"Detailed traceback:\n{traceback.format_exc()}")
    
    else:
        print("File processed successfully")
    
    finally:
        print("File processing operation completed")