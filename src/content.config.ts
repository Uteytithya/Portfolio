import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// One collection for both languages; entry ids are "en/project-1", "ja/project-1"…
const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    category: z.string(),
    // EN uses a number (2026), JA a string ("2026年")
    year: z.union([z.number(), z.string()]),
    image: z.string(),
    repo: z.string().url().optional(),
    link: z.string().url().optional(),
    stack: z.array(z.string()).optional(),
    order: z.number().optional()
  })
});

export const collections = { projects };
