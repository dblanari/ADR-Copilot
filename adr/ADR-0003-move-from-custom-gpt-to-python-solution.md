## Move from custom GPT to Python solution

 ** Status:* Proposed
 ** Date:* 2025-09-18

### Context / Drivers
-* ASSUMPTION: Current custom GPT approach is costly to maintain and limited in flexibility. 
-* ASSUMPTION: Organization prefers solutions that can be version-controlled, deployed, and tested more easily. 
-* ASSUMPTION: Python ecosystem provides richer libraries, better integration with existing systems, and long-term maintainability. 

### Options Considered
1. **Continue with custom GPT** — post-migration minimal risk but ongoing dependency on external service. 
2. **Migrate to Python solution** — reimplement logic in Python for better control. 
3. **Hybrid approach** ― retain GPT for natural language tasks but build orchestration and automation in Python. 

### Decision
We will **adopt a Python-based solution** and migrate away from the custom GPT. 

### Consequences

*) Positive:* 
- Improved maintainability and transparency. 
- Easier integration with CI/CD and monitoring. 
- Lower long-term costs. 
- Ability to reuse open-source Python libraries. 

** Negative: *
- Loss of GPT’s natural language interface and convenience. 
- Initial migration effort required. 
- Potential need to re-implement features currently handled by GPT. 

### References
- *ASSUMPTION:* No formal tickets/PRs yet; discussion was informal. 
