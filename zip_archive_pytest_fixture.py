import io
import os
from zipfile import ZipFile

import pytest

@pytest.fixture
def archive():
    archive_file = io.BytesIO()

    # Get the contents of the templates:
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with ZipFile(archive_file, 'w') as zipped:
        for root, subdir, files in os.walk(current_dir + '/templates'):
            for file in files:
                # https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
                zipped.write(os.path.join(root, file),
                             arcname=os.path.relpath(os.path.join(root, file), os.path.join(root, '..')).replace("templates/", ""))
                                       # ^^ Per the comment on Stack Overflow:
                                       # That would let you zip a directory from any working directory, without getting the full absolute paths in the archive
                                       # From: https://stackoverflow.com/users/294743/reimund

    # Reset the read pointer ("re-opens" the file):
    archive_file.seek(0)

    yield archive_file

    archive_file.close()
