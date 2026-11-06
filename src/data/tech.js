/**
 * Readout copy for the Tools & Craft panel.
 *
 * Each line describes what the tool DOES in a stack — not a claim about how
 * long it has been used or how well. Those claims belong in Experience and the
 * case studies, where they can be checked. A hover panel is the wrong place to
 * assert seniority, so it does not.
 *
 * Where a tool is actually used is not written here at all: TechStack.astro
 * derives it from the project frontmatter and the Experience entries, so the
 * panel cannot drift out of step with the rest of the page.
 */
export const techRoles = {
  PHP: {
    en: 'The language under Laravel — request handling, business rules, and everything a server does between a click and a response.',
    ja: 'Laravel を支える言語。リクエスト処理からビジネスロジックまで、サーバー側の処理を担う。'
  },
  TypeScript: {
    en: 'JavaScript with the shapes declared, so a mismatched payload fails at build time instead of in front of a user.',
    ja: '型のある JavaScript。形の不一致を実行時ではなくビルド時に落とす。'
  },
  Python: {
    en: 'The working language of the ML side — data preparation, model training, and the services that put a model behind an endpoint.',
    ja: '機械学習側の主言語。データ前処理、学習、そしてモデルを API の背後に置くまで。'
  },
  Dart: {
    en: 'The language Flutter runs on; one codebase compiled ahead of time to native on both phones.',
    ja: 'Flutter の言語。単一のコードから両プラットフォームのネイティブへ事前コンパイルされる。'
  },
  'C++': {
    en: 'Close to the metal — embedded control loops and device communication where a garbage collector is not welcome.',
    ja: 'ハードウェアに近い層。GC を置けない組込みの制御ループと機器間通信に。'
  },
  Java: {
    en: 'The classroom language for data structures and object modelling, and still what much of the enterprise world runs on.',
    ja: 'データ構造とオブジェクト設計の基礎を学んだ言語。今も業務システムの多くを動かしている。'
  },
  Laravel: {
    en: 'The backend frame most of this work is built in — routing, Eloquent, queues, auth, and migrations that keep schema changes reversible.',
    ja: 'バックエンドの土台。ルーティング、Eloquent、キュー、認証、そして巻き戻せるマイグレーション。'
  },
  Nuxt: {
    en: 'Vue with the server side attached — file-based routing and rendering on the server so the first paint is not a spinner.',
    ja: 'サーバーサイドを備えた Vue。ファイルベースのルーティングと SSR で、初回表示をスピナーにしない。'
  },
  Flutter: {
    en: 'One widget tree drawn to its own canvas, so an app looks and behaves the same on both platforms without a second codebase.',
    ja: '独自のキャンバスに描画する単一のウィジェットツリー。二重実装なしに両 OS で同じ挙動を得る。'
  },
  Express: {
    en: 'The thin Node server — middleware, a few routes, and nothing in the way when a service only needs to be a service.',
    ja: '薄い Node サーバー。ミドルウェアと最小限のルートだけで、余計なものを挟まない。'
  },
  Svelte: {
    en: 'A compiler rather than a runtime: the framework disappears at build time and ships as plain DOM updates.',
    ja: 'ランタイムではなくコンパイラ。ビルド時にフレームワークは消え、素の DOM 更新だけが残る。'
  },
  PostgreSQL: {
    en: 'The relational default — real constraints, transactions, JSON when the shape is genuinely loose, and a planner worth trusting.',
    ja: 'リレーショナルの既定解。制約とトランザクション、必要なら JSON、そして信頼できるプランナ。'
  },
  MySQL: {
    en: 'The database behind most Laravel deployments; familiar operational ground and a hosting story that exists everywhere.',
    ja: 'Laravel 運用の定番。扱い慣れた運用基盤で、どこにでもホスティング先がある。'
  },
  Redis: {
    en: 'Memory used deliberately — caching, sessions, rate limits, and queues, for work that must be fast and may be lost.',
    ja: '意図して使うメモリ。キャッシュ、セッション、レート制限、キュー。速さが要り、失っても良い処理に。'
  },
  Firebase: {
    en: 'Realtime sync, auth, and hosting without a server to run — the shortest path from a mobile client to shared live state.',
    ja: 'サーバーを持たずに済むリアルタイム同期・認証・ホスティング。モバイルから共有状態への最短経路。'
  },
  'Google Cloud': {
    en: 'Managed infrastructure when a project should not own hardware — compute, storage, and the services around a deployed model.',
    ja: 'ハードウェアを持たない選択。コンピュート、ストレージ、デプロイ済みモデル周辺のサービス群。'
  },
  Git: {
    en: 'The record of how something came to be. Branches for work in progress, and a history worth reading afterwards.',
    ja: '成り立ちの記録。進行中の作業はブランチに、履歴は後から読める形で残す。'
  },
  Docker: {
    en: 'The same environment on a laptop and in production — dependencies pinned in the image rather than in a setup document.',
    ja: '手元と本番で同一の環境。依存関係は手順書ではなくイメージに固定する。'
  },
  AWS: {
    en: 'Where services go to be reachable — compute, object storage, and networking, sized to what the thing actually needs.',
    ja: 'サービスを公開する場所。必要な規模に合わせたコンピュート、オブジェクトストレージ、ネットワーク。'
  }
};

/**
 * Stack strings in the content and Experience tags do not always match the
 * label shown in the grid. Only genuine aliases belong here — this must not
 * become a way to claim a tool was used somewhere it was not.
 */
export const techAliases = {
  Firebase: ['Realtime DB'],
  'C++': ['Embedded']
};
