# Third-Party Notices

This inventory records third-party software and materials identified in the
repository and related technical review. It is not necessarily exhaustive,
does not replace the original licence texts, and is not a legal opinion or a
representation that every component is cleared for a particular transaction
or distribution.

Manifest pins and lockfile resolutions describe repository declarations, not
necessarily the packages installed in a live deployment. No production
backend package inventory or Python lockfile was available for this review.
Where a version is not pinned, it is identified as unpinned rather than
inferred from a developer's local environment.

## Backend runtime and Python packages

| Component | Version / status | Licence or terms identified | Commercial use, notices, and unresolved matters |
|---|---|---|---|
| PyMuPDF | `1.28.2`, pinned in backend requirements; direct runtime use | Dual licensed under GNU AGPL-3.0 or Artifex Commercial License. The installed package's `COPYING` contains a short dual-licence statement; the upstream project publishes the licence text. | Commercial operation/distribution requires a rights path appropriate to the use: obtain and verify any required Artifex commercial licence, or evaluate and comply with the applicable AGPL terms. The repository does not evidence an Artifex licence or establish AGPL compliance. Confirm requirements with Artifex and qualified counsel. |
| FastEmbed | `0.8.0`, pinned in `requirements.txt` and `requirements-vercel-fastembed.txt`; active matcher dependency | Apache-2.0 evidence in the upstream `v0.8.0` source tag and in the PyPI wheel and sdist; both published artifacts contain `LICENSE` and `NOTICE`. Their metadata also has the contradictory `License :: Other/Proprietary License` classifier. | Apache-2.0 generally permits commercial use and redistribution subject to its conditions, including licence and applicable notice preservation and modification notices. The 0.8.0 classifier discrepancy remains in those artifacts; retain the licence, notice, and artifact evidence. The deployed package version is unknown. |
| NumPy | Direct dependency; unpinned in backend requirements | NumPy 2.x metadata expresses BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0; exact resolved version is not pinned. | Preserve applicable copyright, licence, and component notices on redistribution. Because the version is unpinned, establish the resolved production version and its corresponding notices before preparing a final notice bundle. |
| FastAPI | `0.141.1`, pinned; direct runtime | MIT | Commercial use is generally permitted subject to retaining copyright and permission notices in distributed copies or substantial portions. |
| Uvicorn | `0.53.0`, pinned; direct runtime server | BSD-3-Clause | Commercial use is generally permitted subject to retaining copyright, conditions, and disclaimer in source or binary redistribution. |
| Pydantic | `2.13.5`, pinned; direct runtime | MIT | Commercial use is generally permitted subject to retaining copyright and permission notices in distributed copies or substantial portions. |
| python-multipart | `0.0.32`, pinned; direct runtime upload dependency | Apache-2.0 | Commercial use is generally permitted subject to Apache-2.0 conditions, including licence and applicable notice preservation and modification notices. |
| pytest | `9.1.1`, pinned in the requirements files; test-only by application use | MIT | Development/testing dependency. Preserve notices if the package or its copies are redistributed; its presence in a requirements file does not establish that it is part of production runtime. |
| Starlette | Version not pinned directly; FastAPI transitive dependency | BSD-3-Clause in the locally inspected package metadata | Preserve applicable BSD notice and disclaimer if redistributed. The resolved production version is unknown. |
| ONNX Runtime | Version not pinned directly; FastEmbed transitive dependency | MIT; its installed distribution includes `LICENSE` and `ThirdPartyNotices.txt`. | Preserve the licence and third-party notices when redistributing the runtime. The production version and platform-specific package are unknown. |
| Hugging Face Hub and `hf-xet` | Versions not pinned directly; FastEmbed/Hugging Face dependencies | Apache-2.0 in locally inspected package metadata | Apache notice conditions apply on redistribution. Production versions are unknown. |
| Tokenizers | Version not pinned directly; FastEmbed transitive dependency | Apache-2.0 upstream; locally installed metadata showed an Apache classifier but no licence file | Include the upstream licence text and applicable notices if redistributed. Confirm the production artifact/version and include its actual licence materials. |
| Requests | Version not pinned directly; FastEmbed transitive dependency | Apache-2.0 in locally inspected metadata; its installed distribution includes `LICENSE` and `NOTICE` | Preserve applicable licence and notice materials on redistribution. Production version is unknown. |
| Pillow | Version not pinned directly; FastEmbed transitive dependency | MIT-CMU in locally inspected metadata | Preserve the applicable copyright and licence notice on redistribution. Production version is unknown. |
| `certifi` | Version not pinned directly; transitive dependency | MPL-2.0 in locally inspected metadata | If distributed, preserve notices and assess applicable source/covered-file obligations, particularly for modified covered files. Production inclusion/version is unknown. |
| `tqdm` | Version not pinned directly; transitive dependency | MPL-2.0 AND MIT in locally inspected metadata | Preserve applicable notices and evaluate the MPL terms for any modified covered files distributed. Production version is unknown. |
| `py-rust-stemmers` | Version not pinned directly; FastEmbed transitive dependency | Local package contained a `LICENSE`, but package metadata did not declare a licence in the inspected environment | Inspect the exact production artifact and its licence text; the version and production resolution are unknown. |
| Other Python transitives | Versions vary by resolver and platform; no Python lockfile | Locally inspected metadata includes MIT, BSD, Apache-2.0, PSF-2.0, MPL-2.0, and combined expressions | This list is not a complete production SBOM. Resolve and inventory the actual deployed dependency tree and retain each distributed package's notices. |

