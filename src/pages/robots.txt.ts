import type { APIRoute } from 'astro';
import { SITE_URL } from '../site';

// Generated rather than kept as a static file in public/, because the sitemap
// line has to carry an absolute URL. As a static file that domain was a second
// copy of SITE_URL, and the two would eventually disagree — pointing crawlers
// at a sitemap on a host that no longer exists. Now the domain is set in
// exactly one place: src/site.ts.
export const GET: APIRoute = () =>
  new Response(
    [
      'User-agent: *',
      'Allow: /',
      '',
      `Sitemap: ${new URL('sitemap-index.xml', SITE_URL).href}`,
      ''
    ].join('\n'),
    { headers: { 'Content-Type': 'text/plain; charset=utf-8' } }
  );
