---
title: "Schedulify 管理システム"
category: "バックエンド開発"
year: "2025年"
image: "/projects/schedulify-thumb.svg"
repo: "https://github.com/Uteytithya/SchedulifyAdmin"
order: 2
---
スケジュール管理プラットフォーム Schedulify の管理バックエンド。予定表も、ユーザーも、権限も、静かに整えつづける Laravel アプリケーションです。

## 課題

スケジュールは、共有された瞬間に難しくなります。重なる予約、変わりつづける空き状況、そのすべてを見渡して正す管理者。Schedulify には、それらの操作を確実に支えるバックエンドが必要でした。

## アプローチ

Laravel の MVC 構成を、意図的にきれいに保ちました。スケジュール操作のための REST エンドポイント、管理画面を守る JWT 認証、そしてマイグレーションで履歴まで読める MySQL のスキーマ。管理ビューは Blade と Tailwind CSS で描き、重要な経路は PHPUnit が守ります。

## 結果

120コミットの着実な積み重ねが、保守しやすい管理バックエンドになりました。関心の分離は明快に、セットアップはマイグレーションから再現可能に。他のクライアントが迷わず積み上げられる API です。
