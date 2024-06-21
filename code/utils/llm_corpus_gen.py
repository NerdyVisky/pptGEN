# Generate 1000 random code samples
# Generate 1000 random URL links
import os
import re
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (ChatPromptTemplate)

TOPICS = {
    "Implementing Trie Data Structure": "Python",
    "KMP Algorithm": "C++",
    "Binary Search Tree Operations": "Java",
    "Bellman-Ford Algorithm": "Javascript",
    "Graph Coloring": "Solidity",
    "Floyd-Warshall Algorithm": "Python",
    "AVL Tree Implementation": "C++",
    "Breadth First Search": "Java",
    "Depth Limited Search": "Javascript",
    "Prim's Algorithm": "Solidity",
    "Kruskal's Algorithm": "Python",
    "Topological Sorting": "C++",
    "Shortest Path in Unweighted Graph": "Java",
    "A* Pathfinding Algorithm": "Javascript",
    "Min-Cost Max Flow": "Solidity",
    "Union-Find Data Structure": "Python",
    "Radix Sort": "C++",
    "Huffman Coding": "Java",
    "Tarjan's Strongly Connected Components Algorithm": "Javascript",
    "Ford-Fulkerson Algorithm": "Solidity",
    "Articulation Points and Bridges": "Python",
    "Convex Hull Algorithms": "C++",
    "Segment Tree with Lazy Propagation": "Java",
    "Z Algorithm for Pattern Matching": "Javascript",
    "Biconnected Components": "Solidity",
    "Bloom Filter": "Python",
    "Edmonds-Karp Algorithm": "C++",
    "Viterbi Algorithm": "Java",
    "Boyer-Moore Majority Vote Algorithm": "Javascript",
    "Rabin-Karp Algorithm": "Solidity",
    "K-D Tree Implementation": "Python",
    "Suffix Array and Suffix Tree": "C++",
    "Matrix Exponentiation": "Java",
    "Counting Inversions": "Javascript",
    "Maximum Bipartite Matching": "Solidity",
    "Johnson's Algorithm for All-Pairs Shortest Paths": "Python",
    "Longest Increasing Subsequence": "C++",
    "Dinic's Algorithm": "Java",
    "Trie Data Structure": "Javascript",
    "B-Tree Implementation": "Solidity",
    "Sparse Table": "Python",
    "Hopcroft-Karp Algorithm": "C++",
    "Maximum Subarray Problem": "Java",
    "Disjoint Set Union (DSU)": "Javascript",
    "Interval Tree": "Solidity",
    "Palindromic Substrings": "Python",
    "Sliding Window Maximum": "C++",
    "Binary Indexed Tree (Fenwick Tree)": "Java",
    "Longest Common Subsequence": "Javascript",
    "Eulerian Path and Circuit": "Solidity",
    "Hamiltonian Cycle": "Python",
    "Gaussian Elimination": "C++",
    "Hungarian Algorithm": "Java",
    "Binary Search Tree": "Javascript",
    "Mo's Algorithm": "Solidity",
    "Persistent Segment Tree": "Python",
    "Cartesian Tree": "C++",
    "Karger's Algorithm": "Java",
    "Counting Sort": "Javascript",
    "Subset Sum Problem": "Solidity",
    "Matrix Chain Multiplication": "Python",
    "Longest Palindromic Subsequence": "C++",
    "Knuth-Morris-Pratt Algorithm": "Java",
    "Ternary Search": "Javascript",
    "Segment Tree": "Solidity",
    "Josephus Problem": "Python",
    "Cycle Detection in Graph": "C++",
    "Topological Sort": "Java",
    "Sieve of Eratosthenes": "Javascript",
    "Quick Sort": "Solidity",
    "Merge Sort": "Python",
    "Bubble Sort": "C++",
    "Selection Sort": "Java",
    "Insertion Sort": "Javascript",
    "Heap Sort": "Solidity",
    "Pancake Sorting": "Python",
    "Sleep Sort": "C++",
    "Tim Sort": "Java",
    "Shell Sort": "Javascript",
    "Bucket Sort": "Solidity",
    "Median of Medians": "Python",
    "Fisher-Yates Shuffle": "C++",
    "Gnome Sort": "Java",
    "Comb Sort": "Javascript",
    "Counting Sort": "Solidity",
    "Cocktail Shaker Sort": "Python",
    "Odd-Even Sort": "C++",
    "Strand Sort": "Java",
    "Binary Insertion Sort": "Javascript",
    "Pigeonhole Sort": "Solidity",
    "Cycle Sort": "Python",
    "Bogo Sort": "C++",
    "Bitonic Sort": "Java",
    "Stooge Sort": "Javascript",
    "Introduction to Sorting Algorithms": "Solidity",
    "Introduction to Search Algorithms": "Python",
    "Depth First Search": "C++",
    "Breadth First Search": "Java",
    "Introduction to Graph Algorithms": "Javascript",
    "Basic Data Structures": "Solidity",
    "Array and Linked List": "Python",
    "Stack and Queue": "C++",
    "Hash Table": "Java",
    "Binary Tree": "Javascript",
    "AVL Tree": "Solidity",
    "Red-Black Tree": "Python",
    "B Tree": "C++",
    "B+ Tree": "Java",
    "Splay Tree": "Javascript",
    "Binary Heap": "Solidity",
    "Fibonacci Heap": "Python",
    "Binomial Heap": "C++",
    "Leftist Heap": "Java",
    "Skew Heap": "Javascript",
    "Treap": "Solidity",
    "k-ary Heap": "Python",
    "Radix Tree": "C++",
    "Ternary Search Tree": "Java",
    "Tries": "Javascript",
    "Suffix Trie": "Solidity",
    "Patricia Trie": "Python",
    "Bloom Filter": "C++",
    "Skip List": "Java",
    "Van Emde Boas Tree": "Javascript",
    "Segment Tree": "Solidity",
    "Fenwick Tree": "Python",
    "Suffix Array": "C++",
    "Suffix Tree": "Java",
    "Cartesian Tree": "Javascript",
    "Kd Tree": "Solidity",
    "Range Tree": "Python",
    "Interval Tree": "C++",
    "Order Statistic Tree": "Java",
    "Persistent Data Structures": "Javascript",
    "Multidimensional Binary Indexed Tree": "Solidity",
    "Persistent Segment Tree": "Python",
    "Binary Search": "C++",
    "Linear Search": "Java",
    "Jump Search": "Javascript",
    "Interpolation Search": "Solidity",
    "Exponential Search": "Python",
    "Fibonacci Search": "C++",
    "Ternary Search": "Java",
    "Introductory Sorting Algorithms": "Javascript",
    "Selection Sort": "Solidity",
    "Bubble Sort": "Python",
    "Insertion Sort": "C++",
    "Merge Sort": "Java",
    "Quick Sort": "Javascript",
    "Heap Sort": "Solidity",
    "Radix Sort": "Python",
    "Counting Sort": "C++",
    "Bucket Sort": "Java",
    "Shell Sort": "Javascript",
    "Comb Sort": "Solidity",
    "Cocktail Shaker Sort": "Python",
    "Cycle Sort": "C++",
    "Pancake Sort": "Java",
    "Binary Insertion Sort": "Javascript",
    "Gnome Sort": "Solidity",
    "Bitonic Sort": "Python",
    "Tim Sort": "C++",
    "Introductory Data Structures": "Java",
    "Linked List": "Javascript",
    "Stack": "Solidity",
    "Queue": "Python",
    "Double-Ended Queue (Deque)": "C++",
    "Priority Queue": "Java",
    "Set Data Structure": "Javascript",
    "Hash Set": "Solidity",
    "Map Data Structure": "Python",
    "Hash Map": "C++",
    "Tree Map": "Java",
    "Graph Data Structure": "Javascript",
    "Directed Graph": "Solidity",
    "Undirected Graph": "Python",
    "Weighted Graph": "C++",
    "Unweighted Graph": "Java",
    "Cyclic Graph": "Javascript",
    "Acyclic Graph": "Solidity",
    "Complete Graph": "Python",
    "Bipartite Graph": "C++",
    "Simple Graph": "Java",
    "Multigraph": "Javascript",
    "Hypergraph": "Solidity",
    "Planar Graph": "Python",
    "Tree": "C++",
    "Binary Tree": "Java",
    "Binary Search Tree": "Javascript",
    "AVL Tree": "Solidity",
    "Red-Black Tree": "Python",
    "B Tree": "C++",
    "B+ Tree": "Java",
    "Splay Tree": "Javascript",
    "Treap": "Solidity",
    "Cartesian Tree": "Python",
    "Kd Tree": "C++",
    "Range Tree": "Java",
    "Interval Tree": "Javascript",
    "Order Statistic Tree": "Solidity",
}

