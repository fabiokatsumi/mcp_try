#!/usr/bin/env python3
"""
Cleanup script to remove empty files and move remaining files to archive
"""

import os
import shutil


def remove_empty_files():
    """Remove all empty files from the root directory."""
    print("🧹 Cleaning up empty files...")
    
    # Get all files in current directory
    for item in os.listdir('.'):
        if os.path.isfile(item):
            # Check if file is empty (0 bytes)
            if os.path.getsize(item) == 0:
                print(f"Removing empty file: {item}")
                os.remove(item)
    
    print("✅ Empty files cleanup complete")


def move_remaining_files():
    """Move any remaining files that shouldn't be in root."""
    print("📦 Moving remaining files...")
    
    # Files that should stay in root
    essential_files = {
        '.dockerignore',
        'Dockerfile.production', 
        'README.md',
        'requirements.txt',
        'requirements-dev.txt',
        'setup.py',
        'deploy_dokploy.sh',
        'final_organize.py',
        'cleanup_root.py'  # This script itself
    }
    
    # Check all files in root
    for item in os.listdir('.'):
        if os.path.isfile(item) and item not in essential_files:
            print(f"Moving {item} to archive/misc/")
            
            # Create misc directory if needed
            os.makedirs('archive/misc', exist_ok=True)
            
            # Move the file
            try:
                shutil.move(item, f'archive/misc/{item}')
                print(f"✅ Moved {item}")
            except Exception as e:
                print(f"❌ Failed to move {item}: {e}")


def main():
    """Main cleanup function."""
    print("🚀 Root Directory Cleanup")
    print("=" * 50)
    
    remove_empty_files()
    move_remaining_files()
    
    print("\n✅ Root directory cleanup complete!")
    print("Root now contains only essential files.")


if __name__ == "__main__":
    main()
