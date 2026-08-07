import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { SITE_URL } from './src/site.ts';

// Astro 5: view transitions are stable — enabled via <ClientRouter /> in
// BaseLayout.astro, not an experimental flag.
export default defineConfig({
  site: SITE_URL,
  integrations: [
    react(),
    tailwind({ applyBaseStyles: false }),
    mdx(),
    sitemap({
      i18n: { defaultLocale: 'en', locales: { en: 'en', ja: 'ja' } },
      // `/` is a client-side redirect shim, 404 is not a real page, and
      // /font-lab is a throwaway type specimen (delete both when the display
      // face is settled).
      filter: (page) => {
        const path = new URL(page).pathname;
        return (
          path !== '/' &&
          !path.startsWith('/404') &&
          !path.startsWith('/font-lab')
        );
      }
    })
  ],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ja'],
    routing: {
      prefixDefaultLocale: true
    }
  }
});
