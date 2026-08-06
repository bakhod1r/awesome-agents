---
name: threat-model
description: Produce a STRIDE threat model for a system or feature. Use before building anything that handles authentication, money, personal data, file uploads, or third-party input.
---

# Threat Model

Threat modelling is cheap before the build and expensive after. Do it at design time.

## Procedure

1. **Scope.** Name the system, its trust boundaries, and what is explicitly out of scope.
   Out-of-scope items are written down — silence reads as coverage.
2. **Data flow.** Diagram actors, processes, data stores, and every flow that crosses a
   trust boundary. Threats live at the crossings, not inside the boxes.
3. **Enumerate with STRIDE** at each crossing:

   | | Question |
   |---|---|
   | **S**poofing | Can an actor claim another identity? |
   | **T**ampering | Can data be modified in transit or at rest? |
   | **R**epudiation | Can an action be denied because nothing logged it? |
   | **I**nformation disclosure | What leaks, to whom, through which channel? |
   | **D**enial of service | What exhausts under load or deliberate abuse? |
   | **E**levation of privilege | How does a low-privilege actor gain more? |

4. **Rate** by exploitability and impact. Not by gut feel, not by scanner severity.
5. **Mitigate or accept.** Every threat gets a control, or a signed risk acceptance
   with a named owner and an expiry date.
6. **Verify.** Each mitigation names the specific test that proves it works.

## Output

```markdown
# Threat Model: <system>
## Scope and trust boundaries
## Out of scope
## Data flow
## Threats
| ID | Boundary | STRIDE | Threat | Exploitability | Impact | Mitigation | Verified by |
## Accepted risks
| ID | Risk | Owner | Expiry | Rationale |
```

## Worked example

Feature: users upload a profile picture, served from a CDN.

| ID | Boundary | STRIDE | Threat | Mitigation | Verified by |
|---|---|---|---|---|---|
| T1 | Browser→API | T | Content-Type lied about; SVG uploaded as image/png, executes script on view | Re-encode server-side; never trust the declared type; serve from a separate origin | `test_upload_svg_polyglot_is_reencoded` |
| T2 | Browser→API | D | 10 GB upload or a decompression bomb exhausts disk | Size cap before buffering; dimension cap after decode header, before full decode | `test_upload_exceeds_cap_rejected_before_buffer` |
| T3 | API→Storage | E | Filename `../../etc/passwd` escapes the upload directory | Discard the client filename entirely; store under a generated UUID | `test_path_traversal_filename_discarded` |
| T4 | Storage→CDN | I | Object URL is guessable; private avatars enumerable | Random 128-bit object key; deny bucket listing | `test_bucket_listing_denied` |
| T5 | API→Image lib | E | Malformed image triggers a native-code CVE in the decoder | Decode in a sandboxed worker with no network and a memory cap; pin and scan the library | `test_decoder_runs_without_network` |
| T6 | Browser→CDN | S | Attacker replaces another user's avatar via a predictable object key | Ownership check on write; key derived server-side only | `test_cannot_overwrite_other_user_avatar` |

Six threats on a "just an avatar upload" feature. T1 and T5 are the ones that get shipped
without a threat model — and they are the ones that turn into an incident.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "We validate input" as a mitigation | Which validator? Running where? Against which encoding? |
| Threats without a verifying test | An untested mitigation is an assumption wearing a control's uniform |
| Rating by scanner severity | Scanner severity ignores your architecture and your data |
| Modelling only the happy actor | The attacker does not use your UI |
| Model produced once at launch | It is living. New flow, new crossing, new threats. |
| No out-of-scope section | Readers assume you covered what you silently skipped |

## Done when

- [ ] Every trust boundary crossing has been walked through all six STRIDE categories.
- [ ] Every threat ends in a mitigation **or** a dated, owned risk acceptance.
- [ ] Every mitigation names a specific test, not a policy.
- [ ] Out-of-scope is explicit.
- [ ] The model is stored next to the design, not in a slide deck.