def configure_llm(TEMPERATURE=0,LLM_MODEL='gpt-3.5-turbo'):
     model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
     return model

def generate_code_snippets(ID=111111):
     print(f"Generating code snippets for ID: {ID}")
     model = configure_llm(TEMPERATURE=0.5, LLM_MODEL='gpt-3.5-turbo')
     prompt = ChatPromptTemplate.from_messages([
          ("system", "You are a helpful code assistant. You have access to internet resources"),
          ("human", """I am a professor of Computer Science, I want to generate code for certain topics in CS. I am providing you a Python Dict where the keys are topics \
           I want to generate code for and the value is the programming language I want my code in. The dict is as follows:\n
           {topics}
           Generate code as plain text seperated by ```code<content>``` and three line breaks. \
           Here do not change the word code inside the side-ticks as it will be used to get individual code segments.\
           Make sure to not make any syntax errors,\
           and hence double check each output code snippet.\n
           
           Keep the following in mind:\n
           1. Do not generate additional elements unless they are part of the above request. 
           2. Once generating the all the code snipptes, verify that the total number of snippets generated are the same as total number of requests.
           3. Do not provide any input and output examples in the code or any library imports. Just the basic code function. 
           4. Do not provide more than 30 lines of code in any case.
           """)
     ])
     chain = prompt | model
     gen_code = chain.invoke({"topics": TOPICS}).content
     code_dump = f"code\\buffer\\corpus\\{ID}.txt"

     with open(code_dump, 'w') as file:
        file.write(gen_code)

     with open(code_dump, 'r') as file:
        content = file.read()
        pattern = r'```code(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        code_dir = 'code\\buffer\\corpus\\code_snips'
        code_snip_paths = []
        for i, match in enumerate(matches):
            code_snippet = match.strip() # Remove leading/trailing whitespace
            # print(code_snippet)
            os.makedirs(os.path.join(code_dir, ), exist_ok=True)
            code_snip_name = f'{hex(random.randint(0x100000, 0xFFFFFF))[2:]}.txt'
            code_file_path = os.path.join(code_dir, code_snip_name)
            with open(code_file_path, 'w') as file:
                file.write(code_snippet)
            code_snip_paths.append(code_file_path)
     return code_snip_paths


