


outline_prompt = [
            ("system", "You are a helpful university professor and you are guiding your PhD student to create an outline for the lecture he will deliver to a class."),
            ("human", """I would like to get help designing a detailed Table of Contents for an advanced university presentation lecture on {topic}. Please help me create the Table of Content in form of a Python dict.\n
Example:\n
Input Topic : Tree Data Structures
Expected Output:\n
[
    "Introduction : Definition & Characteristics",
    "Introduction : Example of a Tree",
    "Types of Trees",
    "Binary Trees : What are they?",
    "Binary Trees : Searching an element",
    "Tree Traversal",
    "Pre-order Traversal",
    "In-order Traversal",
    "Post-order Traversal",
    "Comparing traversal methods",
    "Binary Search Trees: Introduction",
    "Binary Search Trees: Time Complexity",
    "BST v/s Binary Trees",
    "Applications of Trees",
    "Huffman Algorithm : History",
    "Huffman Algorithm : Pseudocode",
    "Summary of Trees"
]
             \n
             I want you to provide the output in form of a python list of strings having slide titles of each slide. The length of the list will be the total number of slides in the presentation. Do not generate more than 15 slide titles.           
             Just return the output without the conversation.""")
        ]
instruction_example = [
    {
        "topic": "Divide and Conquer Approach",
        "outline": """[
    "Introduction to Gaussian Distributions",
    "Historical Background",
    "The Normal Distribution: Definition",
    "Properties of Gaussian Distributions",
    "Probability Density Function",
    "Cumulative Distribution Function",
    "Parameters of Gaussian Distribution: Mean and Variance",
    "Standard Normal Distribution",
    "Z-Scores and Normalization",
    "Central Limit Theorem",
    "Applications of Gaussian Distributions",
    "Estimating Parameters",
    "Maximum Likelihood Estimation",
    "Gaussian Distributions in Machine Learning",
    "Multivariate Gaussian Distribution",
    "Covariance and Correlation Matrices",
    "Sampling from a Multivariate Gaussian",
    "Gaussian Processes",
    "Challenges and Limitations of Gaussian Models",
    "Summary and Conclusions"
]
""",
   "elements": ['flow-chart', 'graph', 'tree', 'block-diagram', 'enumeration','description', 'url', 'table', 'equation', 'plot', 'bar-chart', 'line-chart', 'pie-chart', '3d-plot'],
   "output": """
{{
    "Introduction to Gaussian Distributions": [
        {{"element_type": "description", "element_caption": "Overview of Gaussian distributions and their importance in statistics"}},
        {{"element_type": "graph", "element_caption": "Visual introduction to the bell curve shape of Gaussian distributions"}}
    ],
    "Historical Background": [
        {{"element_type": "description", "element_caption": "Discussion on the origin and development of Gaussian distributions"}},
        {{"element_type": "timeline", "element_caption": "Timeline of key historical milestones related to Gaussian distributions"}}
    ],
    "The Normal Distribution: Definition": [
        {{"element_type": "description", "element_caption": "Formal definition of the normal distribution"}},
        {{"element_type": "equation", "element_caption": "Mathematical equation of the normal distribution"}}
    ],
    "Properties of Gaussian Distributions": [
        {{"element_type": "block-diagram", "element_caption": "Diagram showing key properties such as symmetry and bell shape"}},
        {{"element_type": "enumeration", "element_caption": "List of statistical properties like mean, variance, etc."}}
    ],
    "Probability Density Function": [
        {{"element_type": "equation", "element_caption": "Equation of the probability density function for a Gaussian distribution"}},
        {{"element_type": "plot", "element_caption": "Plot showing the probability density function across different values"}}
    ],
    "Cumulative Distribution Function": [
        {{"element_type": "description", "element_caption": "Defining cumulative distribution function"}},
        {{"element_type": "plot", "element_caption": "Graphical representation of CDF for Gaussian distribution"}}
    ],
    "Parameters of Gaussian Distribution: Mean and Variance": [
        {{"element_type": "description", "element_caption": "Explanation of mean and variance in Gaussian distributions"}},
        {{"element_type": "table", "element_caption": "Table showing effects of different means and variances on the distribution shape"}}
    ],
    "Standard Normal Distribution": [
        {{"element_type": "description", "element_caption": "Characteristics of the standard normal distribution"}},
        {{"element_type": "equation", "element_caption": "Equation defining the standard normal distribution"}}
    ],
    "Z-Scores and Normalization": [
        {{"element_type": "description", "element_caption": "Explanation of Z-scores and their use in normalization"}},
        {{"element_type": "graph", "element_caption": "Graph showing transformation of data into Z-scores"}}
    ],
    "Central Limit Theorem": [
        {{"element_type": "description", "element_caption": "Statement and explanation of the Central Limit Theorem"}},
        {{"element_type": "graph", "element_caption": "Graphical illustration of the theorem using sample means"}}
    ],
    "Applications of Gaussian Distributions": [
        {{"element_type": "enumeration", "element_caption": "List of various applications in different fields"}},
        {{"element_type": "flow-chart", "element_caption": "Flowchart showing decision-making based on Gaussian statistics"}}
    ],
    "Estimating Parameters": [
        {{"element_type": "description", "element_caption": "Methods for estimating parameters of Gaussian distributions"}},
        {{"element_type": "block-diagram", "element_caption": "Diagram illustrating parameter estimation techniques"}}
    ],
    "Maximum Likelihood Estimation": [
        {{"element_type": "description", "element_caption": "Introduction to maximum likelihood estimation"}},
        {{"element_type": "equation", "element_caption": "Equation used in the maximum likelihood estimation for Gaussian"}}
    ],
    "Gaussian Distributions in Machine Learning": [
        {{"element_type": "description", "element_caption": "Overview of how Gaussian distributions are used in machine learning"}},
        {{"element_type": "flow-chart", "element_caption": "Flowchart showing steps in a machine learning model using Gaussian assumptions"}}
    ],
    "Multivariate Gaussian Distribution": [
        {{"element_type": "description", "element_caption": "Explanation of multivariate Gaussian distributions"}},
        {{"element_type": "3d-plot", "element_caption": "3D plot of a multivariate Gaussian distribution"}}
    ],
    "Covariance and Correlation Matrices": [
        {{"element_type": "description", "element_caption": "Defining covariance and correlation in the context of Gaussian distributions"}},
        {{"element_type": "table", "element_caption": "Table showing example covariance and correlation matrices"}}
    ],
    "Sampling from a Multivariate Gaussian": [
        {{"element_type": "description", "element_caption": "Techniques for sampling from a multivariate Gaussian distribution"}},
        {{"element_type": "plot", "element_caption": "Plot showing samples drawn from a multivariate Gaussian"}}
    ],
    "Gaussian Processes": [
        {{"element_type": "description", "element_caption": "Introduction to Gaussian processes"}},
        {{"element_type": "graph", "element_caption": "Graph illustrating a simple Gaussian process"}}
    ],
    "Challenges and Limitations of Gaussian Models": [
        {{"element_type": "description", "element_caption": "Discussion on the limitations and challenges of using Gaussian models"}},
        {{"element_type": "enumeration", "element_caption": "List of common issues and scenarios where Gaussian models may fail"}}
    ],
    "Summary and Conclusions": [
        {{"element_type": "description", "element_caption": "Recap of key points covered in the presentation"}},
        {{"element_type": "bar-chart", "element_caption": "Bar chart summarizing the usage of Gaussian distributions across different fields"}}
    ]
}}
"""}
]
instruction_prompt = ("human", """Hello. I want you to help me prepare lecture slides on {topic}. I am providing you with the outline of the lecture in form of a nested dictionary.\n
                 Outline :{outline}
                 Each element in the object is a slide where the value represent the slide title. I want you to add two keys namely 'element_type' and 'element_caption' for each subsection and determine which types of elements would be most beneficial to understand that subsection.\n
                 The elements can be as follows: {elements}.\n
                 You should provide three elements per subheading.\n
                 Whenever possible generate atleast one text based element (Description, URL, or Enumeration) and one visual element (Rest of the elements) per subsection, such that there is diversity in elements.\n
                 As a rule of thumb, make sure the distribution of elements is nearly same for the entire presentation.\n 
                 I want you to generate the results within the outline and only output the revised outline without any conversation.\n
                 Do not generate the slide numbers in the output, they are just for your reference.
                 """)



