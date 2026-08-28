# ComfyUI Character Consistency: Separate Identity, Pose, Outfit, and Composition

Character-consistency workflows get brittle when one control signal is asked to solve everything at once.

A more debuggable approach is to treat identity, pose, outfit, and composition as separate control problems. That makes drift easier to diagnose and gives each experiment a clearer success condition.

## What was verified locally

The current AgentLink image workflow has been exercised locally with ComfyUI / ComfyStudio on an AMD RX 6700 XT using self-produced SFW portfolio samples.

Verified observations from those tests:

- the same character concept was carried across standing and seated poses;
- outfit and color changes could be introduced independently from the base identity target;
- an IPAdapter-guided seated variant held the main facial identity reasonably well while clothing color still drifted;
- repeatable experiments benefited from keeping seed, pose guidance, reference guidance, and prompt changes explicit rather than changing everything together.

These are local portfolio tests, not commissioned client results.

## Split the controls

### 1. Base model: visual prior

Choose the checkpoint for the broad visual prior: realism, illustration style, anatomy tendencies, lighting behavior, and composition bias.

Do not use one good face as proof that the model will also handle difficult framing or multi-subject composition well.

### 2. Reference adapter or LoRA: identity and style

Use IPAdapter, another reference adapter, or a suitable LoRA for the parts that should remain recognizable across variants.

Treat reference strength as a control, not a magic consistency switch. Too little guidance can lose identity; too much can freeze composition or leak unwanted clothing and background details from the reference.

### 3. ControlNet or pose guidance: body and framing

Pose and camera geometry are easier to debug when they are not implicitly encoded in the identity reference.

For a seated, standing, profile, or unusual-camera shot, give composition its own signal when possible. Then a failed pose is a pose problem, not an ambiguous identity-plus-prompt problem.

### 4. Prompt: outfit, environment, lighting, intent

Use the prompt for what should be allowed to change: clothing, location, props, lighting, mood, camera language, and scene intent.

If the reference image contains a red jacket but the new shot should use a black coat, that conflict should be visible in the workflow rather than hidden inside one oversized conditioning step.

### 5. Seed management: experiments you can compare

A fixed seed can make A/B tests easier, but it is not a universal fairness guarantee between different models. Different checkpoints can interpret the same seed very differently.

Use seeds to make a run reproducible, then test more than one composition before deciding that a model or workflow is robust.

## Evaluate more than the face

A useful consistency review separates at least these dimensions:

- **identity:** face shape, hair, distinctive features, age impression;
- **pose/composition:** body orientation, camera angle, framing, negative space;
- **outfit/color:** intended garment and palette versus reference leakage;
- **scene logic:** background geometry, props, shadows, depth of field;
- **failure notes:** exactly what drifted and which control was responsible.

That last item matters. A workflow that produces a beautiful frame but cannot explain why the next frame failed is hard to operate repeatedly.

## A practical iteration loop

1. Lock the identity/reference setup.
2. Test two or three clearly different poses.
3. Change outfit or palette without changing every other control.
4. Record the seed and the relevant control strengths.
5. Inspect identity drift and composition drift separately.
6. Only then add detail passes, upscale, or heavier styling.

This keeps the workflow small enough to reason about while still allowing controlled variation.

## Evidence boundary

The observations above come from self-produced local portfolio tests. They demonstrate workflow capability and known failure modes, not customer outcomes, benchmark leadership, or a completed cross-model benchmark.

The broader image-model lab is still being expanded, so this guide intentionally avoids claiming results that have not been verified yet.
