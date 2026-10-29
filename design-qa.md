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

## October 28 company identity correction
Roger supplied the current MapleTrail Software Inc. Facebook page/logo. Replaced the former logo with that exact 1254px source artwork and corrected full company-name references throughout the 19 pages, metadata, support/legal text and image alt text. The legal-body validator permits only that exact identity replacement and its sentence-ending punctuation normalization; all other existing policy/support wording remains protected.

Current rendered evidence: `../evidence/new-logo-desktop.png` (1200px-wide desktop capture), `new-logo-320.png` (confirmed 320×720), `new-logo-layout.json` (scrollWidth=320; real logo loaded at512px, box108×70), and `new-brand-social-overview.jpg`. Browser viewport updates applied asynchronously; only the later measured320px capture is narrow verification. CSS/layout unchanged. Original new-logo JPEG is retained under images/brand with Facebook photo provenance in ASSET-SOURCES.md.

Independent review caught a P2 sharing-card capture issue: 1280×720 canvas and two unloaded logo slots. Recaptured after every image completed and normalized to the exact1200×630 card region. All seven resulting JPEGs were independently inspected: correct dimensions, complete logo, no extra canvas. Per-card image-loading readback: `../evidence/new-brand-social-loads.json`. Static validator now enforces the actual sharing-image dimensions. All19 pages,494 references,94 image tags and12 policies/support bodies pass. Independent reviewer returned no remaining P0/P1/P2 findings. No publication.

## Homepage caption and product-content correction
User reported that the caption's visible backing shape looked poor and substantive product copy had been lost, especially Roger's reason for creating Moments Later. Removed the supporting-line background and the mobile floating panel. The coastal photo has a uniform cream wash for text contrast; no local caption/card shape remains. Browser computed backgrounds for both the copy container and supporting paragraph are transparent.

Reintroduced38 original substantive product sections,251 headings/prose/list units from corrected2ea8c6a, through editable `content/product-details.json`. The complete founder story, attribution and six audience items now appear immediately after the Moments Later hero, linked by “Why I built Moments Later.” Other recovered material includes Apple Watch capture, journal context, Mac/shared Premium, Habit Wallet Health/privacy/limits, travel export/Premium details, If Needed's planning details, and both Acadie languages' cultural/Acadie+/press information. Current corporate identity and release facts remain intact. Obsolete Apple-first positioning is excluded.

Evidence inspected: `../evidence/hero-caption-comparison.jpg` puts equal-width1200×630 before/after hero crops together; final desktop screenshots `hero-without-box-desktop.png` and `founder-story-desktop.png` were captured at actual1200×900. `founder-story-320.png` and `restored-content-layout.json` use actual320×720. All seven main routes have scrollWidth320 and no overflowing main elements. The story link navigates to #why and exposes the complete original paragraphs. No browser errors/warnings. Final sizing override reset.

Independent source review verified the story exactly against2ea8c6a after whitespace normalization, original substantive heading/paragraph/list content retained across pages, no duplicate IDs or broken references, and no P0/P1/P2 findings. Static checks now enforce every recovered content unit in rendered pages. Generator idempotence and diff whitespace check pass. Local review only.


## Current Acadie features and native captures — October 28, 2026
Added a prominent bilingual Living Acadie section immediately after each hero: Daily Trivia, Acadie Code, Word Search, Community boards, creators, Web Radio and optional Acadie+ extras. Updated the homepage summary and Acadie hero/metadata. General iOS/Android availability is retained; Games are explicitly scoped to iPhone/iPad because the current public Google description does not independently verify Android games parity. Account and online-preparation requirements match public Apple copy. Existing heritage, family, story, press, legal and founder-story content remains intact.

Roger explicitly excluded ButterKit artwork. All eight new image outputs use original native app captures, with source hashes/transforms in `content/acadie-feature-assets.json`; no composed store export is used. Games/Creators source hashes match the capture provenance manifest. Community images are native public board-list details, cropped to exclude older navigation; they make no claim about current message counts. No native app build, simulator, account, catalog or release operation was performed.

