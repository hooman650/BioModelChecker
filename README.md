# BioModelChecker
Bio-ModelChecker: Using Bounded Constraint Satisfaction to Seamlessly Integrate Observed Behavior with Prior Knowledge of Biological Networks.

## Abstract 
The in Silico study and reverse engineering of regulatory networks has gained in recognition as an insightful tool for the qualitative study of biological mechanisms that underlie a broad range of  complex illness. In the creation of reliable network models, the integration of prior mechanistic knowledge with experimentally observed behavior is hampered by the disparate nature and  widespread sparsity of such measurements. The former challenges conventional regression-based parameter fitting while the latter leads to large sets of highly variable but equally data compliant network models. 
BioModelChecker (BioMC) proposes a Constraint Satisfaction (CS) based bounded model checking framework for parameter set identification that readily accommodates partial records and the exponential complexity of this problem. BioMC introduces specific criteria to describe the biological plausibility of competing multi-valued regulatory networks that satisfy all the constraints and formulate model identification as a multi-objective optimization problem. Optimization is directed at  maximizing structural parsimony by mitigating control action selectivity while also favoring increased state transition efficiency and robustness of the network’s dynamic response. 

## Getting Started
Please see the ```BioMC-usermanual.pdf``` for a detailed instructions how to install and use BioMC. BioMC already comes with several benchmarks in  ```.json ``` format that could be used to get familiar with the tool.
