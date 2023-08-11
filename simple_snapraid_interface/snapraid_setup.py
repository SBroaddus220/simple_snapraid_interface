#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the SnapraidSetup class, which is used to run SnapRAID commands.
"""

import logging
from pathlib import Path
from typing import Optional, List

from simple_snapraid_interface.utilities import utilities

# **********
# Sets up logger
logger = logging.getLogger(__name__)

# **********
class SnapraidSetup:
    """Represents a SnapRAID setup."""
    
    def __init__(self, executable_path: Path) -> None:
        """Instantiates a new SnapraidSetup object.

        Args:
            executable_path (Path): Path to the SnapRAID executable.
        """
        self.executable_path = executable_path
        
        #: Command to sync the SnapRAID setup.
        self.subprocess_sync_command: Optional[List[str]] = None
        
        
    def prepare_sync_subprocess(self) -> List[str]:
        """Prepares the command to sync the SnapRAID setup.

        Raises:
            FileNotFoundError: If the SnapRAID executable is not found.

        Returns:
            List[str]: Command to sync the SnapRAID setup.
        """
        logger.info(f"Preparing the sync subprocess for SnapRAID `{self.executable_path}`.")
        if not self.executable_path.exists():
            raise FileNotFoundError(f"SnapRAID executable at {self.executable_path} not found.")
        
        command = [
            self.executable_path,
            "sync"
        ]
        
        self.subprocess_sync_command = command
        
        return self.subprocess_sync_command
    
    
    async def sync(self, print_output: bool = True) -> None:
        """Syncs the SnapRAID setup.

        Args:
            print_output (bool, optional): Whether to print the output to the console. Defaults to True.
        """
        self.prepare_sync_subprocess()
        logger.info(f"Syncing the SnapRAID setup `{self.executable_path}`.")
        try:
            await utilities.run_command(self.subprocess_sync_command, print_output)
        except RuntimeError as e:
            logger.error(f"Error running sync command: {str(e)}")


# **********
if __name__ == "__main__":
    pass
