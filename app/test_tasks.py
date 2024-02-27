import pathlib
import time
import unittest

from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch

from app import tasks


class TestTasks(TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        path = pathlib.Path('/tests')
        path.mkdir()
        (path / "backup-20231012-121212.json").touch()
        tasks.BACKUP_DIR = path

    @patch('os.walk')
    @patch('os.remove')
    @patch('os.stat')
    def test_delete_old_backups(self, mock_stat, mock_remove, mock_walk):
        mock_walk.return_value = [(".", [], ["file1.txt", "file2.txt"])]

        mock_stat.return_value.st_mtime = time.time() - (tasks.DAYS * 86400 + 1)

        tasks.delete_old_backups()

        self.assertEqual(mock_remove.call_count, 2)

    @patch('os.walk')
    @patch('os.remove')
    @patch('os.stat')
    def test_delete_old_backups_no_match(self, mock_stat, mock_remove, mock_walk):
        mock_walk.return_value = [(".", [], ["file1.txt", "file2.txt"])]

        mock_stat.return_value.st_mtime = time.time()

        tasks.delete_old_backups()

        mock_remove.assert_not_called()

    @patch('os.walk')
    @patch('os.remove')
    @patch('os.stat')
    def test_delete_old_backups_empty_directory(self, mock_stat, mock_remove, mock_walk):
        mock_walk.return_value = [(".", [], [])]

        tasks.delete_old_backups()

        mock_remove.assert_not_called()

    @patch('app.tasks.call_command')
    @patch('app.tasks.open', create=True)
    @patch('app.tasks.datetime')
    @patch('app.tasks.delete_old_backups')
    def test_create_db_backup(self, mock_delete_old_backups, mock_datetime, mock_open, mock_call_command):
        # Arrange
        mock_datetime.now.return_value.strftime.return_value = "20231012-121212"

        # Act
        result = tasks.create_db_backup()

        # Assert
        self.assertEqual(result, 0)
        mock_open.assert_called_once_with('/tests/backup-20231012-121212.json', 'w')
        mock_call_command.assert_called_once_with('dumpdata', stdout=mock_open().__enter__())
        mock_delete_old_backups.assert_called_once()


if __name__ == '__main__':
    unittest.main()