# code_snip_paths = generate_code_snippets()
def store_all_file_paths():
    root_dirs = ['code\\buffer\\corpus\\charts', 'code\\buffer\\corpus\\diagrams', 'code\\buffer\\corpus\\equations', 'code\\buffer\\corpus\\tables', 'code\\buffer\\corpus\\code_snips']
    for dir_path in root_dirs:
        files = [f'{dir_path}/{f}' for f in os.listdir(dir_path)]
        base_name = os.path.basename(dir_path)
        match base_name:
            case 'charts':
                CHARTS = files
            case 'diagrams':
                DIAGRAMS = files
            case 'tables':
                TABLES = files
            case 'equations':
                EQUATIONS = files
            case 'code_snips':
                CODE_SNIPS = files
    with open('code\\utils\\corpus_paths.py', 'w') as file:
        file.writelines(f'CHARTS = {CHARTS}\n\n')
        file.writelines(f'DIAGRAMS = {DIAGRAMS}\n\n')
        file.writelines(f'TABLES = {TABLES}\n\n')
        file.writelines(f'EQUATIONS = {EQUATIONS}\n\n')
        file.writelines(f'CODE_SNIPS = {CODE_SNIPS}\n\n')
    return True

# for i in range(1, 11):
#     ID = 100000 + i
#     code_snip_paths = generate_code_snippets(ID)
#     print(ID)
#     print(f"Code Snippets generated for ID: {ID}")

if(store_all_file_paths()):
    print("File paths stored")
else:
    raise Exception("ERR")