instruction_example_prompt = [
                ("human", """Hello. I want you to help me prepare lecture slides on {topic}. I am providing you with the outline of the lecture in form of a nested dictionary.\n
                 Outline :{outline}
                 Each element in the object is a slide where the value represent the slide title. I want you to add two keys namely 'element_type' and 'element_caption' for each subsection and determine which types of elements would be most beneficial to understand that subsection.\n
                 The elements can be as follows: {elements}.\n
                 You should provide three elements per subheading.\n
                 Whenever possible generate atleast one text based element (Description, URL, or Enumeration) and one visual element (Rest of the elements) per subsection, such that there is diversity in elements.\n
                 As a rule of thumb, make sure the distribution of elements is nearly same for the entire presentation.\n 
                 I want you to generate the results within the outline and only output the revised outline without any conversation.\n
                 """),
                 ("ai", "{output}")
            ]


generation_prompt =  [
                ("system", "You are an capable and expert content creator. You can create multi-modal content such as text, images, code, etc. You also have access to all internet sources at your discretion."),
                ("human", """
                 I am a university professor and I want to create lecture slides on the topic of {topic}\n
                 I am providing you the Table of Contents for the same:\n
                 {outline}
                 \n
                 Within each subsection of the Table of Contents, I have the list of element types I want to render while explaining that particular subsection with element_caption as the instruction to generate the element.\n
                 Generate presentation content by keeping the following instructions in mind:\n
                 1. Each section in the Table of Contents must be a title slide with no body elements.\n
                 2. Each subsection in the Table of Contents should have the key name as the title with the body elements described by element_type, and element_caption.\n
                 3. Depending on the element_type for each element in a subsection, you have to generate appropriate modality of the content. Consider the following guidelines for specific element_types:\n
                 \t a. For element_type = 'description', you have to generate paragraph style element named description which explains or gives brief introduction to the topic.
                 \t b. For element type = 'enumeration', you have to generate point-wise style element named enumeration. An enumeration can be a single point.\n
                 \t c. For element_type = 'url', you have to generate a hyperlink to a URL according to element_caption. You can use any link as URL.\n
                 \t e. For element_type = 'equation', you have to generate LaTex Code depending on the instruction given in element_caption.\n
                 \t f. For element_type = 'table', you have to generate a table depending on the instruction given in element_caption. Use Latex code.\n
                 \t g. For element_type = 'flowchart', you have to generate a flowchart depending on the instruction given in element_caption. Use Latex code. Follow the general guidelines for a flowchart, like each node should be a node with shape as per its use, arrows should be directional.\n
                 \t h. For element_type = 'graph', you have to generate LaTex Code depending on the instruction given in element_caption. Graphs are figures with nodes and vertices. Each element in graph should be labelled if required.\n
                 \t i. For element_type = 'diagram', you have to generate LaTex Code depending on the instruction given in element_caption. Diagrams can be simple block diagrams representing an entity or Venn Diagrams.\n
                 4. The first point in an enumeration is the heading of the enumeration.\n
                 I want you to generate have atleast 3 elements per subtopic.\n
                 The presentation content should be generated in form of a JSON object. The presentation ID is {presentation_ID}

                 """)
            ]


