---
title: "Fake COVID News Detection"
category: "ML Developer"
year: 2025
image: "/projects/fakenews-thumb.svg"
repo: "https://github.com/Uteytithya/fake_covid_news_detection"
order: 3
---
A machine learning classifier that separates real COVID-19 reporting from misinformation — built as a transparent, reproducible pipeline from raw text to verdict.

## The brief

During the pandemic, false information moved faster than corrections. The project asks a narrow, useful question: given a piece of COVID-19 news, can a model tell whether it's genuine?

## The approach

The pipeline is deliberately legible. A cleaning notebook takes the public COVID fake-news dataset from raw to ready, documenting every transformation — both the uncleaned and cleaned data ship with the repository. TF-IDF vectorization turns each article into features, and a trained classifier renders the judgment. The full methodology is written up in an accompanying report and presentation.

## The result

A working detector and, just as importantly, an honest record of how it was built — every preprocessing choice visible in the notebooks, the vectorizer preserved alongside the model, and findings documented for anyone who wants to retrace the path.
