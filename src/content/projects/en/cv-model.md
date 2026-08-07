---
title: "InternLink — CV Model"
category: "ML Developer"
year: 2025
image: "/projects/cvmodel-thumb.svg"
repo: "https://github.com/InternLink-TheNextStep/CVModel"
stack: ["Python", "FastAPI", "LayoutLM", "PyMuPDF", "Docker", "Nginx"]
order: 1
---
An AI system that reads a CV the way a human reviewer does — layout and all. An ensemble of LayoutLM document-understanding models classifies candidates into five developer and data roles, straight from multi-page PDF resumes.

## The brief

InternLink matches candidates to positions, and the slowest step was the first one: someone reading every CV. The goal was a service that could look at a resume — not just its text, but its structure — and predict where the candidate fits.

## The approach

As the ML developer on the project, I owned the model layer end to end. Two LayoutLM variants work as an ensemble: v1 for spatial layout understanding and v3 for efficiency, weighted 40% each, with keyword-based scoring covering the final 20%. I trained them on 4,817 resumes across five categories — backend, frontend, fullstack, data analyst, and data scientist. PyMuPDF handles multi-page extraction, with visual marker detection picking out details like addresses, and divider detection separating experience from education.

## The result

I shipped it as a production-ready FastAPI service, containerized with Docker and fronted by Nginx — REST endpoints for CV analysis with confidence scores across every prediction, plus health monitoring and full architecture documentation.