The backend manifests are not interchangeable. `requirements.txt` and
`requirements-vercel-fastembed.txt` include FastEmbed; other manifests select
Sentence Transformers and PyTorch instead. The live Vercel backend's selected
manifest and installed package versions have not been verified.

## Frontend runtime and build dependencies

| Component | Version / status | Licence or terms identified | Commercial use, notices, and unresolved matters |
|---|---|---|---|
| React | `19.3.0` in `package-lock.json`; also identified in the inspected live frontend bundle | MIT | Commercial use is generally permitted subject to preserving the copyright and permission notice in redistributed copies or substantial portions. |
| React DOM | `19.3.0` in `package-lock.json`; production dependency | MIT | Preserve the applicable copyright and permission notice on redistribution. |
| Scheduler | `0.28.0` in `package-lock.json`; React DOM transitive dependency | MIT | Preserve the applicable copyright and permission notice if redistributed. |
| Vercel Analytics (`@vercel/analytics`) | `2.0.1` in `package-lock.json`; also identified in the inspected live frontend bundle | MIT | Preserve applicable MIT notice on redistribution. The service and account remain subject to Vercel terms and are not transferred by this notice. |
| Vite | `8.3.6` in `package-lock.json`; build tooling | MIT | Build/development dependency, not a direct production dependency. Preserve notices if Vite itself is redistributed. |
| `@vitejs/plugin-react` | `6.1.1` in `package-lock.json`; build tooling | MIT in lockfile metadata | Preserve notices if redistributed. Its presence does not establish that it is included in the deployed browser output. |
| ESLint and associated plugins/types | Versions resolved in `package-lock.json`; development/lint tooling | Lockfile identifies MIT for direct packages; transitive packages include MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, BlueOak-1.0.0, and MPL-2.0 | Development/build dependencies. Preserve notices if distributed. The actual production bundle's inclusion of their code is not established by the lockfile. |
| `lightningcss` and platform packages | `1.33.0` in `package-lock.json`; build dependency | MPL-2.0 | If redistributed, include the applicable notices and consider MPL source obligations for modified covered files. Whether any package files are shipped is unknown. |
| `caniuse-lite` | `1.0.30001810` in `package-lock.json`; build-time data dependency | CC-BY-4.0 in lockfile metadata | If the data is redistributed, attribution is required under the applicable licence. Presence in the build tree does not establish inclusion in final browser assets. |
| Other frontend transitive packages | 169 package entries in the lockfile overall; production closure is four packages, remaining packages are development/build closure | Lockfile records MIT, Apache-2.0, BSD, ISC, MPL-2.0, BlueOak-1.0.0, and CC-BY-4.0 package metadata | Lockfile metadata is not a complete notice bundle. Confirm actual artifact contents and retain applicable notices for packages or code redistributed in source/build output. |

The lockfile is the repository's exact npm resolution. It does not by itself
prove that a particular live deployment used that lockfile or that every
development/build package is present in the deployed output. The inspected
frontend JavaScript bundle did contain React 19.3.0 and Vercel Analytics
2.0.1.

## Model files

| Component | Version / status | Licence or terms identified | Commercial use, notices, and unresolved matters |
|---|---|---|---|
| `all-MiniLM-L6-v2` ONNX model and tokenizer files | Five bundled files in `backend/models/all-MiniLM-L6-v2/`; hashes match the corresponding files in `Qdrant/all-MiniLM-L6-v2-onnx` on Hugging Face | The Qdrant ONNX model card and the original `sentence-transformers/all-MiniLM-L6-v2` model card declare Apache-2.0. | Apache-2.0 generally permits commercial use and redistribution subject to its conditions. Preserve the licence and applicable attribution/notice information. No model-specific `LICENSE` or `NOTICE` is bundled in this repository or listed in the inspected upstream file tree. The Kompa commit does not pin the upstream revision. |
| Base model `nreimers/MiniLM-L6-H384-uncased` | Identified in the Sentence Transformers model card | Its model card declares MIT. | This is distinct from the ONNX package's Apache-2.0 declaration. The full rights chain and any additional conditions should be assessed independently. |
| Training datasets identified in the model card | Multiple datasets; see the upstream model card | Dataset-specific terms are not assessed here. | A model licence declaration does not by itself establish the rights or terms for training datasets. Separate dataset review remains open. |

