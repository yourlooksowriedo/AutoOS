## Stub-Generation for native stubs

This folder has a couple of python scripts used for extracting stubs from native python libs.

You run it like so:

-   python -m pip install <lib you want to scrape>
-   python -m scrape_lib <path to site-packages/lib name> <path to site-packages> <output folder>

Stubs will be generated in the output folder. After that's done, you can copy them over the bundled stubs.

See the launch.json for examples.

## Brython browser stubs

`generate_brython_stubs.py` produces the runtime stubs used for Python embedded in Brython HTML.
It downloads the pinned Brython revision by default:

```console
python generate_brython_stubs.py --output ../bundled/html-embedded-stubs/brython
```

Pass `--source <path>` to generate from a Git checkout at the pinned Brython revision. The
generator rejects other commits so the generated provenance stays accurate. Use `--check` to
verify that the checked-in output matches the pinned source without modifying files.
