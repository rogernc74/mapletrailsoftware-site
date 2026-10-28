# Editorial asset provenance

- `images/editorial/mapletrail-lockup.png`: whitespace crop `(74,142,439,380)` of the repository's authentic optimized `images/mapletrail-logo.png`; original leaf and wordmark pixels retained.
- All app UI: repository screenshots. PR 11's optimized images reused. `images/momentslater/capture.webp`, `timeline.webp`: cropped actual screenshot region `(152,372,588,1317)` after resizing the original correction-commit PNGs to 740×1600; poster-only text/margins removed. `mac-today.webp`: authentic Mac screenshot region, crop `(305,258,975,710)` from the 1280×800 resized original poster.
- `images/editorial/coast.webp`, `memories.webp`, `essentials.webp`: generated using the built-in ImageGen tool with the selected homepage/Moments Later/If Needed concept as style references. Source masters retained in `../generated_images/`. Supporting decorative photographs, no generated product interface or logo.

Prompts: (1) wide editorial Atlantic Canadian rocky coast, warm late afternoon, evergreen headland at right, pale left sky/sea for copy, subdued navy/forest/honey palette, no text/logos/devices/people, no named-location assertion; (2) warm oak/cream linen still life, printed shoreline/flower photos, blank journal, pen and ceramic coffee cup, natural afternoon light, terracotta/forest accents, no devices/UI/logos/text; (3) calm home desk, sage plant, cream ceramic cup, plum notebook, folders and blank notebook, soft morning light, no labels/devices/UI/logos. All generated with exact concept image attached as visual reference.

Exact original Library files remain under `../references/`; they are review evidence and are not shipped as page assets. No font downloads or third-party runtime are required. The page display font is Georgia with serif fallbacks.

- `images/og/*.jpg`: browser-rendered 1200×630 Coastal Editorial sharing cards with real logo/screens, current release wording and decorative generated photos. Source: `scripts/social-card.html.template`; screenshot PNG masters in `../evidence/social-*.png`. JPEG conversion only, no generated or retouched UI.
