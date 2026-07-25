// React island: EN | 日本語 toggle. Swaps the locale prefix on the current
// path and remembers the choice for the root-page redirect.
export default function LanguageSwitcher({ locale, path }) {
  const swap = (target) => {
    const next = path.replace(/^\/(en|ja)(?=\/|$)/, `/${target}`);
    return next === path && !path.startsWith(`/${target}`) ? `/${target}/` : next;
  };

  const remember = (lang) => {
    try {
      localStorage.setItem('lang', lang);
    } catch {
      /* private mode — the link still navigates */
    }
  };

  const linkStyle = (active, ja) => ({
    fontFamily: ja ? "'Zen Kaku Gothic New', sans-serif" : "'Inter', sans-serif",
    fontSize: '13px',
    fontWeight: 500,
    letterSpacing: '0.04em',
    color: active ? '#223A5E' : '#6B6560',
    borderBottom: active ? '1px solid #223A5E' : '1px solid transparent',
    paddingBottom: '1px',
    textDecoration: 'none',
    transition: 'color 300ms ease'
  });

  return (
    <nav
      aria-label="Language"
      style={{ display: 'flex', alignItems: 'center', gap: '10px' }}
    >
      <a
        href={swap('en')}
        onClick={() => remember('en')}
        aria-current={locale === 'en' ? 'true' : undefined}
        style={linkStyle(locale === 'en', false)}
      >
        EN
      </a>
      <span
        aria-hidden="true"
        style={{ width: '1px', height: '12px', background: 'rgba(0,0,0,0.12)' }}
      />
      <a
        href={swap('ja')}
        onClick={() => remember('ja')}
        aria-current={locale === 'ja' ? 'true' : undefined}
        style={linkStyle(locale === 'ja', true)}
      >
        日本語
      </a>
    </nav>
  );
}
