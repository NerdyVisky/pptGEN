few_shot_examples = [
  {
           "presentation_ID": 11111,
           "topic": "0/1 Knapsack Problem",
           "outline": """
            The 0/1 Knapsack problem is a fundamental conundrum in computer science, tasked with maximizing value while respecting weight constraints. Its premise involves selecting items from a given set, each with an associated weight and value, to fill a knapsack of limited capacity. The challenge lies in determining the optimal combination of items to maximize the total value without surpassing the knapsack's weight limit. This problem is commonly tackled using dynamic programming techniques, where a table is filled iteratively to compute the maximum value achievable for various subproblems. The algorithm progresses by considering each item sequentially and updating the table with the maximum value achievable at each weight capacity. Once the table is fully populated, the solution can be found in its last cell, representing the maximum value attainable with the given constraints. Real-life applications of the 0/1 Knapsack problem span diverse domains. It finds utility in resource allocation for project management, portfolio optimization in finance, packet routing in telecommunications, cargo loading in transportation, and inventory management in retail. These applications leverage the problem's ability to efficiently optimize resource allocation, making it a crucial tool in decision-making processes across various industries.
            """,
           "ppt_content":
           """
       {{
        "presentation_ID": 11237,
        "topic": "0/1 Knapsack Problem"
        "slides": [
           {{
              "slide_number": 1,
              "title": "Solving the 0/1 Knapsack Problem",
              "description": "Djikstra's Algorithm is a foundational tool in computer science for finding the shortest path between nodes in a graphExploring Dynamic Programming Approaches",
              "enumeration": [],
              "equations": []
           }},
           {{
              "slide_number": 2,
              "title": "Introduction to 0/1 Knapsack",
              "description": "Definition: A classic optimization problem in computer science and combinatorial optimization. Given a set of items, each with a weight and a value, determine the number of each item to include in a knapsack so that the total weight is less than or equal to a given limit, and the total value is maximized.",
              "enumeration": [
                  "Widely applicable in various fields such as resource allocation, finance, and logistics.",
                  "Foundation for understanding dynamic programming techniques."
              ],
              "equations": []
           }},
           {{
              "slide_number": 3,
              "title": "0/1 Knapsack: Pseudocode",
              "description": "Dynamic Programming Algorithm for 0/1 Knapsack:",
              "enumeration": [
                  "-> Initialize a 2D array 'dp' of size (n+1) x (W+1)",
                  "-> Iterate over each item and each possible weight capacity.",
                  "-> At each step, determine whether including the current item would increase the total value.",
                  "-> Update the 'dp' table accordingly.",
                  "-> The final entry in 'dp[n][W]' contains the maximum achievable value."
              ],
              "equations":[
                {{
                "eq_desc": "DP Algorithm for 0/1 Knapsack",
                "tex_code": "$DP[i][j] = \\max(DP[i-1][j], DP[i-1][j - w[i]] + v[i])$"
                }}
              ]
           }},
           {{
              "slide_number": 4,
              "title": "Use Cases",
              "description": "0/1 Knapsack has a wide range of applications.",
              "enumeration": [
                 "Resource allocation in project management.",
                 "Portfolio optimization in finance.",
                 "Cargo loading in transportation logistics.",
                 "Subset selection in machine learning feature engineering."
              ],
              "equations": []
           }}
        ]
        }}
           """
       },
  {
    "presentation_ID": 22222,
    "topic": "Language Modeling, Syntax, Parsing",
    "context": """
      Natural Language Processing (NLP) is a vast field concerned with the interaction between computers and human language. A core subfield within NLP is Language Modeling (LM), which deals with statistically analyzing and representing language patterns. LMs learn the probabilities of word sequences, enabling them to predict the next word in a sequence, generate text, translate languages, and perform other tasks involving human language.
      The interplay between language modeling, syntax, and parsing is crucial for various NLP applications. LMs benefit from syntactic knowledge to generate more coherent and grammatically correct text. Parsing empowers computers to extract meaning from sentences by understanding their structure. Together, these concepts lay the foundation for tasks like machine translation, sentiment analysis, question answering, and text summarization.
      """,
    "ppt_content": """
    {{
      "presentation_ID": 11404,
      "topic": "Language Modeling, Syntax, Parsing"
      "slides": [
        {{
          "slide_number": 1,
          "title": "Language Modeling, Syntax, and Parsing",
          "description": "Cornerstones of Natural Language Processing (NLP)",
          "enumeration": [],
          "equations": []
        }},
        {{
          "slide_number": 2,
          "title": "Language Modeling (LM)",
          "description": "Statistical analysis and representation of language patterns.",
          "enumeration": [
            "Predicting next words in sequences",
            "Text generation",
            "Machine translation",
            "Understanding word relationships"
          ],
          "equations": [
            {{
              "eq_desc": "LM Probability Distribution",
              "tex_code": "$P(w_n | w_1, w_2, ..., w_[n-1])$"
            }}
          ]
        }},
        {{
          "slide_number": 3,
          "title": "Syntax",
          "description": "The grammatical structure of language",
          "enumeration": [
            "Rules for combining words into phrases and sentences",
            "Ensuring grammatically correct structures",
            "Understanding word order and relationships"
          ],
          "equations": [
            {{
              "eq_desc": "Example Context-Free Grammar Rule",
              "tex_code": "VP -> VB NP"
            }}
          ]
        }},
        {{
          "slide_number": 4,
          "title": "Parsing",
          "description": "Analyzing sentences and their structure",
          "enumeration": [
            "Breaking down sentences into constituents (words, phrases)",
            "Identifying syntactic relationships",
            "Understanding sentence structure for meaning extraction"
          ],
          "equations": []
        }},
        {{
          "slide_number": 5,
          "title": "Interplay and Applications",
          "description": "Synergy for NLP tasks",
          "enumeration": [
            "LMs leveraging syntax for coherent text generation",
            "Parsing for semantic understanding",
            "Foundation for tasks like machine translation, sentiment analysis, question answering, and text summarization"
          ],
          "equations": []
        }}
      ]
    }}
    """
  }
]


