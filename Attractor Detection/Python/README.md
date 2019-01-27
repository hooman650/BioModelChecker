## Functions
- comp_S(): compute the image of any given states using sync/async update scheme
- state_transition_graph(): enumerate full state transition graph
- viz(): visualize state transition graph
- config_k(): configure k parameters in linear time given expected state
  transition graph, and obtain an range of valid values for each K
  parameters
- verify_got_stg_range(): verify the ranges of K parameters correctly
  produce the expected state transition graph

## Format of Cycle Input File *.cycle
- Every corresponding line corresponds to a mapping. In the case of
  sync, it is a one-to-one mapping. While in the case of async, it is a
  one-to-many mapping.
- Example: '0000'>'0001','0010'

### Authors
- The implementation is done by Hooman Sedghamiz and Wenxiang Chen
