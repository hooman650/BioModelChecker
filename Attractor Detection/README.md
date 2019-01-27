# Exhaustive Attractor detection in Logical Multivalued Regulatory Networks

The class computes the node and cyclic attractors in a multivalued regulatory graph exhaustively.
It simulates the time evolution of the network and forms a so called State Transition Graph (STG) that could be traveresed to detect cyclic and node attractors.
An attractor is a set of state(s) where once the system enters them, stays there indefinitely. 
The attractors are closely related to [Strongly Connected Components (SCC)](https://en.wikipedia.org/wiki/Strongly_connected_component) in a graph but without any outdegrees. In 1972, Tarjan proposed an algorithm that only requires a single depth-first search to compute the SCCs in a graph. The method implemented here is a modified Tarjan's algorithm to detect cyclic and node attractors in a graph.

## Logical Regulatory Graph 

A logical regulatory graph is defined as a directed and weighted graph where each edge denotes an interaction (inhibition or promotion) and its corresponding weight indicates the state above which that action becomes active. These can also be denoted as matrix as shown below;

<img margin-left="auto" margin-right="auto" src="HPA.gif">

## Discrete Approximation

The multivalued networks approximate the continous concentration level of biological entities in a discrete manner and therefore reduce the simulation search space to a discrete space.

<img margin-left="auto" margin-right="auto" src="BinaryStep.pdf">

## Transition Function

The equations below indicate how a typical differential equation that describes the concentration level of an entity can be approximated by discrete values;

<img margin-left="auto" margin-right="auto" src="P6.pdf">

You might ask how this equation might work in practice (the K value defined in the equation above). The image below shows interactively how the image an entity is defined given its regulators (computer science guys call regulators fan-inns). The index of a K value is determined by accounting for active regulators.

<img margin-left="auto" margin-right="auto" src="KValues.gif">

## Time Updates

The STG of a regulatory graph might be simulated by iteratively computing its image. Once the image (tendency) of the network at the next step is computed one has to decide about the order of update (e.g. out of the 4 entities for instance in this network which entity gets updated first or do they get updated simulatnously). The figure below illustrates two special type of time updates called priority with memory (similar to asynchronous) where only a single entity gets updated at a time and synchronous where all the entites can get updated simultanously. The green edges indicate an attractor. Depending on the time update chosen the shape of the STG and **cylic** attractors would be different.

<img margin-left="auto" margin-right="auto" src="Attractors.gif">
