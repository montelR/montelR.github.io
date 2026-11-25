import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
const schema = z.object({ title: z.string(), summary: z.string(), category: z.string(), status: z.string(), order: z.number(), stack: z.array(z.string()).default([]) });
const projects = defineCollection({loader: glob({pattern:'**/*.md',base:'./src/content/projects'}), schema});
const cases = defineCollection({loader: glob({pattern:'**/*.md',base:'./src/content/case-studies'}), schema});
export const collections = { projects, cases };
