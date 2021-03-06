# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for repos.yaml configuration file.

.. literalinclude:: ../spack/schema/repos.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'repos': {
        'type': 'array',
        'default': [],
        'items': {'type': 'string'},
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack repository configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
