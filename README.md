# MARIANNE and the Industrial Agent for I4.0 (Agent4.0)
Source files for the Agent 4.0 and the MARIANNE architecture on Python with PADE.

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
Scientific papers (still in the peer-review process) present MARIANNE as an agent-based architecture for Industry 4.0, focusing on Cyber-Physical Production Systems.

* L. A. Cruz S. and B. Vogel‐Heuser, “Industrial Artificial Intelligence: A Predictive Agent Concept for Industry 4.0,” in 20th International Conference on Industrial Informatics (INDIN), 2022, pp. 1–6.
* L. A. Cruz S. and B. Vogel-Heuser, “A CPPS-architecture and workflow for bringing agent-based technologies as a form of artificial intelligence into practice,” - Autom., vol. 70, no. 6, pp. 580–598, Jun. 2022, doi: 10.1515/auto-2022-0008. Available Open Acces online: https://www.degruyter.com/document/doi/10.1515/auto-2022-0008/html



# License
GPL v3.0

# Contact
Luis Alberto Cruz Salazar (luis.cruz@tum.de)

Technical University of Munich

Institute of Automation and Information Systems https://www.mec.ed.tum.de/ais
