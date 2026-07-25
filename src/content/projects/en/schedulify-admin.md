---
title: "Schedulify Admin"
category: "Backend Developer"
year: 2025
image: "/projects/schedulify-thumb.svg"
repo: "https://github.com/Uteytithya/SchedulifyAdmin"
order: 2
---
The administrative backend for Schedulify, a scheduling management platform — a Laravel application that keeps timetables, users, and permissions in quiet order.

## The brief

Scheduling looks simple until people share it: overlapping bookings, shifting availability, and administrators who need to see and correct all of it. Schedulify needed a backend that made those operations dependable.

## The approach

A standard Laravel MVC architecture, kept deliberately clean — REST endpoints for scheduling operations, JWT-based authentication guarding the admin surface, and MySQL behind versioned migrations so the schema's history is as readable as its present. Blade templates with Tailwind CSS render the admin views; PHPUnit covers the critical paths.

## The result

A hundred and twenty commits of steady iteration into a maintainable admin backend — clear separation of concerns, reproducible setup from migrations, and an API another client can build on without asking questions.
