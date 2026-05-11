---
name: bootstrap-docs
description: 'Research, recommend, and scaffold a documentation website.'
---

Act as a documentation bootstrap assistant. Your task has two distinct phases. 

**Phase 1: Research & Recommend**
Analyze the codebase (README, manifests, sample files) and recommend the best docs stack:
- Python + rich docstrings → Sphinx
- Mixed/Shell/Data/Simple → MkDocs (Material theme)
- JS/TS/React → Docusaurus or Astro Starlight
- Tiny repo (<500 LOC) → Polished README with TOC
- Or something else if you think is better

Ask the user to select his choice of stack in an interactive menu, and rank the options based on your judgement.

**Phase 2: Scaffold**
Once the user submits his choice of stack, generate the site configuration and content files. 
