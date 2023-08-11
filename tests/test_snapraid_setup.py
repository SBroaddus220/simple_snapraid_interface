#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 
Test cases for the SnapraidSetup class.
"""

import asyncio
from pathlib import Path

import unittest
from unittest import mock
from unittest.mock import AsyncMock, MagicMock, PropertyMock

from simple_snapraid_interface.snapraid_setup import SnapraidSetup

# ****************
class TestSnapraidSetup(unittest.TestCase):

    # ****************
    def setUp(self):
            
        # Mocks the Snapraid executable
        self.SNAPRAID_PATH = MagicMock(spec=Path)
        type(self.SNAPRAID_PATH).stat = PropertyMock(return_value=MagicMock(st_mode=0o700))
    
        # Generic setup instance
        self.snapraid_setup = SnapraidSetup(self.SNAPRAID_PATH)
    
    # ****************
    # Prepare sync subprocess tests
    def test_prepare_sync_subprocess_command_setup(self):
        # Arrange
        expected_command = [self.snapraid_setup.executable_path, "sync"]

        with mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()) as mock_subprocess, \
            mock.patch('pathlib.Path.exists', return_value=True):
            # Act
            command = self.snapraid_setup.prepare_sync_subprocess()

            # Assert
            self.assertEqual(command, expected_command)


    def test_prepare_sync_subprocess_no_executable(self):
        # Arrange
        self.snapraid_setup.executable_path = Path('/fake/path')
        with mock.patch('pathlib.Path.exists', return_value=False):
            # Act & Assert
            with self.assertRaises(FileNotFoundError):
                self.snapraid_setup.prepare_sync_subprocess()


    def test_prepare_sync_subprocess_idempotence(self):
        # Arrange
        with mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()):

            # Act
            command1 = self.snapraid_setup.prepare_sync_subprocess()
            command2 = self.snapraid_setup.prepare_sync_subprocess()

            # Assert
            self.assertEqual(command1, command2)


    # ****************
    # Sync tests
    def test_sync_method(self):
        # Arrange
        with mock.patch("simple_snapraid_interface.utilities.utilities.run_command", return_value=None) as mock_run_command, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch('asyncio.create_subprocess_exec', new=mock.MagicMock()):
            # Act
            asyncio.run(self.snapraid_setup.sync())

            # Assert
            mock_run_command.assert_called_once()
            
            
    def test_sync_method_prepares_subprocess(self):
        # Arrange
        mock_subprocess_command = mock.Mock()

        # Manually sets the attribute to the required value to simulate prepare sync subprocess call
        def side_effect():
            self.snapraid_setup.subprocess_sync_command = mock_subprocess_command
            return mock_subprocess_command

        with mock.patch("simple_snapraid_interface.utilities.utilities.run_command", return_value=None) as mock_run_command, \
            mock.patch('pathlib.Path.exists', return_value=True), \
            mock.patch.object(SnapraidSetup, 'prepare_sync_subprocess', side_effect=side_effect) as mock_prepare_sync_subprocess:

            # Act
            asyncio.run(self.snapraid_setup.sync())

            # Assert
            mock_prepare_sync_subprocess.assert_called_once()
            mock_run_command.assert_called_once()


# ****************
if __name__ == '__main__':
    unittest.main()
