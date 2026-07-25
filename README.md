# Quiet Craft — 静かなる技

A bilingual (EN / 日本語) personal portfolio built with Astro 5, Tailwind CSS,
and React islands, designed around Japanese wabi-sabi principles: ma (間),
shibui (渋い), kanso (簡素), and mono no aware (物の哀れ).

## Commands

```sh
pnpm install
pnpm dev        # http://localhost:4321
pnpm build      # static output in dist/
pnpm preview
```

npm works too (`npm install`, `npm run dev`).

## Structure

- `/` — detects language client-side (saved preference, then `navigator.language`) and redirects to `/en/` or `/ja/`
- `/en/`, `/ja/` — full single-page portfolio (Hero → About → Work → Tech → Contact)
- `/en/projects/<slug>/`, `/ja/projects/<slug>/` — markdown case studies from `src/content/projects/`
- The only React island is `LanguageSwitcher.jsx`; everything else is static `.astro`

## Notes

- View transitions use Astro 5's stable `<ClientRouter />` (the old
  `experimental.viewTransitions` flag no longer exists).
- Project thumbnails are placeholder SVGs in `public/projects/` — swap in real
  photography and update the `image` frontmatter in each markdown file.
- Deploys to Vercel with zero config (static output).
