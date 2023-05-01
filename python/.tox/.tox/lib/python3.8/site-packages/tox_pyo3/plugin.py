# -*- coding: utf-8 -*-
import logging
try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

import pluggy

hookimpl = pluggy.HookimplMarker("tox")

log = logging.getLogger('pyo3')


@hookimpl
def tox_addoption(parser):
    parser.add_testenv_attribute("pyo3",
                                 "bool",
                                 "Build PyO3 Rust extension",
                                 default=False)


@hookimpl
def tox_testenv_create(venv, action):
    if not venv.envconfig.pyo3:
        return
    venv.envconfig.whitelist_externals.append('maturin')


@hookimpl
def tox_testenv_install_deps(venv, action):
    if not venv.envconfig.pyo3:
        return

    basepath = venv.envconfig.changedir
    if not Path(basepath, 'Cargo.toml').exists():
        log.info("No Rust extension found. Skipping...")
        return
    cmd = venv.getcommandpath("maturin")
    action.setactivity("pyo3", "Building Rust extension module")
    venv._pcall([cmd, "develop"],
                venv=True,
                action=action,
                cwd=basepath,
                redirect=True,
                returnout=True)
