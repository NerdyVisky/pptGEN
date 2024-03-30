few_shot_examples = [
       {
           "presentation_ID": 11111,
           "topic": "0/1 Knapsack Problem",
           "level": "advanced",
           "TOC": "1. Title Slide\n 2. Introduction slide\n 3. Algorithm pseudocode\n 4. Use Cases of the algorithm",
           "ppt_content":
           """
       {{
        "presentation_ID": 11237,
        "slides": [
           {{
              "slide_number": 1,
              "title": "Solving the 0/1 Knapsack Problem",
              "description": "Djikstra's Algorithm is a foundational tool in computer science for finding the shortest path between nodes in a graphExploring Dynamic Programming Approaches",
              "enumeration": []
           }},
           {{
              "slide_number": 2,
              "title": "Introduction to 0/1 Knapsack",
              "description": "Definition: A classic optimization problem in computer science and combinatorial optimization. Given a set of items, each with a weight and a value, determine the number of each item to include in a knapsack so that the total weight is less than or equal to a given limit, and the total value is maximized.",
              "enumeration": [
                  "Widely applicable in various fields such as resource allocation, finance, and logistics.",
                  "Foundation for understanding dynamic programming techniques."
              ]
           }},
           {{
              "slide_number": 3,
              "title": "0/1 Knapsack: Pseudocode",
              "description": "Dynamic Programming Algorithm for 0/1 Knapsack:",
              "enumeration": [
                  "Initialize a 2D array 'dp' of size (n+1) x (W+1)",
                  "Iterate over each item and each possible weight capacity.",
                  "At each step, determine whether including the current item would increase the total value.",
                  "Update the 'dp' table accordingly.",
                  "The final entry in 'dp[n][W]' contains the maximum achievable value."
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
              ]
           }}
        ]
        }}
           """
       },
       {    "presentation_ID": 11112,
            "topic": "Machine Translation",
            "level": "introductory",
            "TOC": "1. Title Slide\n 2. Introduction\n 3. Methods in MT\n 4. <Common Method in MT>",
            "ppt_content": 
            """
        {{
        "presentation_ID": 11112,
        "slides": [
           {{
              "slide_number": 1,
              "title": "Machine Translation",
              "description": "The art of translating between languages by the machines!",
              "enumeration": []
           }},
           {{
              "slide_number": 2,
              "title": "Introduction to Machine Translation",
              "description": "Machine Translation has been defined as the process that utilizes computer software to translate text from one natural language(such as English) to another (such as French).",
              "enumeration": [
                "The idea of machine translation may be traced back to the 17th century",
                "MT on the web starts with Systran offering free translation of small texts (1996)"
              ]
           }},
           {{
              "slide_number": 3,
              "title": "Techniques in Machine Translation",
              "description": "",
              "enumeration": [
                 "Example-based MT",
                 "Dictionary-based",
                 "Rule-based",
                 "Hybrid MT",
                 "Neural MT",
                 "Statistical",
                 "Interlingual",
                 "Transfer-based"
              ]
           }},
           {{
              "slide_number": 4,
              "title": "Rule-based MT",
              "description": "RBMT involves more information about the linguistics of the source and target languages ,using the syntactic rules and semantic analysis of both languages",
              "enumeration": [
                 "Direct Systems",
                 "Transfer RBMT Systems",
                 "Interlingual RBMT Systems"
              ]
           }}
        ]
     }}
     """           
       }
   ]


suffix = """
       Look at the above examples and help me create the content for a presentation of the following details:
       Topic : {topic}\n
       Level : {level}\n
       Table of Contents : {TOC}\n

       The presentation ID is {presentation_ID}
       """

prefix = f"""
        I am a university professor and I want you to help me prepare content of presentations based on a lecture topic I will provide.
        You can access to all online resources to acquire content on the provided topic\n
        I want you to provide slide-wise detailed content in a JSON format. Make sure you understand the semantic meaning of each title to generate body content for that slide. Make use of bulleted enumerations, and maintain coherence from one slide to the next. 
        \nI am sharing a few examples where "User" is my prompt and "Expected JSON Output" is the expected output.\n
   """
template = """
       User:
       Prepare a presentation having 6 slides on {topic}, with the following table of contents:
       \n\n
       {TOC}
       \n\n
       For each slide, please ensure the following constraints while generating PPT\n
        1. Title should be between 1 to 4 words
        2. The description should be between 5 and 50 words
        3. The enumeration list should have between 1 and 5 items, with each item having 1 to 3 words.
       Consider this a {level} level course, and prepare the depth of content accordingly.
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       \n\n\n
       
       Expected JSON output:\n
       {ppt_content}
       """