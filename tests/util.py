import contextlib
import distutils.spawn  # pylint: disable=no-name-in-module,import-error
import functools
import os
import shutil
import sys
import tempfile

import pytest
from pkg_resources import ResolutionError  # type: ignore
from pkg_resources import Requirement, resource_filename

from cwltool.context import LoadingContext, RuntimeContext
from cwltool.factory import Factory
from cwltool.resolver import Path
from cwltool.singularity import is_version_2_6, is_version_3_or_newer
from cwltool.utils import onWindows, subprocess, windows_default_container_id


def get_windows_safe_factory(
    runtime_context=None,  # type: RuntimeContext
    loading_context=None,  # type: LoadingContext
    executor=None,  # type: Any
):  # type: (...) -> Factory
    if onWindows():
        if not runtime_context:
            runtime_context = RuntimeContext()
        runtime_context.find_default_container = functools.partial(
            force_default_container, windows_default_container_id
        )
        runtime_context.use_container = True
        runtime_context.default_container = windows_default_container_id
    return Factory(executor, loading_context, runtime_context)


def force_default_container(default_container_id, _):
    return default_container_id


def get_data(filename):
    # normalizing path depending on OS or else it will cause problem when joining path
    filename = os.path.normpath(filename)
    filepath = None
    try:
        filepath = resource_filename(Requirement.parse("cwltool"), filename)
    except ResolutionError:
        pass
    if not filepath or not os.path.isfile(filepath):
        filepath = os.path.join(os.path.dirname(__file__), os.pardir, filename)
    return str(Path(filepath).resolve())


needs_docker = pytest.mark.skipif(
    not bool(distutils.spawn.find_executable("docker")),
    reason="Requires the docker executable on the " "system path.",
)

needs_singularity = pytest.mark.skipif(
    not bool(distutils.spawn.find_executable("singularity")),
    reason="Requires the singularity executable on the system path.",
)

needs_singularity_2_6 = pytest.mark.skipif(
    not (distutils.spawn.find_executable("singularity") and is_version_2_6()),
    reason="Requires that version 2.6.x of singularity executable version is on the system path.",
)

needs_singularity_3_or_newer = pytest.mark.skipif(
    not (distutils.spawn.find_executable("singularity") and is_version_3_or_newer),
    reason="Requires that version 2.6.x of singularity executable version is on the system path.",
)


windows_needs_docker = pytest.mark.skipif(
    onWindows() and not bool(distutils.spawn.find_executable("docker")),
    reason="Running this test on MS Windows requires the docker executable "
    "on the system path.",
)


def get_main_output(args, env=None):
    process = subprocess.Popen(
        [sys.executable, "-m", "cwltool"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()


@contextlib.contextmanager
def temp_dir(suffix=""):
    c_dir = tempfile.mkdtemp(suffix, dir=os.curdir)
    try:
        yield c_dir
    finally:
        shutil.rmtree(c_dir, ignore_errors=True)


@contextlib.contextmanager
def working_directory(path):
    """Change working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    # before python 3.6 chdir doesn't support paths from pathlib
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(str(prev_cwd))
