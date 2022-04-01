# MARIANNE and the Industrial Agent for I4.0 (Agent4.0)
Source files for the Agent 4.0 and the MARIANNE architecture on Python with PADE.

#  MARIANNE content
*src/MARIANNE/:* sources for PADE (.py), AASX Package Explorer (.aasx), NOVAAS (.json), and TwinCAT (.tnzip) software tools.

# Industrial Agents (IAs) classes instantiation 
*src/MARIANNE/:* (.py) file, and following code lines refers to the IA classes applied (see publications for the concepts):

|       Class I       |           Class II        |       Class III       |
|    -------------    |       -------------       |      -------------    |
|  *Resource Agent*   | *Agent Management System* | *Communication Agent* |
|  Lines  259 to 333  |      Lines  10 to 23      |    Lines  183 to 232  |
|                     |      *Process Agent*      |                       |
|                     |     Lines  237 to 256     |                       |


# Further notes
- For the implementation of MARIANNE use PADE(https://pade.readthedocs.io/) and NOVAAS(https://gitlab.com/gidouninova/novaas).
- Python 3.7+ is recommended for running the python scripts.
- For creating the AASX file, the AASX Package Explorer(https://github.com/admin-shell-io/aasx-package-explorer/releases/tag/v2020-11-16.alpha) is used. 

# Publications
Scientific papers (still in the peer-review process) present MARIANNE as an agent-based architecture for Industry 4.0, focusing on Cyber-Physical Production Systems.

# License
GPL v3.0

# Contact
Luis Alberto Cruz Salazar (luis.cruz@tum.de)

Technical University of Munich

Institute of Automation and Information Systems https://www.mec.ed.tum.de/ais
