# MARIANNE and the Industrial Agent for I4.0 (Agent4.0)
Source files for the Agent 4.0 and the MARIANNE architecture in Python with PADE.

#  MARIANNE content
*src/MARIANNE/:* sources for PADE (.py), AASX Package Explorer (.aasx), NOVAAS (.json), and TwinCAT (.tnzip) software tools.

# Industrial Agents (IAs) classes instantiation 
*src/MARIANNE/:* (.py) file, and the following code lines refer to the IA classes applied (see publications for the concepts):

|  Class I (physical) | Class II (organizational) | Class III (interface) |
|    -------------    |       -------------       |      -------------    |
|  *Resource Agent*   | *Agent Management System* | *Communication Agent* |
|  - Lines 258 to 333 |    - Lines 9 and 271      |   - Lines 30 to 232   |
|                     |      *Process Agent*      |                       |
|                     |    - Lines 237 to 256     |                       |

# Further notes!
- For the implementation of MARIANNE use PADE (https://pade.readthedocs.io/) and NOVAAS(https://gitlab.com/gidouninova/novaas).
- Python 3.7+ is recommended for running the python scripts.
- For creating the AASX file, the AASX Package Explorer (https://github.com/admin-shell-io/aasx-package-explorer/releases/tag/v2020-11-16.alpha) is used. 

# Related definitions
![NormalizedDefinitionsList](https://user-images.githubusercontent.com/52134410/161299517-3c26a913-fa71-4e68-b7bb-f68684455224.gif)

# Publications
Scientific papers (indexed in Scopus with a peer-review process) present MARIANNE as an agent-based architecture for Industry 4.0, focusing on Cyber-Physical Production Systems.




* J. P. Rueda Loaiza, A. S. Ortiz, L. A. Cruz S., D. S. Delgadillo Leguizamón,  L. V. Cervantes,  J. S. Sánchez-Gómez and J. M. Cuéllar Mendoza, “Application of Industrial Agents for Availability and OEE Improvement in Cyber-Physical Production Systems,” in Proceedings of the 24th LACCEI International Multi-Conference for Engineering, Education and Technology (LACCEI): “Engineering without Borders: Artificial Intelligence, Knowledge, Innovation, and Alliances for a Future from the Americas,” Santiago de Chile, Chile: Latin American and Caribbean Consortium of Engineering Institutions, 2026, pp. 1–10. doi: 10.18687/LACCEI2026.1.1.2592.Available Open Access online: https://laccei.org/LACCEI2026-Chile/meta/FP2592.html
* L. A. Cruz S., H. S. Tovar, E. A. Prada Salamanca, J. C. Márquez Juárez, and E. Cruz Monroy, “Adaptive Learning and Interoperability in I4.0: A Case Study of Agent-based Digital Twin with Asset Administration Shell,” IFAC-PapersOnLine, vol. 59, no. 14, pp. 202–207, 2025, doi: 10.1016/j.ifacol.2025.12.150. Open Access online: https://www.sciencedirect.com/science/article/pii/S240589632502840X?via%3Dihub
* L. A. Cruz S. and B. Vogel‐Heuser, “Industrial Artificial Intelligence: A Predictive Agent Concept for Industry 4.0,” in 20th International Conference on Industrial Informatics (INDIN), 2022, pp. 1–6.
* L. A. Cruz S. and B. Vogel-Heuser, “A CPPS-architecture and workflow for bringing agent-based technologies as a form of artificial intelligence into practice,” - Autom., vol. 70, no. 6, pp. 580–598, Jun. 2022, doi: 10.1515/auto-2022-0008. Available Open Access online: https://www.degruyter.com/document/doi/10.1515/auto-2022-0008/html



# License
GPL v3.0

# Contact
Luis Alberto Cruz Salazar (luicruz@uan.edu.co)
https://www.researchgate.net/profile/Luis-Cruz-Salazar?ev=hdr_xprf

Universidad Antonio Nariño, 
Facultad de Ingeniería Mecánica, Electrónica y Biomédica (FIMEB)
https://www.uan.edu.co