## Images, template materials, fonts, and sample PDFs

| Component | Version / status | Licence or terms identified | Commercial use, notices, and unresolved matters |
|---|---|---|---|
| React/Vite starter assets (`react.svg`, `vite.svg`) | Tracked frontend assets; not referenced by current application source | `react.svg` matches the Vite React starter asset; the Vite project is MIT-licensed upstream. | Preserve applicable template notices if the assets or related template material are redistributed. Brand and trademark permissions are separate and are not established here. |
| `favicon.svg` and `hero.png` | Tracked assets; source/creator not established | No reliable project provenance or licence notice identified | Ownership, source, permission, and any third-party content are unresolved. Do not treat repository presence as proof of ownership. |
| `icons.svg` | Tracked SVG sprite containing social/service marks | Origin and licence/attribution not established; includes recognizable third-party brand symbols | Rights to the artwork and trademark use are unresolved. Public availability alone does not establish permission. |
| Nimbus Sans embedded in sample PDFs | PDF-embedded font subsets; exact source build not identified | URW Base 35 licence identifies AGPL-3.0 with a special exception allowing font programs to be embedded in PostScript/PDF documents irrespective of the document licence. | Retain the applicable font licence/exception evidence. This does not clear rights in the PDF text, marks, or other content. |
| Liberation Serif embedded in a sample PDF | PDF-embedded subset | Liberation Fonts declare SIL Open Font License 1.1; the licence distinguishes font software from documents created with the fonts. | Preserve font-software notices if distributing the font software. PDF content rights are separate. |
| Noto Serif embedded in a sample PDF | PDF-embedded subset | SIL Open Font License 1.1; the licence distinguishes font software from documents created with the fonts. | Preserve font-software notices if distributing the font software. PDF content rights are separate. |
| Sample PDFs in `sample-data/` | Nine tracked PDF fixtures; some are used by tests/evaluation; two commercial-offer examples have no code/test reference found | No content licence or source/creator permission identified | Redistribution rights in text, names, contact details, logos/graphics, and other content remain unknown. Generic or test-like content is not proof of being synthetic. |

## Notice and provenance handling

For any proposed source, binary, container, or other distribution, identify
which components are actually included and retain the original licence and
notice files required by their terms. Apache-2.0, MIT, BSD, MPL, CC-BY, and
other licences have different conditions; this inventory does not replace
those texts or determine how they apply to a specific distribution.

The proprietary `LICENSE` applies only to original materials that the
relevant rights holder owns or is authorized to license. It does not override
third-party licences. A buyer's ability to operate the application depends
on the applicable third-party licences, separate permissions, and external
service terms. PyMuPDF licensing, the model's upstream/base-model and dataset
rights, asset provenance, PDF content clearance, and production dependency
versions remain matters for confirmation.

## Selected upstream references

These references support the component and terms summaries above. The
corresponding original licence files and terms govern; links do not replace
including required notices in a distribution.

* [PyMuPDF 1.28.2 COPYING](https://github.com/pymupdf/PyMuPDF/blob/1.28.2/COPYING)
* [FastEmbed v0.8.0 source](https://github.com/qdrant/fastembed/tree/v0.8.0),
  [PyPI 0.8.0 release artifacts and metadata](https://pypi.org/project/fastembed/0.8.0/)
* [NumPy 2.5.4 licence](https://github.com/numpy/numpy/blob/v2.5.4/LICENSE.txt)
* [FastAPI 0.141.1 licence](https://github.com/fastapi/fastapi/blob/0.141.1/LICENSE)
* [Uvicorn 0.53.0 source](https://github.com/encode/uvicorn/tree/0.53.0)
* [Pydantic 2.13.5 source](https://github.com/pydantic/pydantic/tree/v2.13.5)
* [python-multipart 0.0.32 source](https://github.com/Kludex/python-multipart/tree/0.0.32)
* [React 19.3.0 licence](https://github.com/facebook/react/blob/v19.3.0/LICENSE)
* [Vite 8.3.6 source](https://github.com/vitejs/vite/tree/v8.3.6)
* [Tokenizers 0.23.3 licence](https://github.com/huggingface/tokenizers/blob/v0.23.3/LICENSE)
* [ONNX Runtime 1.31.0 licence](https://github.com/microsoft/onnxruntime/blob/v1.31.0/LICENSE)
* [Sentence Transformers model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
  and [Qdrant ONNX model card](https://huggingface.co/Qdrant/all-MiniLM-L6-v2-onnx)
* [URW Base 35 licence](https://github.com/ArtifexSoftware/urw-base35-fonts/blob/master/LICENSE),
  [Liberation Fonts licence](https://github.com/liberationfonts/liberation-fonts/blob/main/LICENSE),
  and [Noto Fonts licence](https://github.com/notofonts/latin-greek-cyrillic/blob/main/OFL.txt)
