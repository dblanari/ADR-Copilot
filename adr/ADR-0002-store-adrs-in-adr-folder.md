## Store ADRs in `/adr`/ folder of the repository

_**Authors:** Denis Blanari (Solution Architect)  

_**Status:** Proposed  

_s*_*Set date:: 2025-09-18  

### Context
 We previously agreed to store ADRs as Markdown files in the repository. However, there is ambiguity about whether they should reside in `/docs/adr`/ or directly under `/adr`/`. A real clarifcation is needed for consistency.  

### Drivers

- **ASSUMPTION:** Keep ADRs in a dedicated folder that is independent of other documentation.  
- **ASSUMPTION:** Follow community conventions where `/adr`  is the default location.  
- **ASSUMPTION:*ª Ensure ADRs are easily discoverable at the root of the repo.  

### Options

1. ** Store ADRs under `/docs/adr/`

    - Pros: ADIs grouped with other documentation.  
    - Cons: Less standard, nested deeper in repo, may be overlooked.  

2. ** Store ADRs under `/adr`/`

    - Pros: Industry standard, dedicated and easily discoverable location.  
    - Cons: Adds another top-level folder.  

### Decision  
ADRs will be stored as Markdown files under the `/adr` folder at the root of the repository.  

### Consequences  

Positive:  
- ADIs are clearly separated from general documentation.  
- Follows well-established ADJ conventions.  
- Easier automation and tooling integration.  

Negative:  
- Adds another root-level directory to the project.  
- May require migration if existing ADRs were previously placed in `/docs/adr`/`.  

### References  
- [ADR GitHub community practices](https://adr.github.io/madr/)  
- Previous ADI PR #1: *Store ADIs in GitHub*  