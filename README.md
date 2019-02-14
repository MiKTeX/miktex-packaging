## MiKTeX Packaging

Tools for maintaining the MiKTeX package repository.

### Prerequisites

You need:

- a CTAN mirror
- the TeX catalogue entry sources
- a package staging directory (can be empty)
- a working MiKTeX installation

### Configuring

Create a build directory and run `cmake` as follows:

```
export PATH=/path/to/miktex-bin-dir:$PATH
cmake \
  -DMIKTEX_CTAN_MIRROR=/path/to/ctan-mirror \
  -DMIKTEX_TEX_CATALOGUE=/path/to/tex-catalogue/entries \
  -DMIKTEX_PACKAGE_STAGING_ROOT=/path/to/miktex-package-staging-root \
  ../source
```

Replace `../source` with the path to this directory.
