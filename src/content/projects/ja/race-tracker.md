---
title: "レーストラッカー"
category: "Flutterモバイル開発"
year: "2025年"
image: "/projects/race-thumb.svg"
repo: "https://github.com/Uteytithya/race_tracker"
stack: ["Flutter", "Dart", "Firebase", "Realtime DB"]
order: 4
---
レースの「いま」を追いかける Flutter 製クロスプラットフォームアプリ。タイムも順位も、Firebase を通じてすべての端末にその瞬間に届きます。

## 課題

レース当日は混沌としています。コースの各地点に散らばる計時係、順位を知りたい観客、あとで記録を突き合わせる運営。アプリの仕事は、全員が見ている「ひとつの現在」をつくることでした。

## アプローチ

Flutter を選び、ひとつの Dart コードベースから iOS・Android・ウェブ・デスクトップへ画面を届けました。同期は Firebase Realtime Database の役目。ゴール地点で記録されたタイムは、着地した瞬間に他のすべての場所へ現れます。計測のロジックと表示を分けて設計したので、新しいレース形式もUIに触れずに加えられます。

## 結果

ひとつのコードベース、8つのプラットフォーム。観客の手の中のどの端末にも、同じレースが同じ瞬間に映ります。