text_generation_example = [
    {
        "titles": """[
            "Introduction to Trees",
            "Types of Tree Data Structures",
            "Binary Trees",
            "Tree Traversals",
            "Application of Trees"
        ]
        """,
        "presentation_ID": 12451,
        "output": """
{{
"presentation_ID": 12451,
"topic": Tree Data Structure,
"slides":[
      {{
         "slide_number": 1,
         "title": "Introduction to Trees",
         "description": "Trees are hierarchical data structures consisting of nodes connected by edges. They contain a root node, branches, and leaves. Each node can have zero or more children, forming a tree-like structure. Trees are widely used in computer science for organizing and managing data efficiently.",
         "enumeration": [],
         "url": "https://www.w3schools.com/dsa/dsa_theory_trees.php"
      }},
      {{
         "slide_number": 2,
         "title": "Types of Tree Data Structures",
         "description": "",
         "enumeration": ["Types of Trees", 
                        "Binary Tree",
                        "Binary Search Tree (BST)",
                        "AVL Tree",
                        "Red-Black Tree",
                        "B-tree",
                        "Trie",
                        "Heap"
                        ],
        "url": ""
      }},
      {{
         "slide_number": 3,
         "title": "Binary Trees",
         "description": "Binary trees: Data structures composed of nodes where each node has at most two children, commonly referred to as the left child and the right child.",
         "enumeration": [],
         "url": ""
      }},
      {{
         "slide_number": 4,
         "title": "Tree Traversals",
         "description": "",
         "enumeration": ["Three types of Traversals", "Inorder", "Preorder", "Postorder"]
      }},
      {{
         "slide_number": 5,
         "title": "Application of Trees",
         "description": "",
         "enumeration": ["Various applications", "File Systems: Representing the structure of directories and files in operating systems.",
           "Network Routing: Used in routing algorithms such as OSPF and BGP",
           "Syntax Tree: Representing the structure of program code in compilers and interpreters for parsing and analysis."]
      }}
      ]
}}
        """
    }
]
text_generation_ex_prompt = [
                ("human", """I am providing some instructions which are related to generating text-based content for a presentation on Tree Data Structure with presentation ID: {presentation_ID}.
1. For the section title 'Introduction to Trees'(Slide Number 1) generate the actual text content of a description element given the element caption: Simple description of what a tree data structure is.
2. For the section title 'Introduction to Trees'(Slide Number 1) generate the actual text content of a url element given the element caption: URL to a resource on trees (Placeholder: https://www.example.com)
3. For the section title 'Types of Tree Data Structures'(Slide Number 2) generate the actual text content of a enumeration element given the element caption: Listing the names of common types of tree data structures
4. For the section title 'Binary Trees'(Slide Number 3) generate the actual text content of a description element given the element caption: Simple description of what a binary tree is.
5. For the section title 'Tree Traversals'(Slide Number 4) generate the actual text content of a enumeration element given the element caption: Listing the type of tree traversal techniques.
6. For the section title 'Application of Trees'(Slide Number 5) generate the actual text content of a enumeration element given the element caption: Enumerating various real life applications of trees.
Generate text content as a Python Dict having the topic, presentation_ID and slides. Slides will be a list of objects whose length will be total number of slides. Here are the slide-wise titles:\n
{titles}\n
Each object will have slide_number, title, description, enumeration, and url as keys.
For title, description, and url content the value is a string while for an enumeration content the value is a python list of strings where each element of that list is a string.\n"""),
                 ("ai", "{output}")
            ]