Visual QA used native Firefox because the in-app browser binding returned `browser.user is unavailable` through both supported access methods. Actual rendered screenshots were inspected, not HTTP status: EN/fr desktop at the normal 1512px CSS-wide window (3024px screenshot density2), and Firefox Responsive Design Mode with visible320×800 controls. The new cards stack at320px, images preserve proportions and text stays within the viewport. No visible horizontal clipping. This narrow pass is visual evidence, not an instrumented DOM overflow measurement. EN Games and FR Community/Creators anchor clicks reached the matching sections. Tab after the Creators jump focused the image link with a visible outline. The FR→EN language link reached /acadie/. Responsive Mode was closed at completion. Unrelated tabs were preserved; a dedicated local preview tab remains open.

Evidence: `../evidence/acadie-current-en-desktop.png`, `acadie-current-fr-desktop.png`, `acadie-current-en-320.png`, `acadie-current-fr-320-community.png`, `acadie-current-fr-320-creators-focus.png`, `acadie-current-homepage-feature.png`, and `acadie-current-final.png`. The final capture shows all three native screens and their explanatory copy. Coastal paper/navy typography and quiet spacing remain consistent with the selected direction. Community's older lower-resolution native detail is less sharp than the current Games/Creators captures; its provenance is explicit.

Independent read-only source review verified all8 original hashes/transforms and bilingual parity, and caught a P2 platform-scope ambiguity in the homepage and metadata. Fixed by explicitly qualifying Games on iPhone/iPad in both locales and the homepage; reviewer confirmed no remaining P0/P1/P2 findings. Static checker passes19 pages,511 local references,100 images,12 preserved legal/support bodies,38 restored product sections and251 original content units. Generator idempotence and diff whitespace checks pass. Local preview only; no publication.


## Radio thumbnail and older screenshots correction — October 28, 2026
Roger identified missing Radio imagery and outdated Names/Explore screens, then rejected the initial Radio image's size. Radio now has a compact native player thumbnail: maximum320px tall/170px wide desktop and300px tall/150px wide mobile. Clicking it opens the image for detail. Radio explanation, player image and following Acadie+ copy appear in that order on mobile. The new Web Radio jump is present. Native newer Names and localized1.6 Explore/Stories replace all inherited older screenshot references in both Acadie pages; the homepage also uses refreshed Explore. Both Names captions explicitly identify the available English UI capture. No unpublished genealogy directory, ButterKit composition, app source edit or native device operation.

Visual verification: dedicated native Chrome QA window, after Firefox interaction was interrupted by Roger's concurrent navigation. Existing user tabs and article were preserved. EN desktop Names screenshot and serif body copy inspected; compact EN Radio inspected. French Radio thumbnail and following content inspected with Chrome Responsive controls confirmed at320×800; no visible horizontal clipping. This is visual evidence, not a new DOM overflow measurement. The first native stepper set produced a1px width: discarded as evidence, then width was typed and read back as320. Responsive emulation and DevTools were closed afterward. Main IAB binding was unavailable from the prior check.

Evidence: `../evidence/acadie-names-refreshed-desktop.png`, `acadie-radio-compact-desktop.png`, `acadie-radio-compact-fr-320.png`; candidate sheets preserve the inspected source choices. Final normal-width French Radio evidence shows the compact image beside its explanation and Acadie+ beneath the row. The320px capture confirms the final mobile order/size.

Independent source review verified all8 new source hashes/transformations and excluded private/test fixture content. It caught a P2 typography issue: adding a Names caption changed the last paragraph selector. Fixed the selector to exclude eyebrow/caption paragraphs, preserving19px Georgia story text (18px mobile). Source recheck and final-commit disposition are recorded in the compact receipt. All19 pages,517 local references,102 image tags,12 legal/support bodies,38 sections and251 preserved content units pass. Generator idempotence and whitespace checks pass. No publication.
