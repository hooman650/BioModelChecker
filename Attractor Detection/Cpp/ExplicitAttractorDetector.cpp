/* 
Modified Tarjan algorithm for identification of attractors in a regulatory network defined by:
1. ADJ : Adjacency list : First Row 'Source' ; Second Row 'Target'; Third Row 'Threshold of action' (should be signed)
2. D: Delay , false : Synchronous, true : Asynchronous
3. L: Max transcription Level
4. N: Number of entities
Copy right Hooman Sedghamiz July, 2018
Email: Hooman.sedghamiz@gmail.com
*/

#include "stdafx.h"
#include <vector>
#include <iostream>
#include <list>
#include <cmath>
#include <stack>
#include "inttypes.h"
#include <algorithm>    // std::min
#define NIL -1          // Unknown

using namespace std;

// The Directed Graph on the GO
class Graph
{
	short V;                                   // No. of vertices
	short Attr_N;                              // No. of Attractors
	int temp_ind;                              // temporary index for conversion 
	bool Root_f;                               // root flag
	bool D;                                    // Delay false: Synch; true: Asynch
	int index;                                 // Index (counter)
	int SS;                                    // Size of State space
	list<int> *adj_ind;                        // Holds the index of incoming edges
	list<int> *adj_Th;                         // Holds the threshold of incoming edges
	list<int> *STG;                            // Holds the State Transition Graph on the GO!
	vector<int> *BinaryM;                      // Binary Mask
	vector<int> *Tr_index;                     // Holds STG of the model (to see which nodes are visited)
	vector<int> *Tr_lowlink;                   // Lowlink Vec
	vector<bool> *Tr_onStack;                  // On stack 
	vector<bool> *out_v;                       // Output vector of thresholds
	vector<int> *Image;                        // holds the state of the network
	vector<int> *state;                        // holds the state of the network
	vector<int> *N;                            // Max Transcription Levels for the network
	vector<vector<int> > *K;                   // In-balanced 2D vector for K values
	short MaxIn;                               // Initialize with 0 indegs
// Methods
public:
	Graph(int V, vector<int> L, vector< vector<int> > k, bool D, vector< vector<int> > ADJ);                 // Constructor
	void addEdge(int v, int w, int Th);                   // This adds the indegs and the threshold of action
	void DFS();                                           // prints all vertices in DFS manner	
	void pushIndeg(vector< vector<int> > &ADJ);           // Computes the indeg for each node
	void Max_indeg();                                     // Computes max indegree in the network
	void LexToState(int temp);                            // Converts a lex index to its state  
	void StateToLex();                                    // void state to Lex
	void StrongConnect(int LexI,stack<int> &stack);       // Identify SCC
	void ComputeImage();                                  // Computes the image given the current state
	void Th_f(int &V_ind);                                // Computes if a node is ON or OFF
	void Delay_f(int &LexI);                              // Computes the next state based on the delay
};

