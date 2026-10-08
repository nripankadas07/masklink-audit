# masklink-audit

Audit row-aligned source/masked export pairs for unchanged/erased identifiers, per-domain collisions, inconsistent tokens and changed non-ID anchor cells; reports omit cell values.

For data engineers verifying pseudonymized csv exports before downstream joins. Export transformations can silently break identifier linkage or collapse distinct identifiers. Independent checking is useful when the transformation engine is outside the team's control.

## Install and first useful result

Python 3.10+; no runtime dependencies, accounts, API keys or network requests from the tool.
Installation may download setuptools from PyPI. No package has been published to a registry.

```sh
git clone https://github.com/nripankadas07/masklink-audit.git
cd masklink-audit
python -m venv .venv
# POSIX; Windows: .venv\Scripts\activate
. .venv/bin/activate
python -m pip install .
masklink-audit manifest.json
```

The included fixtures are synthetic. `python demo.py` prints the same real example.
CLI exit codes: 0 = accepted/unchanged, 1 = findings/changed, 2 = invalid input or read failure.
Reports are JSON. Input contracts are explicit; see the included JSON files for their schemas.
Use `--help` for arguments. Paths are local and UTF-8. The tool never writes input/output data.

## Check the implementation

```sh
python verify.py
```

Runs 11 meaningful unit checks, Python compilation, then installs this package into a
new virtual environment and exercises accepted, findings and invalid-input CLI cases outside
the source directory. CI repeats this on Python 3.10, 3.12 and 3.14.

## Limits

Does not transform or anonymize data and does not certify privacy. Requires identical schemas and preserved row order; reordered rows cannot reliably be detected without unchanged anchor columns. All non-ID columns must remain exact. Checks only declared identifier columns, not free-text leaks or quasi-identifiers. Full tables and identifier maps held in memory; source and masked data remain sensitive. Reports expose row/column/domain metadata. UTF-8 CSV only, no fuzzy identity matching.

See [RESEARCH.md](RESEARCH.md) for the user brief, dated alternatives and tradeoffs;
[VALIDATION.md](VALIDATION.md) for observed check coverage and
[SUPPORT.md](SUPPORT.md) for contribution/security reporting. MIT licensed;
original implementation using the Python standard library, with no competitor code or prose copied.
