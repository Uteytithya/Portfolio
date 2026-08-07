# 縁の下 — Beneath the Floor

A bilingual (EN / 日本語) personal portfolio built with Astro 5, Tailwind CSS,
and React islands, designed around Japanese wabi-sabi principles: ma (間),
shibui (渋い), kanso (簡素), and mono no aware (物の哀れ).

The title comes from 縁の下の力持ち — the one whose essential work goes unseen,
which is the job description for a backend developer.

## Commands

```sh
pnpm install
pnpm dev        # http://localhost:4321
pnpm build      # static output in dist/
pnpm preview
```

npm works too (`npm install`, `npm run dev`).

Two generated assets are committed rather than built on every deploy. Both need
Python with `fonttools` and `brotli` (`pip install fonttools brotli`):

```sh
npm run fonts   # re-subset the self-hosted webfonts (reads dist/, writes public/fonts/)
npm run og      # re-render the social card into public/og.png
```

**Re-run `npm run fonts` after introducing a new kanji**, then rebuild. The
fonts in `public/fonts/` are subsets containing only the characters the site
actually renders — full Latin, full kana, and just the kanji in use. A kanji
that is not in the subset falls back to a system font and looks wrong. Latin and
kana are covered in full, so ordinary copy edits need nothing. Because the
script reads `dist/`, run `npm run build` first.

Serving these two CJK families from Google Fonts meant 1.35 MB across 118
requests, since the English page alone renders ~55 Japanese characters and each
one pulls a different unicode-range slice. The subsets are 5 files, ~270 KB, and
no third-party connection.

## Structure

- `/` — detects language client-side (saved preference, then `navigator.language`) and redirects to `/en/` or `/ja/`
- `/en/`, `/ja/` — full single-page portfolio (Hero → About → Work → Experience → Tech → Contact)
- `/en/colophon/`, `/ja/colophon/` — how the site is built (type, palette, stack)
- `404.astro` — bilingual, lives outside the locale tree and links to both homes
- `/en/projects/<slug>/`, `/ja/projects/<slug>/` — markdown case studies from `src/content/projects/`
- The only React island is `LanguageSwitcher.jsx`; everything else is static `.astro`

## Notes

- View transitions use Astro 5's stable `<ClientRouter />` (the old
  `experimental.viewTransitions` flag no longer exists).
- Type is Zen Old Mincho (display) and Zen Kaku Gothic New (body), both SIL OFL
  and self-hosted from `public/fonts/` with their licences alongside. Two
  families cover both languages: each draws its Latin next to its kana.
- Project thumbnails are placeholder SVGs in `public/projects/` — swap in real
  photography and update the `image` frontmatter in each markdown file.
- Deploys to Vercel with zero config (static output).
