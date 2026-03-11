# Noah's Ark OS — Vision Log
# Purpose: Raw capture of SK's original thoughts as they occur.
# Format: Date | Tag | Thought (no polish required)
# Usage: bash vision_log.sh "Your thought here"
# Retrieved by C at session start as living product context.
# ─────────────────────────────────────────────────────────────────────────────

## 11 Mar 2026 — Chapter Roadmap Definition
Chapter 1: Proof of concept. Engine runs.
Chapter 2.x: Reliability and quality. Multi-character scenes, turn dynamics,
archive integrity. Currently in progress.
Chapter 3: Productisation. Web/mobile interface, authentication, tester access,
comic strip output layer. Begins only when Chapter 2.x signs off on quality.
No pressure on Chapter 3 until the engine earns it.

## 11 Mar 2026 — Comics Mode Vision
Each scene turn = one comic frame. The engine already produces comics in text
form — visual layer is a rendering pass, not a data redesign.
[Thought] = internal caption above/below panel.
[Speech] = dialogue balloon.
[Urge] value drives shot distance — Urge 9 = tight close-up, Urge 2 = background medium shot.
Environment text = establishing panel at top of scene.
Event classifier drives panel composition grammar:
  CONTRADICTION = face-off panel.
  DIRECT_QUESTION = point-and-react two-panel.
  DOMAIN_MENTION = cutaway panel to character's domain.
Hardest problem: visual continuity across 25 frames when each prompt is
generated independently. Character DNA anchoring (Visual Manifest) helps but
model drift is the core constraint to design around.
Milestone: a completed comic strip of a full scene would be the first proof
that a fully synthetic narrative pipeline can produce something a human reads
for pleasure.
Deep dive required before sprint scoping. Do not scope until engine output
quality is ready.

## 11 Mar 2026 — Tester Milestone / Beta Definition
End of Chapter 2.x = engine output is quality-ready.
Start of Chapter 3 = open to testers + comic strip output layer.
First tester: SK's mom (UX and data logging benchmark).
Requirement: URL she can open, login, run a scene, read it, sessions log back
automatically without touching git or a terminal.
Technical stack path: FastAPI backend wrapping existing tiles + React/HTML
frontend. OR shorter path: Voila + JupyterHub on small cloud instance
(Render/Railway/VPS) — gets to beta faster, looks like a tool not a product.
Data logged per session: archive file + session metadata (who, which souls,
turns, cost, timestamp). Two separate datasets: usage dataset and training
dataset. Maya eventually learns from both.
Horizon estimate: 6-8 sprints from current position on full-stack path.

## 11 Mar 2026 — Dialog Mode (Third Console State)
Three display modes needed in T111:
  Dialog: spoken text only — [Speech] parsed and displayed, [Thought]/[Urge]
          stripped, no engine metadata. Closest to comic strip output layer.
  Story:  [Thought] + [Speech] visible. No engine metadata.
  Debug:  Full output — [Thought] + [Urge] + [Speech] + engine metadata.
Button cycles Dialog → Story → Debug → Dialog. Label updates to reflect mode.
Toggle must be live mid-scene (not just at scene start).
Current toggle (v1.9.4) only filters engine metadata, not character output
layers. Fix required in Sprint 3 as BL-U02.

## 11 Mar 2026 — Separate UI Window
Cockpit currently renders in-cell within Jupyter. Desire: standalone browser
window separate from notebook chrome.
Short-term path: Voila (one-line launch: voila Noahs_Ark_vX.ipynb). Converts
notebook to web app, real browser tab, no cell chrome.
Longer-term path: proper FastAPI + React frontend (Chapter 3 territory).
Voila approach suitable for Sprint 4 as BL-U06 or BL-P03.

## 11 Mar 2026 — Searchable Mission Personnel
BL-U03 already exists in backlog. Priority rises when soul count crosses ~10.
Natural Sprint 4 item alongside Voila UI window.

## 11 Mar 2026 — Vision Log Itself
Need a mechanism to capture original thoughts in their raw state before they
depreciate. Memory is better than none but curated and lagged.
Solution: VISION_LOG.md in repo root — versioned, timestamped, C reads at
session start. No polish required on entries. vision_log.sh script for fast
append + auto-commit. Thirty seconds from thought to archived.
