# aiXiv preparation

| Draft | Metadata | Research log |
| --- | --- | --- |
| Revision of aiXiv:2611.03093 | [Parking-function manifest](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/aixiv.json) | [Parking-function research log](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/process.md) |
| New preorder submission | [Preorder manifest](proofs/athanasiadis-chapoton-conj-4.8-proof/aixiv.json) | [Preorder research log](proofs/athanasiadis-chapoton-conj-4.8-proof/process.md) |

The [proposed v2 changelog](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/changelog-v2.txt) accompanies the revised PDF and source for the existing identifier. The manifests preserve the human byline and declare the AI contribution as `ai-authored`. The preorder draft uses aiXiv’s default CC BY 4.0 license, pending approval. [Publication guide](https://aixiv.online/guide) · [Submission API and CLI documentation](https://aixiv.online/skill.md)

## Abstracts and process notes

The abstract fields use ordinary Unicode prose with short inline TeX in single dollar delimiters. JSON doubles each TeX backslash, so the decoded string contains one, as in the published records. Both draft abstracts round-tripped through the validation endpoint. The first is 605 characters and the second is 603. The process summaries use one plain paragraph each, 222 and 224 characters respectively including the final newline. There are no Markdown delimiters in either paragraph. The reviewed official documentation specifies file limits in the CLI (25 MB for each of the source and PDF). A hard character limit for the process-summary field was not documented. Published summaries in the sample exceed both draft lengths, and both complete paragraphs were included in the validated payloads. [aiXiv:2610.02762 record](https://aixiv.online/api/v1/papers/2610.02762) · [aiXiv:2611.00013 record](https://aixiv.online/api/v1/papers/2611.00013)

## Validation and approval

Use a staging directory with `paper.tex` in its own subdirectory. The CLI otherwise archives neighboring files alongside an explicitly selected TeX source. Copy only the reviewed files and pass `--no-sessions` on every CLI submission operation.

```sh
# From the manuscript's directory
staging_dir=$(mktemp -d)
mkdir "$staging_dir/source"
cp paper.tex "$staging_dir/source/"
cp paper.pdf aixiv.json process.md "$staging_dir/"
npx aixiv@0.5.0 publish "$staging_dir" --source source/paper.tex --dry-run --no-sessions
```

Both server dry-runs returned `ok: true`, `dry_run: true`, and an empty `sessions_would_attach` list. The only multipart files were the standalone `paper.tex` and the reviewed `paper.pdf`. The server validated the supplied PDFs, which were compiled locally.

In CLI 0.5.0 the revision workflow sends a live version request even if `--dry-run` is present. The v2 payload was inspected locally with network transmission blocked. It targets `/api/v1/papers/2611.03093/versions` and contains the revised files, the abstract and other versioned fields, and the changelog. The separate in-place update for the process summary and AI declaration was previewed with `edit 2611.03093 --manifest --dry-run`. After approval, the version request and in-place metadata update are both needed. [Version and metadata-edit documentation](https://aixiv.online/skill.md#edit-a-paper-the-user-owns-edit)

The owner-authenticated trace list for aiXiv:2611.03093 returned zero attachments. If an attachment appears, obtain its ID with `aixiv trace list 2611.03093`. The documented `aixiv trace remove TRACE_ID` operation targets only that attachment and requires separate approval. [Trace management documentation](https://aixiv.online/skill.md#edit-a-paper-the-user-owns-edit)
