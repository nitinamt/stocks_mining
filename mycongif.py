import configparser
import os

class ConfigManager:
    """
    Manages configuration settings stored in an INI-style file.

    Configuration files are structured into sections, each containing key-value pairs.
    Example:
    [Database]
    host = localhost
    port = 5432
    user = admin

    [API]
    api_key = abcdef12345
    base_url = https://api.example.com
    """

    def __init__(self, config_file_path='config.ini'):
        """
        Initializes the ConfigManager with the path to the configuration file.

        Args:
            config_file_path (str): The path to the INI configuration file.
                                    Defaults to 'config.ini' in the current directory.
        """
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self._load_config() # Load existing config when the manager is initialized

    def _load_config(self):
        """
        Loads configuration data from the specified file.
        If the file does not exist, an empty configuration is used.
        """
        try:
            # Read the configuration file.
            # If the file doesn't exist, config.read() returns an empty list,
            # and subsequent operations will work on an empty config object.
            self.config.read(self.config_file_path)
            print(f"Configuration loaded from: {self.config_file_path}")
        except Exception as e:
            print(f"Error loading configuration file {self.config_file_path}: {e}")
            # In case of a severe error (e.g., file corruption),
            # we might want to initialize with a fresh config.
            self.config = configparser.ConfigParser()


    def save_config(self):
        """
        Saves the current configuration data back to the file.
        Creates the file if it does not exist.
        """
        try:
            # Ensure the directory for the config file exists
            os.makedirs(os.path.dirname(self.config_file_path) or '.', exist_ok=True)
            with open(self.config_file_path, 'w') as configfile:
                self.config.write(configfile)
            print(f"Configuration saved to: {self.config_file_path}")
        except Exception as e:
            print(f"Error saving configuration file {self.config_file_path}: {e}")

    def add_key(self, section, key, value):
        """
        Adds or updates a configuration key-value pair within a specified section.
        If the section does not exist, it will be created.

        Args:
            section (str): The name of the section (e.g., 'Database', 'API').
            key (str): The name of the configuration key (e.g., 'host', 'api_key').
            value (str): The value to be stored for the key. Note: all values are stored as strings.
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
            print(f"Created new section: [{section}]")

        self.config.set(section, key, str(value))
        print(f"Added/Updated key: [{section}]{key} = {value}")

    def get_key(self, section, key, default=None):
        """
        Retrieves the value for a specified configuration key from a section.

        Args:
            section (str): The name of the section.
            key (str): The name of the configuration key.
            default (any, optional): The value to return if the section or key is not found.
                                     Defaults to None.

        Returns:
            str: The value of the key as a string, or the default value if not found.
        """
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            print(f"Warning: Key '{key}' not found in section '{section}'. Returning default value.")
            return default
        except Exception as e:
            print(f"Error getting key [{section}]{key}: {e}")
            return default

    def get_section(self, section):
        """
        Retrieves all key-value pairs for a specified section as a dictionary.

        Args:
            section (str): The name of the section.

        Returns:
            dict: A dictionary of key-value pairs for the section, or an empty dictionary
                  if the section does not exist.
        """
        if self.config.has_section(section):
            return dict(self.config.items(section))
        else:
            print(f"Warning: Section '{section}' not found.")
            return {}

    def remove_key(self, section, key):
        """
        Removes a specific key from a section.

        Args:
            section (str): The name of the section.
            key (str): The name of the key to remove.

        Returns:
            bool: True if the key was removed, False otherwise.
        """
        if self.config.has_option(section, key):
            self.config.remove_option(section, key)
            print(f"Removed key: [{section}]{key}")
            return True
        else:
            print(f"Warning: Key '{key}' not found in section '{section}'. Cannot remove.")
            return False

    def remove_section(self, section):
        """
        Removes an entire section from the configuration.

        Args:
            section (str): The name of the section to remove.

        Returns:
            bool: True if the section was removed, False otherwise.
        """
        if self.config.has_section(section):
            self.config.remove_section(section)
            print(f"Removed section: [{section}]")
            return True
        else:
            print(f"Warning: Section '{section}' not found. Cannot remove.")
            return False

# # --- Example Usage ---
# if __name__ == "__main__":
#     # Define a custom config file path for testing
#     test_config_file = 'my_project_settings.ini'

#     print("--- Initializing ConfigManager ---")
#     config_manager = ConfigManager(test_config_file)

#     # --- Adding Configuration ---
#     print("\n--- Adding Configuration ---")
#     config_manager.add_key('Database', 'host', 'localhost')
#     config_manager.add_key('Database', 'port', '5432')
#     config_manager.add_key('Database', 'user', 'admin_user')
#     config_manager.add_key('Database', 'password', 'secure_password_123')

#     config_manager.add_key('API', 'api_key', 'your_secret_api_key_here')
#     config_manager.add_key('API', 'base_url', 'https://api.myapp.com/v1')
#     config_manager.add_key('API', 'timeout_seconds', 30) # Value will be stored as string "30"

#     config_manager.add_key('Features', 'enable_logging', True) # Value will be stored as string "True"
#     config_manager.add_key('Features', 'max_retries', 5)

#     # --- Saving Configuration ---
#     print("\n--- Saving Configuration ---")
#     config_manager.save_config()

#     # Simulate reloading the application by creating a new ConfigManager instance
#     print("\n--- Reloading ConfigManager to verify persistence ---")
#     reloaded_config_manager = ConfigManager(test_config_file)

#     # --- Accessing Configuration ---
#     print("\n--- Accessing Configuration ---")
#     db_host = reloaded_config_manager.get_key('Database', 'host')
#     db_port = reloaded_config_manager.get_key('Database', 'port')
#     api_key = reloaded_config_manager.get_key('API', 'api_key')
#     log_enabled = reloaded_config_manager.get_key('Features', 'enable_logging')
#     timeout = reloaded_config_manager.get_key('API', 'timeout_seconds', 60) # Test with default

#     print(f"Database Host: {db_host}")
#     print(f"Database Port: {db_port}")
#     print(f"API Key: {api_key}")
#     print(f"Logging Enabled: {log_enabled} (Type: {type(log_enabled)})") # Note: value is string "True"
#     print(f"API Timeout: {timeout}")

#     # Accessing a non-existent key
#     non_existent_key = reloaded_config_manager.get_key('NonExistentSection', 'some_key', 'default_value')
#     print(f"Non-existent key with default: {non_existent_key}")

#     # Get an entire section
#     db_section = reloaded_config_manager.get_section('Database')
#     print(f"\nDatabase Section: {db_section}")

#     # --- Modifying Configuration ---
#     print("\n--- Modifying Configuration ---")
#     reloaded_config_manager.add_key('Database', 'port', '5433') # Update port
#     reloaded_config_manager.add_key('Features', 'max_retries', 10) # Update retries
#     reloaded_config_manager.save_config()

#     # Verify modification
#     print("\n--- Verifying Modification ---")
#     updated_port = reloaded_config_manager.get_key('Database', 'port')
#     updated_retries = reloaded_config_manager.get_key('Features', 'max_retries')
#     print(f"Updated Database Port: {updated_port}")
#     print(f"Updated Max Retries: {updated_retries}")

#     # --- Removing Keys and Sections ---
#     print("\n--- Removing Keys and Sections ---")
#     reloaded_config_manager.remove_key('Database', 'password')
#     reloaded_config_manager.remove_section('Features')
#     reloaded_config_manager.save_config()

#     print("\n--- Verifying Removal ---")
#     password_after_removal = reloaded_config_manager.get_key('Database', 'password', 'NOT_FOUND')
#     features_section_after_removal = reloaded_config_manager.get_section('Features')
#     print(f"Password after removal: {password_after_removal}")
#     print(f"Features section after removal: {features_section_after_removal}")

#     # Clean up the test config file
#     if os.path.exists(test_config_file):
#         os.remove(test_config_file)
#         print(f"\nCleaned up test config file: {test_config_file}")
