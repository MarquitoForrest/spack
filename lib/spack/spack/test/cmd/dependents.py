# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

from llnl.util.tty.color import color_when

import spack.store
from spack.main import SpackCommand

dependents = SpackCommand('dependents')


def test_immediate_dependents(mock_packages):
    out = dependents('libelf')
    actual = set(re.split(r'\s+', out.strip()))
    assert actual == set(['dyninst', 'libdwarf',
                          'patch-a-dependency', 'patch-several-dependencies'])


def test_transitive_dependents(mock_packages):
    out = dependents('--transitive', 'libelf')
    actual = set(re.split(r'\s+', out.strip()))
    assert actual == set(
        ['callpath', 'dyninst', 'libdwarf', 'mpileaks', 'multivalue_variant',
         'singlevalue-variant-dependent',
         'patch-a-dependency', 'patch-several-dependencies'])


@pytest.mark.db
def test_immediate_installed_dependents(mock_packages, database):
    with color_when(False):
        out = dependents('--installed', 'libelf')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['dyninst', 'libdwarf']])

    libelf = spack.store.db.query_one('libelf')
    expected = set([d.dag_hash(7) for d in libelf.dependents()])

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependents(mock_packages, database):
    with color_when(False):
        out = dependents('--installed', '--transitive', 'fake')

    lines = [l for l in out.strip().split('\n') if not l.startswith('--')]
    hashes = set([re.split(r'\s+', l)[0] for l in lines])

    expected = set([spack.store.db.query_one(s).dag_hash(7)
                    for s in ['zmpi', 'callpath^zmpi', 'mpileaks^zmpi']])

    assert expected == hashes
