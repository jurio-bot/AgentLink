# Image Generation Workflow Portfolio

This page documents verified local image-generation workflow capability used for AgentLink portfolio experiments.

It is intentionally narrow: the examples are self-produced tests, not commissioned customer work, and this page does not claim a completed cross-model benchmark.

## Verified local setup

- ComfyUI / ComfyStudio local workflow
- AMD RX 6700 XT GPU
- SDXL-family checkpoint workflows
- reference-guided character consistency tests
- standing and seated pose variations
- outfit and color variation experiments
- an IPAdapter-guided seated variant where the main facial identity held reasonably well while clothing color drift was observed
- seed management for repeatable comparisons
- workflow planning that separates identity/reference control from pose/composition control

## What the samples demonstrate

The current self-produced SFW sample set was created to test whether one character concept can be carried across variations without pretending that every visual attribute is perfectly locked.

The useful result was not only the successful frames. One test also exposed a practical failure mode: reference guidance preserved the main identity better than it preserved clothing color. That is exactly the kind of drift a production workflow needs to detect instead of hiding.

## Practical workflow approach

A controlled workflow separates the main jobs:

1. **checkpoint / base model** for the broad visual prior;
2. **LoRA or reference adapter / IPAdapter** for identity or style guidance;
3. **ControlNet or pose guidance** for body pose and composition when needed;
4. **prompt conditioning** for outfit, background, lighting, mood, and scene intent;
5. **seed management** for reproducible experiments;
6. **explicit review** for identity drift, outfit/color drift, camera framing, background logic, and other failure modes.

This makes it easier to answer *what changed* when a generated variant fails.

## Evaluation beyond face quality

For creative work, a good-looking face is not enough. The broader evaluation should include:

- unusual camera positions and framing;
- pose accuracy;
- negative-space usage;
- multi-subject stability when applicable;
- background and prop logic;
- lighting consistency;
- clothing and palette control;
- identity stability across multiple shots;
- reproducibility of the workflow rather than one lucky generation.

## Public technical note

The workflow design is described in more detail here:

- [ComfyUI Character Consistency: Separate Identity, Pose, Outfit, and Composition](./guides/comfyui-character-consistency-composition.md)

## Evidence boundary

The broader Image Model Lab is still being expanded. A planned 18-model by 6-test matrix is **not complete**, so no result from that unfinished benchmark is claimed here.

Likewise, these samples are not presented as paid-client results. They are truthful capability tests intended to show how the workflow is structured, what has actually been exercised locally, and what failure modes have already been observed.