// Define Constructor
Graph::Graph(int V, vector<int> L, vector< vector<int> > k, bool D, vector< vector<int> > ADJ)
{
	this->Attr_N = 0;                             // Nr. of Attractors
	this->V = V;                                  // Nr. of nodes in the regulatory graph
	this->D = D;                                  // delay : 0: Synch ; 1: Asynch
	this->MaxIn = 0;                              // Max Indegree of the network
	this->SS = 1;                                 // Size of the STG
	this->Root_f = false;                         // Flag for identification of the attractors
	this->index = 0;                              // Reset the index counter
	adj_ind = new list<int>[V];                   // Initialize the in-deg list  
	adj_Th  = new list<int>[V];                   // Initialize the Threshold list
	BinaryM = new vector<int>;                    // Initialize the BinaryMask    
	Tr_index = new vector<int>;                   // Tr_index
	Tr_lowlink = new vector<int>;                 // Tr_lowlink
	Tr_onStack = new vector<bool>;                // Onstack?
	out_v = new vector<bool>;                     // Outdeg
	Image   = new vector<int>;                    // Initialize the state of the net 
	state = new vector<int>;                      // Initialize the state of the net   
	N = new vector<int>;                          // Initialize the max levels of the net
	K = new vector<vector<int> >(V);
	for (int i = 0; i < V; i++) {
		this-> Image->push_back(0);               // Initialize the state to be zero
		this-> state->push_back(0);               // Initialize the state to be zero
		this-> N->push_back(L[i]);                // Push the Max Levels
		this-> SS *= L[i];                        // Cartesian Product of the STG 
		(*K)[i].resize(k[i].size());
		for (int j = 0; j < k[i].size(); j++) {
			(*K)[i][j] = k[i][j];
		}
	}
	STG = new list<int>[SS];                      // Initialize the STG 
	for (int i = 0; i < SS; i++) {
		this->Tr_index->push_back(NIL);
		this->Tr_lowlink->push_back(NIL);
		this->Tr_onStack->push_back(false);
	}
	pushIndeg(ADJ);                              // Push indegrees and Threshold of actions for each node
	Max_indeg();                                 // Compute the max indeg of the net and create the BinaryMask
	for (int i = 0; i < MaxIn; i++)
		this->out_v->push_back(false);
}

// Converts a lexicographical index to its corresponding vector representation
void Graph::LexToState(int temp) {
	int Pr;
	for (int j = 0; j < V - 1; j++) {
		// Compute the Product 
		Pr = 1;
		for (int k = j + 1; k < V; k++) {
			Pr *= ((*N)[k]);
		}
		(*state)[j] = (temp) / Pr;
		(temp) %=  Pr;
	 }
	(*state)[V - 1] = temp;
}

void Graph::StateToLex() {
	// get the lexicographial index of the next state
	int Pr;
	temp_ind = 0;
	for (int j = 0; j < V - 1; j++) {
			Pr = 1;
			for (int k = j + 1; k < V; k++) {
				Pr *= ((*N)[k]);
			}
			temp_ind += (*state)[j] * Pr;
		}
	temp_ind += (*state)[V - 1];
}

/*
Computes the indeg for each node
ADJ[0][:]  Targets
ADJ[1][:]  Sources
ADJ[2][:]  Threshold of actions (this is signed)
*/
void Graph::pushIndeg(vector< vector<int> > &ADJ)
{
	for (int j = 0; j < ADJ[0].size(); j++) {
		addEdge(ADJ[0][j] - 1, ADJ[1][j] - 1, ADJ[2][j]);
	}
}

// Generate a list of Incoming Actions for each Node (Index and Thresholds)
void Graph::addEdge(int v, int w, int Th)
{
	adj_ind[v].push_back(w); // Add w to v’s list.
	adj_Th[v].push_back(Th); // Add w to v’s list.
}

// Compute Max_Ind of the network and initialize a Binary Mask
void Graph::Max_indeg()
{
	int temp_s;
	for (int i = 0; i < V; i++) {
		temp_s = adj_ind[i].size();
			if (temp_s > MaxIn)
				MaxIn = temp_s;
	}
	// Initialize the Binary Mask
	for (int i = 0; i < MaxIn; i++) 
		BinaryM -> push_back(int(pow(2.0, double(i))));
}

// prints all vertices in DFS manner
void Graph::DFS()
{
	// Mark all the vertices as not visited
	stack<int> stack;
	for (int i = 0; i < SS; i++)
		if ((*Tr_index)[i] == NIL) {
			StrongConnect(i,stack);
			Root_f = false;
		}

}

