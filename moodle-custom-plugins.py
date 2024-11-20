#!/usr/bin/env python3
import subprocess
import os
import sys
import shutil

# Ensure two arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script.py <source_moodle_dir> <destination_moodle_dir>")
    sys.exit(1)
source_dir = sys.argv[1]
dest_dir = sys.argv[2]
# Verify directories existence
if not os.path.isdir(source_dir):
    print(f"Error: Source directory '{source_dir}' does not exist.")
    sys.exit(1)
if not os.path.isdir(dest_dir):
    print(f"Error: Destination directory '{dest_dir}' does not exist.")
    sys.exit(1)

# Command to get the list of custom plugins
command = ['sudo', '-u', 'www-data', '/usr/bin/php', os.path.join(source_dir, 'admin', 'cli', 'uninstall_plugins.php'), '--show-contrib']
try:
    # Execute the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")
    sys.exit(1)

# Retrieve plugin names from the command output
plugin_names = [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
for plugin_name in plugin_names:
    # Remove underscores to get the target sequence of characters
    target_sequence = plugin_name.replace('_', '')
    found = False
    best_match_length = -1
    found_path = ''
    # Use os.walk to recursively search directories
    for root, dirs, files in os.walk(source_dir):
        # Skip hidden directories and irrelevant deep paths
        dirs[:] = [d for d in dirs if not d.startswith('.') and 'vendor' not in root and 'simplesamlphp' not in root]
        for directory in dirs:
            full_path = os.path.join(root, directory)
            # Create character sequence from the relative path
            relative_path = os.path.relpath(full_path, source_dir).replace('/', '')
            # Check if path matches the plugin name
            i = 0
            j = 0
            while i < len(target_sequence) and j < len(relative_path):
                if target_sequence[i] == relative_path[j]:
                    i += 1
                j += 1
            
            if i == len(target_sequence):
                if not found or len(found_path) > len(relative_path):
                    # Prefer the longest relative path that matches (rather than the shortest).
                    if len(relative_path) > best_match_length:
                        best_match_length = len(relative_path)
                        found_path = full_path
                        found = True
        
        if found:
            # Construct destination plugin path
            dest_plugin_relative_path = os.path.relpath(found_path, source_dir)
            dest_plugin_path = os.path.join(dest_dir, dest_plugin_relative_path)
            # Ask for confirmation before copying
            confirmation = input(f"Copy plugin from '{found_path}' to '{dest_plugin_path}'? [y/N]: ").strip().lower()
            if confirmation != 'y':
                print("Operation cancelled.")
                sys.exit(1)
            # Create destination directories if needed and copy
            os.makedirs(os.path.dirname(dest_plugin_path), exist_ok=True)
            shutil.copytree(found_path, dest_plugin_path, dirs_exist_ok=True)
            print(f"Copied {plugin_name} to {dest_plugin_path}")
            break
    
    if not found:
        print(f"{plugin_name}: No existing directory found.")
