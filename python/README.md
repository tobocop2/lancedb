# LanceDB Python SDK

A Python library for [LanceDB](https://github.com/lancedb/lancedb).

## Installation

```bash
pip install lancedb
```

### Building from source for pre-Haswell x86_64 hosts

Published wheels target `x86-64-haswell` (AVX2 + FMA + F16C). Pre-Haswell hosts (Intel Sandy Bridge / Ivy Bridge / Westmere, AMD Bulldozer / Piledriver / Steamroller) need a from-source build with the baseline lowered:

```bash
RUSTFLAGS="-C target-cpu=x86-64-v2" maturin build --release
pip install ./target/wheels/lancedb-*.whl
```

Runtime SIMD dispatch in the embedded lance crate selects the appropriate tier (scalar / AVX / AVX+FMA / AVX2+FMA / AVX-512) at load time. See lance's [CONTRIBUTING.md](https://github.com/lancedb/lance/blob/main/CONTRIBUTING.md) for the full guide; from Python, `lance.simd_info()` reports which tier was selected.

### Preview Releases

Stable releases are created about every 2 weeks. For the latest features and bug fixes, you can install the preview release. These releases receive the same level of testing as stable releases, but are not guaranteed to be available for more than 6 months after they are released. Once your application is stable, we recommend switching to stable releases.


```bash
pip install --pre --extra-index-url https://pypi.fury.io/lancedb/ lancedb
```

## Usage

### Basic Example

```python
import lancedb
db = lancedb.connect('<PATH_TO_LANCEDB_DATASET>')
table = db.open_table('my_table')
results = table.search([0.1, 0.3]).limit(20).to_list()
print(results)
```

### Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for information on how to contribute to LanceDB.
