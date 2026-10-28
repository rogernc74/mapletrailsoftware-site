# Coastal Editorial design QA

final result: passed

Scope is the selected visual direction with authentic branding/screens and verified information, rather than literal reproduction of the mockups' invented logos, interfaces or copy. All six selected images were opened before implementation. Final rendered captures and reference crops were placed together in comparison inputs and inspected.

## Source and implementation evidence

Source truth: `../references/coastal-home.png`, `acadie.png`, `momentslater.png`, `habitwallet.png`, `momentsaway.png`, `ifneeded.png` (six Library IDs in the delegated brief). Original boards: 1024×1536 pixels. Desktop page frames were cropped from those boards, excluding outer concept labels and separate mobile device mockups where practical. The homepage source includes an overlapping mobile mockup; that is a reference presentation, not a required desktop webpage control.

Implementation: `http://127.0.0.1:8876/`; final desktop captures `../evidence/home-desktop.png`, `acadie-desktop.png`, `momentslater-desktop.png`, `habitwallet-desktop.png`, `momentsaway-desktop.png`, `ifneeded-desktop.png`, `acadie-fr-CA-desktop.png`. CSS viewport 1440×1000, screenshot density 1; full-page captures are 1440px wide. Mobile captures use 390×844, density 1, full-page width 390px. Narrow DOM checks use 320×720. These are design boards without a known CSS viewport, so comparison panels normalize source/implementation to equal 660px widths rather than claiming pixel-identical viewport geometry.

Full comparison evidence: `../evidence/{home,acadie,momentslater,habitwallet,momentsaway,ifneeded}-comparison.jpg`. Focused header/hero comparisons use the same names ending `-hero-comparison.jpg`; these make the typography, authentic logo, hero crop and action hierarchy readable. Mobile overview: `../evidence/mobile-overview.jpg`. Final capture pass scrolled each page before capture to load all deferred screenshots: `final-assets.json` records zero unloaded images in all 14 desktop/mobile cases.

State: default page, menu closed, EN except the separately captured fr-CA route. Keyboard-expanded navigation at 320px: `menu-keyboard-320.png`. Language interaction results: `language-tests.json`. Complete narrow layout results: `320px-final.json`.

## Findings and fixes

No remaining actionable P0/P1/P2 findings.

Final sharing-asset check also replaced PR 11’s baked-in Apple-first homepage wording and incomplete Moments Later platform wording. Seven 1200×630 sharing cards were rendered in the browser using real logo/app imagery; screenshot masters `../evidence/social-*.png`, each image loaded successfully.

1. P2, first desktop pass: app hero headline scale forced an extra Acadie line and dominated the hero. Reduced the desktop app title scale; final Acadie comparison shows the two-line hierarchy.
2. P2, first asset pass: Moments Later's archived PNGs contained poster margins. Cropped the actual app view from those authentic original images, preserving UI pixels; desktop Mac view likewise trimmed. Final Moments Later comparison shows readable real screens, without generated app UI.
3. P2, first mobile pass: hiding a line break joined French heading words. Added actual whitespace, reduced mobile app titles and moved longer introduction below the hero image on narrow screens. Final fr-CA mobile capture shows natural word spacing and a shorter first view.
4. P2, 320px pass: long support email addresses enlarged contact items even though the marketing container clipped page overflow. Added wrapping/min-width rules and removed clipping from document pages. Final 19-route pass checks element bounds as well as scroll width: zero overflowing elements, including support cards.
5. P2, independent review: the shared legal-page language toggle pointed at homepages. Preserved privacy/terms/account-deletion suffixes. Browser clicks tested EN→FR→EN for all three pairs.
6. P2, independent review: an assembled serif brand lockup did not preserve the existing wordmark. Replaced it with a whitespace-trimmed crop of the entire original logo, including its wordmark pixels. Final captures use that asset in both header and footer.
7. Evidence correction: initial full-page captures had not yet loaded some far-below-fold images. Scrolled and recaptured all desktop/mobile pages; `final-assets.json` verifies every image loaded. This was capture timing, not an asset failure.

The independent source reviewer confirmed both review findings resolved and returned no remaining P0/P1/P2 findings. Source digest reviewed: `81c2501919b8d8a794f234a12d2e2734c97016282819d59b0cb62b16b0bbe86c` on the implementation diff based at `2ea8c6a`. Final-commit source verification is in the delivery receipt.

## Five fidelity surfaces

- Typography: Georgia provides the editorial serif display and story text; system sans handles navigation, metadata and action labels. Large title/quiet eyebrow hierarchy and relaxed line height retain the reference direction. Real logo type is raster-preserved, not reset in a substitute font. Mobile wrapping inspected in EN/fr-CA.
- Rhythm/layout: full-width coastal homepage hero; prominent Acadie feature; four-app collection; alternating image/story rows; closing action and coherent footer. Cream gutters, fine rules and restrained corners carry through all pages. App hero layouts adapt around actual portrait screenshots; generated tablet mockups are not recreated. About/company context and product details remain available.
- Palette/tokens: warm cream/paper, forest text, terracotta homepage and memories, navy Acadie, green/yellow Habit Wallet, blue travel accents, plum If Needed. Focus rings are visible; long addresses wrap. Dark photographic footer keeps text legible. No gradient or code-drawn decorative asset is used.
- Images: original MapleTrail logo and existing app screenshots replace all invented brand/UI imagery. Three new supporting photos share the source's coastal or warm desk mood, exported as optimized WebP. Photos are decorative, not asserted named locations. No fleur-de-lis. Screenshot aspect ratios and original UI pixels are preserved. The dark real app UI intentionally differs from the mockups' fictional light UI.
- Copy: Acadie remains released on iOS/Android. Moments Later remains released on iPhone/iPad/Mac/Watch with shared Premium. Existing store URLs are retained. If Needed has no verified public store link; product/support actions avoid an available/coming-soon claim. Both Acadie languages and all 12 existing support/legal bodies are preserved. The unverified mockup location claim and search control were omitted.

## Interaction/check evidence

- 19 HTML pages; 494 local href/src references; 94 image tags; all resolve, have alt attributes and dimensions.
- All 12 legal/support main-text bodies exactly match the PR 11 baseline.
- One h1 and main per page; titles/descriptions present. Canonicals, sitemap, robots, PR 11 optimized images and Acadie metadata language alternates retained.
- All seven marketing routes captured at desktop and mobile widths; no broken images. All 19 routes passed 320px scroll-width AND element-bound checks.
- Keyboard: first Tab exposes skip link with a solid outline; Tab/Enter opens Apps; Tab/Enter follows Acadie. Expanded menu fits 320px.
- Acadie EN/FR homepage switching and all three legal document pairs verified with browser clicks.
- Browser error/warning log check: empty. No app credential or account UI accessed.
- No package/build/lint manifest exists in this static HTML repository. Supported checks are Python static validation, generator idempotence, and `git diff --check`; no framework build was invented.

## Accepted deviations and P3 follow-up

These are a direction-based redesign with authentic content, not screenshot clones. Original logos/app UI, more detailed platform/capability copy, supported legal links, a company About section, direct store actions, and accessible native navigation intentionally differ from illustrative placeholders. Responsive section ordering adapts to long bilingual copy. Decorative imagery is reused across related sections; additional authentic lifestyle photography can be considered in a later content pass. No blocking design question remains.
