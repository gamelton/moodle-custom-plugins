# Moodle Custom Plugin Copier

Moodle has a plugin design issue: plugin directories can be located anywhere within the Moodle directory. The Moodle upgrade guide recommends cleaning out the Moodle directory before upgrading, which means you need to manually copy the plugin directories from the backup to the new Moodle version. Unfortunately, Moodle does not provide information about where plugins are installed.  
This Python script is designed to help identify and copy Moodle plugin directories. It retrieves the plugin name from the command output, lists the subdirectories inside the Moodle directory, and then attempts to locate the plugin directory.

## Usage
The script requires two parameters: the source Moodle directory and the destination Moodle directory. It will copy the plugin after asking for your confirmation.  
1. Ensure Python is installed on your system.
2. Run the script with the following command:
```
python moodle-custom-plugins.py <source_moodle_directory> <destination_moodle_directory>
```
3. Follow the prompts to confirm the plugin directory copy.
