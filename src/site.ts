// Single source of truth for anything that needs an absolute URL or appears in
// structured data. Change SITE_URL here when the domain is settled — it feeds
// astro.config.mjs, the sitemap, canonicals, hreflang, and the JSON-LD below.
export const SITE_URL = 'https://uteytithya.dev';

export const PERSON = {
  name: 'Uteytithya Nuon',
  alternateName: '努温 ウテイティチャ',
  jobTitle: 'Backend Developer',
  email: 'uteytithya@gmail.com',
  github: 'https://github.com/Uteytithya',
  locality: 'Phnom Penh',
  country: 'KH',
  school: 'Cambodia Academy of Digital Technology'
} as const;

export const LOCALES = ['en', 'ja'] as const;
export type Locale = (typeof LOCALES)[number];

// og:locale wants the full tag, not the bare language subtag.
export const OG_LOCALE: Record<Locale, string> = {
  en: 'en_US',
  ja: 'ja_JP'
};
