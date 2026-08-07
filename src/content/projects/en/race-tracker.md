---
title: "Race Tracker"
category: "Flutter Mobile Developer"
year: 2025
image: "/projects/race-thumb.svg"
repo: "https://github.com/Uteytithya/race_tracker"
stack: ["Flutter", "Dart", "Firebase", "Realtime DB"]
order: 4
---
A cross-platform Flutter app for tracking races as they happen — times, positions, and progress synced live across every device through Firebase.

## The brief

Race day is chaos: timekeepers at different points on the course, spectators wanting live positions, organizers reconciling it all afterward. The app's job is to make one shared, always-current picture of the race.

## The approach

I built it in Flutter so a single Dart codebase carries the interface to iOS, Android, web, and desktop, and leaned on Firebase Realtime Database for the synchronizing — a time recorded at the finish line appears everywhere else the moment it lands. I kept tracking logic separate from presentation, so new race formats slot in without touching the UI.

## The result

One codebase, eight platform targets, and a race that every phone in the crowd sees the same way at the same moment.
