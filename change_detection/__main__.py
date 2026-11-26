import sys
from functools import partial
from pathlib import Path

from change_detection.adapter.git_command_repository import GitCommandRepository
from change_detection.adapter.output_file import write_output_file
from change_detection.presentation.command_line import run_change_detection
from change_detection.usecase.detect_change import detect_change

sys.exit(run_change_detection(sys.argv[1:], partial(detect_change, GitCommandRepository(Path.cwd())), write_output_file))