suffix = """
       Look at the above examples and help me create the content for a presentation of the following details:
       Topic : {topic}\n
       Refer the following context when you make the presentation:\n
       {context}
       The presentation ID is {presentation_ID}.
       """

prefix = f"""
        I am a university professor and I want you to help me prepare content of presentations based on a lecture topic I will provide.
        You can access to all online resources and the context I proivde on the provided topic\n
        I want you to provide slide-wise detailed content in a JSON format. Make sure you understand the semantic meaning of each title to generate body content for that slide. Make use of bulleted enumerations, and maintain coherence from one slide to the next.
        I am also providing context to generate the content. Generate content only based on the context I provide. 
        \nAdditionally, I am sharing a few examples where "User" is my prompt and "Expected JSON Output" is the expected output.\n
   """
template = """
       I am a university professor and I want you to help me prepare a presentation on the topic of {topic}\n
       Prepare the actual content based on your knowledge of the topic \n
       The presentation must have 6 slides on {topic}
       First determine an appropriate Table of Contents of the presentation.
       Each slide should have a title, and two textboxes - one paragraph-style (named description), and one point-wise-style (named enumeration)\n
       The title should be between 1 to 4 words.\n
       The description textbox should be between 10-50 words.\n
       The enumeration should be rendered as a list where each element is a string is a bullet point of length between 1 to 4 words.
       Equation is mandatory for each ppt, that means atleast on one slide. Determine whether you require an equation to explain a concept described in the slide and then generate the LaTex format of the equation.
       Consider this an advanced university level course, and prepare the depth of content accordingly.
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       \n\n
       """

few_shot_template = """
       User:\n
       Create presentation content for a lecture to be presented on {topic}\n
       Use the following context to derive knowledge about the topic:\n
       {context}
       \n
       Keep the following requirements in mind:\n
       1. The presentation must have 6 slides.
       2. Each slide should have a title, and two textboxes - one paragraph-style (named description), and one point-wise-style (named enumeration)\n
       3. The title should be between 1 to 4 words.\n
       4. The description textbox should be between 10-50 words.\n
       5. The enumeration should be rendered as a list where each element is a string is a bullet point.
       6. The equation is mandatory for each ppt, that means atleast on one slide. Determine whether you require an equation to explain a concept described in the slide and then generate the LaTex format of the equation.
       
       Consider this an advanced university level course, and prepare the depth of content accordingly. Keep the content as detailed as possible.\n
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       \n\n
       Expected JSON Output:\n
       {ppt_content}
       """

sample_context = """
Dijkstra's algorithm is a foundational method in computer science used for finding the shortest paths between nodes in a graph, particularly in weighted graphs with non-negative edge weights. Named after Dutch computer scientist Edsger W. Dijkstra, the algorithm efficiently explores the graph from a starting node outward, iteratively updating the shortest distance to each node it encounters. It maintains a priority queue or a set to keep track of the nodes whose shortest distances from the source have not yet been finalized. At each iteration, it selects the node with the smallest tentative distance and relaxes the distances of its neighboring nodes, potentially reducing their tentative distances. This process continues until all nodes have been visited or until the shortest path to the target node is found. Dijkstra's algorithm guarantees the shortest path under the condition that the graph does not contain negative weight cycles.\n
Real-life applications of Dijkstra's algorithm are widespread across various domains. In transportation networks, it can be used to find the shortest route between two locations on a road map, optimizing travel time or distance for navigation systems. Similarly, in telecommunications, it aids in routing data packets through networks efficiently, minimizing latency and congestion. Additionally, Dijkstra's algorithm finds utility in network routing protocols, such as the Open Shortest Path First (OSPF) protocol used in Internet Protocol (IP) networks, where it determines the shortest paths between routers to facilitate packet forwarding. Moreover, it is employed in logistics and supply chain management to optimize delivery routes, reducing transportation costs and improving delivery times. By enabling efficient pathfinding in various applications, Dijkstra's algorithm plays a crucial role in enhancing efficiency and performance across diverse industries.
"""