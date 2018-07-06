# BioModelChecker
Biological Model Checker (Bio-MC) is a bounded model checker for parameterization of generalized regulatory networks (Thomas Networks) created by Hooman Sedghamiz at [Center for Clinical Systems Biology (CCSB)](https://www.rochesterregional.org/research/clinical-systems-biology/).

Bio-ModelChecker treats the model parametrization problem as a multi-objective optimization inspired from Control Theory and biology. It employs the power of state of the art Constraint Programming in order to efficiently parameterize a regulatory network. 
Bio-ModelChecker is copyrighted 2018 by Center for Clinical Systems Biology. All rights reserved.

Bio-ModelChecker is available for research and evaluation purposes only. It can not be used in a commercial environment, particularly as part of a commercial product, without written permission. Bio-ModelChecker is provided as is, without any warranty.

![BioMC building blocks. BioMC employs state of the art solvers such as Google-OR-Tools and Chuffed for constraint solving, SQlite for solutions management and D3 project for the visulazation](BioMCFlow.png)

## Abstract 
The in Silico study and reverse engineering of regulatory networks has gained in recognition as an insightful tool for the qualitative study of biological mechanisms that underlie a broad range of  complex illness. In the creation of reliable network models, the integration of prior mechanistic knowledge with experimentally observed behavior is hampered by the disparate nature and  widespread sparsity of such measurements. The former challenges conventional regression-based parameter fitting while the latter leads to large sets of highly variable but equally data compliant network models. 
BioModelChecker (BioMC) proposes a Constraint Satisfaction (CS) based bounded model checking framework for parameter set identification that readily accommodates partial records and the exponential complexity of this problem. BioMC introduces specific criteria to describe the biological plausibility of competing multi-valued regulatory networks that satisfy all the constraints and formulate model identification as a multi-objective optimization problem. Optimization is directed at  maximizing structural parsimony by mitigating control action selectivity while also favoring increased state transition efficiency and robustness of the network’s dynamic response. 

## Getting Started
### 1 - Download the BioMC-Installer.exe :
Download the BioMC-Installer.exe from the release tab and the installer would guide you with the next steps

### 2 - Replace 'classpath.txt' and 'jxbrowser':
Please see the ```BioMC-usermanual.pdf``` for a detailed instructions how to replace ```classpath.txt``` and ```jxbrowser```. BioMC already comes with several benchmarks in  ```.json ``` format that could be used to get familiar with the tool.
