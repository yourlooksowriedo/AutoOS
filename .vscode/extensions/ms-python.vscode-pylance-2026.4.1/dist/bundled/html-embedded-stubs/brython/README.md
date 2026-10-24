# Brython stubs

These stubs describe Brython's browser-only Python APIs. Pylance makes them
available only to Python virtual documents extracted from Brython HTML scripts.

The generated surface is based on Brython 3.14.3, revision
`a0ffdd8dfd9725604439c0f35d64c4adff0d6292`. `browser/__init__.pyi`, `browser/html.pyi`,
`browser/aio.pyi`, `browser/ajax.pyi`, `browser/svg.pyi`,
`browser/webcomponent.pyi`, `browser/worker.pyi`, and `javascript.pyi` contain
curated types for APIs that Brython creates dynamically in JavaScript. The
remaining `browser` modules are generated structurally from Brython's Python
source.

See `LICENCE.txt` for Brython's BSD 3-Clause license.