// Identify the SCC (This is a recursive function)
void Graph::StrongConnect(int LexI, stack<int> &stack)
{
	// Visit the node
	(*Tr_index)[LexI] = (*Tr_lowlink)[LexI] = ++index;
	stack.push(LexI);
	(*Tr_onStack)[LexI] = true;
	// Reset the state vector to LexI
	LexToState(LexI);
	// compute the image
	ComputeImage();
	// compute the next state
	Delay_f(LexI);

	for (auto i = STG[LexI].begin(); i != STG[LexI].end(); ++i) {
	////////////////// Conversion Done! //////////////////////////////////////////
		int temp = *i;
		// if not visited recurse on it
		if ((*Tr_index)[temp] == NIL) {
			StrongConnect(temp, stack);
			(*Tr_lowlink)[LexI] = min((*Tr_lowlink)[temp], (*Tr_lowlink)[LexI]);
		}
		else if ((*Tr_onStack)[temp] == true) {
			(*Tr_lowlink)[LexI] = min((*Tr_lowlink)[LexI], (*Tr_index)[temp]);
		}
		else
			Root_f = true;
	}

	// Print Attractors
	if (((*Tr_lowlink)[LexI] == (*Tr_index)[LexI]) && (!Root_f)) {
		cout << "<---------------------------------------------------->" << endl;
		cout << "SS " << ++Attr_N <<"= ";
		//Root_f = true;
		int temp_pop;
		do {
			temp_pop = stack.top();
			stack.pop();
			(*Tr_onStack)[temp_pop] = false;
			cout << temp_pop << " ";
		} while (temp_pop != LexI);
		cout << endl;
	}
}

// Computes the image of the current state //
void Graph::ComputeImage() {
	int k_ind;
	for (int i = 0; i < V; i++) {
		Th_f(i);                                           // Thresholding function for node 'i'
		k_ind = 0;
		for (int j = 0; j < MaxIn; j++)                        // Index of the K value
			k_ind += (*out_v)[j] * (*BinaryM)[j];
		(*Image)[i] = (*K)[i][k_ind];
	 }
}

// Thresholding function //
void Graph::Th_f(int &V_ind) {
	for (int i = 0; i < MaxIn; i++) {
		(*out_v)[i] = false;
	}
	int counter = 0;
	for (auto i = adj_ind[V_ind].begin(), j = adj_Th[V_ind].begin(); i != adj_ind[V_ind].end(); ++i, ++j) {
		if (*j > 0) {
			if (((*state)[*i]) >= abs(*j))
				(*out_v)[counter] = true;
			else
				(*out_v)[counter] = false;
		}
		else {
			if (((*state)[*i]) < abs(*j))
				(*out_v)[counter] = true;
			else
				(*out_v)[counter] = false;
		}
	    counter++;
	 } 
}

// Delay function computes next state given current state and image //
void Graph::Delay_f(int &LexI) {
	if (!D) {
		// Synchronous //
		for (int i = 0; i < V; i++) {
			if ((*Image)[i] > (*state)[i])
				(*state)[i]++;
			else if ((*Image)[i] < (*state)[i])
				(*state)[i]--;
		}
		StateToLex();                             // Get the index
		STG[LexI].push_back(temp_ind);            // Push the outdegree
	}
	else {
		// Asynchronous //
		for (int i = 0; i < V; i++) {
			if ((*Image)[i] > (*state)[i]) {
				(*state)[i]++;                    // increase the bit
				StateToLex();                     // Get the index
				STG[LexI].push_back(temp_ind);    // Push the outdegree
				(*state)[i]--;                    // decrease the bit (brings it to the original)
			}
			else if ((*Image)[i] < (*state)[i]) {
			    (*state)[i]--;
				StateToLex();                     // Get the index
				STG[LexI].push_back(temp_ind);    // Push the outdegree
				(*state)[i]++;                    // increase the bit (brings it to the original)
			}
		}
	}
}

// Driver program to test methods of graph class
int main()
{
	// test case : Nr of Nodes, Max-Levels, K vector, delay, adjacency matrix //
	Graph g(4, { 2,2,3,3 }, {{ 0,1 },{ 0,1,1,1 },{ 0,2 },{ 0,1,2,2 }}, false, {{1,2,2,3,4,4},{3,1,4,2,3,4}, {-1,1,-1,1,2,2}});
	g.DFS();
	cout << "===========================================================" << endl;
	system("pause");
	return 0;
}

