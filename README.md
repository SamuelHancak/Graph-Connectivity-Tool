# Graph Connectivity Tool

This project provides a tool to analyze and connect graph components from a given input file. The tool reads graph data, identifies connected components, and connects these components by finding the nearest points between them. The results are written to an output file.

## Features

- **Graph Initialization**: Reads graph data from a file and initializes the graph structure.
- **Connected Components Detection**: Identifies all connected components in the graph.
- **Component Connection**: Connects the identified components by finding the nearest points between them using a KDTree.
- **Output**: Writes the added edges to an output file.

## Requirements

- Python 3.x
- `numpy`
- `scipy`

## Installation

Install the required packages using pip:

```sh
pip install numpy scipy
```

## Usage

1. **Prepare the Input File**: Ensure you have a graph data file in the `test_data` directory. The file should contain edges in the format:

   ```
   [x1,y1] [x2,y2]
   ```

2. **Run the Script**: Execute the script with the input file specified in the `FILE_NAME` variable.

```sh
python main.py
```

3. **Output**: The script will generate an output file in the `output_data` directory with the added edges.

```sh
python main.py
```

## Example

Given an input file `test_data/graph_60203.txt` with the following content:

```
[186011,313861] [170979,315381]
[182813,285996] [186011,313004]
...
```

The script will:

1. Initialize the graph with the provided edges.
2. Identify connected components.
3. Connect the components by finding the nearest points between them.
4. Write the added edges to `out_60203.txt`.

## Code Overview

- **Graph Class**: Handles graph initialization and connected components detection.

  - `__init__(self, file_name)`: Initializes the graph from the input file.
  - `__initialise_graph(self, file_name)`: Reads the input file and adds edges to the graph.
  - `__add_edge(self, start_vertex, end_vertex)`: Adds an edge to the graph.
  - `__DFS_util(self, temp, vertex, visited)`: Depth-First Search utility for finding connected components.
  - `find_connected_groups(self)`: Finds all connected components in the graph.

- **connect_groups(groups)**: Connects the identified components by finding the nearest points between them using a KDTree.

- **write_to_file(edges)**: Writes the added edges to the output file.

## License

This project is licensed under the MIT License.
