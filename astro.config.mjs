import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';

// Astro 5: view transitions are stable — enabled via <ClientRouter /> in
// BaseLayout.astro, not an experimental flag.
export default defineConfig({
  integrations: [react(), tailwind({ applyBaseStyles: false }), mdx()],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ja'],
    routing: {
      prefixDefaultLocale: true
    }
  }
});
