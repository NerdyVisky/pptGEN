few_shot_examples = [
       {
           "presentation_ID": 11111,
           "topic": "0/1 Knapsack Problem",
           "context": """
            The 0/1 Knapsack problem is a fundamental conundrum in computer science, tasked with maximizing value while respecting weight constraints. Its premise involves selecting items from a given set, each with an associated weight and value, to fill a knapsack of limited capacity. The challenge lies in determining the optimal combination of items to maximize the total value without surpassing the knapsack's weight limit. This problem is commonly tackled using dynamic programming techniques, where a table is filled iteratively to compute the maximum value achievable for various subproblems. The algorithm progresses by considering each item sequentially and updating the table with the maximum value achievable at each weight capacity. Once the table is fully populated, the solution can be found in its last cell, representing the maximum value attainable with the given constraints. Real-life applications of the 0/1 Knapsack problem span diverse domains. It finds utility in resource allocation for project management, portfolio optimization in finance, packet routing in telecommunications, cargo loading in transportation, and inventory management in retail. These applications leverage the problem's ability to efficiently optimize resource allocation, making it a crucial tool in decision-making processes across various industries.
            """,
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
                  "-> Initialize a 2D array 'dp' of size (n+1) x (W+1)",
                  "-> Iterate over each item and each possible weight capacity.",
                  "-> At each step, determine whether including the current item would increase the total value.",
                  "-> Update the 'dp' table accordingly.",
                  "-> The final entry in 'dp[n][W]' contains the maximum achievable value."
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
            "context":
            """
            Machine Translation (MT) in Natural Language Processing (NLP) is a pivotal field dedicated to automatically translating text from one language to another. Its objective is to replicate the human ability to comprehend and generate natural language across different linguistic systems. MT systems typically employ a variety of techniques ranging from statistical models to neural networks. These methods learn patterns and relationships between languages from vast amounts of parallel corpora, which consist of texts in multiple languages aligned at the sentence or phrase level. One common approach is the sequence-to-sequence (Seq2Seq) model, which utilizes recurrent neural networks (RNNs) or transformers to map input sequences in one language to output sequences in another. The training process involves minimizing the difference between the predicted translation and the reference translation using techniques like maximum likelihood estimation or reinforcement learning. Real-world applications of MT are extensive, impacting global communication, commerce, and cultural exchange. It enables seamless translation in international business dealings, facilitates cross-border collaborations, and enhances accessibility to information across linguistic barriers. MT is also integral to platforms like online language learning resources, multilingual customer support systems, and global news dissemination networks. Moreover, MT plays a crucial role in preserving and disseminating cultural heritage by facilitating the translation of literature, historical documents, and multimedia content. As MT systems continue to advance, they hold the promise of fostering greater linguistic inclusivity and connectivity in an increasingly interconnected world.
            """,
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
       The presentation ID is {presentation_ID}
       """

prefix = f"""
        I am a university professor and I want you to help me prepare content of presentations based on a lecture topic I will provide.
        You can access to all online resources to acquire content on the provided topic\n
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
       Consider this an advanced university level course, and prepare the depth of content accordingly.
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       \n\n
       """

few_shot_template = """
       
       The presentation must have 6 slides on {topic}
       First determine an appropriate Table of Contents of the presentation.
       Each slide should have a title, and two textboxes - one paragraph-style (named description), and one point-wise-style (named enumeration)\n
       The title should be between 1 to 4 words.\n
       The description textbox should be between 10-50 words.\n
       The enumeration should be rendered as a list where each element is a string is a bullet point of length between 1 to 4 words. 
       Consider this an advanced university level course, and prepare the depth of content accordingly.
       \n I am providing you a unique presentation_ID for each presentation which you need to attach as a key in your JSON output: {presentation_ID}
       \n\n
       Expected JSON Output:\n
       {ppt_content}
       """