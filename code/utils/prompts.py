from random_generator import pick_random


outline_prompt = [
            ("system", "You are a helpful university professor and you are guiding your PhD student to create an outline for the lecture he will deliver to a class."),
            ("human", """I would like to get help designing a detailed Table of Contents for an advanced university presentation lecture on {topic} based on the book {book}. Please help me create the Table of Content in form of a Python dict.\n
Example:\n
Input: Tree Data Structures based on the book Data Structures and Algorithms made easy.\n 
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
             I want you to provide the output in form of a python list of strings having slide titles of each slide. The length of the list will be the total number of slides in the presentation. Do not generate more than 15 slide titles and each title should have maximum of 5 words.       
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
   "elements": ['flow-chart', 'architecture-diagram', 'sequence-diagram', 'class-diagram', 'enumeration','description', 'url', 'table', 'equation', 'plot', 'bar-chart', 'line-chart', 'pie-chart', '3d-plot'],
   "output": """
{
    "Introduction to Gaussian Distributions": [
        {"element_type": "description", "element_caption": "Overview of Gaussian distributions and their importance in statistics"},
        {"element_type": "plot", "element_caption": "An example of Gaussian Distribution"}
    ],
    "Historical Background": [
        {"element_type": "enumeration", "element_caption": "Discussion on the origin and development of Gaussian distributions"},
    ],
    "The Normal Distribution: Definition": [
        {"element_type": "enumeration", "element_caption": "Listing the characteristics of a normal distribution"},
        {"element_type": "equation", "element_caption": "Mathematical equation of the normal distribution"}
    ],
    "Properties of Gaussian Distributions": [
        {"element_type": "class-diagram", "element_caption": "Diagram showing key properties such as symmetry and bell shape"},
        {"element_type": "enumeration", "element_caption": "List of statistical properties like mean, variance, etc."}
    ],
    "Probability Density Function": [
        {"element_type": "equation", "element_caption": "Equation of the probability density function for a Gaussian distribution"},
        {"element_type": "plot", "element_caption": "Plot showing the probability density function across different values"}
    ],
    "Cumulative Distribution Function": [
        {"element_type": "enumeration", "element_caption": "Listing properties of Culminative Density Function"},
        {"element_type": "plot", "element_caption": "Graphical representation of CDF for Gaussian distribution"}
    ],
    "Parameters of Gaussian Distribution: Mean and Variance": [
        {"element_type": "enumeration", "element_caption": "Explanation of mean and variance in Gaussian distributions"},
        {"element_type": "table", "element_caption": "Table showing effects of different means and variances on the distribution shape"}
    ],
    "Standard Normal Distribution": [
        {"element_type": "enumeration", "element_caption": "Characteristics of the standard normal distribution"},
        {"element_type": "equation", "element_caption": "Equation defining the standard normal distribution"}
    ],
    "Z-Scores and Normalization": [
        {"element_type": "enumeration", "element_caption": "Bulleted list having an explanation of Z-scores and their use in normalization"},
        {"element_type": "plot", "element_caption": "Plot showing transformation of data into Z-scores"}
    ],
    "Central Limit Theorem": [
        {"element_type": "enumeration", "element_caption": "Explainaing Central Limit Theorem in short bullet points"},
    ],
    "Applications of Gaussian Distributions": [
        {"element_type": "enumeration", "element_caption": "List of various applications in different fields"},
    ],
    "Estimating Parameters": [
        {"element_type": "enumeration", "element_caption": "Listing the methods for estimating parameters of Gaussian distributions"},
        {"element_type": "sequence-diagram", "element_caption": "Sequence Diagram illustrating steps in estimating parameters"}
    ],
    "Maximum Likelihood Estimation": [
        {"element_type": "description", "element_caption": "Introduction to maximum likelihood estimation"},
        {"element_type": "equation", "element_caption": "Equation used in the maximum likelihood estimation for Gaussian"},
        {"element_type": "code", "element_caption": "Code example of calculating the Maximum Likelihood of an outcome"}
    ],
    "Gaussian Distributions in Machine Learning": [
        {"element_type": "enumeration", "element_caption": "Overview of how Gaussian distributions are used in machine learning"},
        {"element_type": "flow-chart", "element_caption": "Flowchart showing steps in a machine learning model using Gaussian assumptions"}
    ],
    "Multivariate Gaussian Distribution": [
        {"element_type": "enumeration", "element_caption": "Explanation of multivariate Gaussian distributions"},
        {"element_type": "3d-plot", "element_caption": "3D plot of a multivariate Gaussian distribution"}
    ],
    "Covariance and Correlation Matrices": [
        {"element_type": "enumeration", "element_caption": "Defining covariance and correlation in the context of Gaussian distributions"},
        {"element_type": "table", "element_caption": "Table showing example covariance and correlation matrices"}
    ],
    "Sampling from a Multivariate Gaussian": [
        {"element_type": "enumeration", "element_caption": "Techniques for sampling from a multivariate Gaussian distribution"},
        {"element_type": "code", "element_caption": "Code example to sample a gaussian distribution"}
    ],
    "Gaussian Processes": [
        {"element_type": "enumeration", "element_caption": "Introduction to Gaussian processes"},
        {"element_type": "class-diagram", "element_caption": "Class Diagram showing relationship between different Gaussian Processes"}
    ],
    "Challenges and Limitations of Gaussian Models": [
        {"element_type": "description", "element_caption": "Discussion on the limitations and challenges of using Gaussian models"},
        {"element_type": "enumeration", "element_caption": "List of common issues and scenarios where Gaussian models may fail"}
    ],
    "Summary and Conclusions": [
        {"element_type": "enumeration", "element_caption": "Recap of key points covered in the presentation"},
    ]
}
"""}
]
instruction_prompt = ("human", """Hello. I want you to help me prepare lecture slides on {topic}. I am providing you with the outline of the lecture in form of a nested dictionary.\n
                 Outline :{outline}
                 Each element in the object is a slide where the value represent the slide title. I want you to add two keys namely 'element_type' and 'element_caption' for each subsection and determine which types of elements would be most beneficial to understand that subsection.\n
                 The elements can be as follows: {elements}.\n
                 You should generate exactly two elements per slide. Do not generate more of less elements per slide.\n
                 Whenever possible generate atleast one text based element (Description, URL, or Enumeration) and one visual element (Rest of the elements) per subsection, such that there is diversity in elements.\n
                 As a rule of thumb, make sure the distribution of elements is nearly same for the entire presentation, but also that enumeration dominates overall given it's the most imporatant element.\n 
                 I want you to generate the results within the outline and only output the revised outline without any conversation.\n
                 Do not generate the slide numbers in the output, they are just for your reference.
                 Your output should be in form of a Python Dict.
                 """)



instruction_example_prompt = [
                ("human", """Hello. I want you to help me prepare lecture slides on {topic}. I am providing you with the outline of the lecture in form of a nested dictionary.\n
                 Outline :{outline}
                 Each element in the object is a slide where the value represent the slide title. I want you to add two keys namely 'element_type' and 'element_caption' for each subsection and determine which types of elements would be most beneficial to understand that subsection.\n
                 The elements can be as follows: {elements}.\n
                 You should provide one or two elements per slide.\n
                 Whenever possible generate atleast one text based element (Description, URL, or Enumeration) and one visual element (Rest of the elements) per subsection, such that there is diversity in elements.\n
                 As a rule of thumb, make sure the distribution of elements is nearly same for the entire presentation, but also that enumeration dominates overall given it's the most imporatant element.\n 
                 And prefer suggesting more enumerations and urls in text content as they are easier to understand in a presentation.\n
                 I want you to generate the results within the outline and only output the revised outline without any conversation.\n
                 Your output should be in form of a Python Dict.
                 """),
                 ("ai", "{output}")
            ]

text_generation_example = [
    {
        "instructions": """{
"Introduction to Trees": [
        {"element_type": "description", "element_caption": "Introduction to the three probability axioms"},
        {"element_type": "url", "element_caption": "A link to a resource to learn more about trees"}
],
"Types of Tree Data Structures": [
        {"element_type": "enumeration", "element_caption": "A list of common types of tree data structures"},
        {"element_type": "class-diagram", "element_caption": "A class diagram showing relationship between different tree data types"}
],
"Basic Terminology in trees": [
        {"element_type": "enumeration", "element_caption": "Descriptive explaination of a terminologies for a tree data structure"},
],
"Tree Traversals": [
        {"element_type": "enumeration", "element_caption": "A list naming types of tree traversal techniques"},
        {"element_type": "table", "element_caption": "A detailed comparitive table between characteristics of different tree traversals"}
],
"Applications of Trees": [
        {"element_type": "enumeration", "element_caption": "A detailed enumeration highlighting areas where trees are applied"}
]
}
        """,
        "topic": "Tree Data Structure",
        "presentation_ID": 12451,
        "subject": "CS",
        "output": """
{
"presentation_ID": 12451,
"subject": 'CS'
"topic": Tree Data Structure,
"slides":[
      {
         "slide_number": 1,
         "title": "Introduction to Trees",
         "description": "Trees are hierarchical data structures consisting of nodes connected by edges. They contain a root node, branches, and leaves. Each node can have zero or more children, forming a tree-like structure. Trees are widely used in computer science for organizing and managing data efficiently.",
         "enumeration": [[]],
         "url": "https://www.w3schools.com/dsa/dsa_theory_trees.php"
      },
      {
         "slide_number": 2,
         "title": "Types of Tree Data Structures",
         "description": "",
         "enumeration": [["Types of Trees", 
                        "Binary Tree",
                        "Binary Search Tree (BST)",
                        "AVL Tree",
                        "Red-Black Tree",
                        ]],
        "url": ""
      },
      {
         "slide_number": 3,
         "title": "Basic Terminology of trees",
         "description": "Binary trees: Data structures composed of nodes where each node has at most two children, commonly referred to as the left child and the right child.",
         "enumeration": [[
         "Root Node :- The root node is the topmost node in the tree hierarchy. In other words, the root node is the one which doesn't have any parent.",
         "Sub Tree :- If the root node is not null, the tree T1, T2 and T3 is called sub-trees of the root node.",
         "Leaf Node :- The node of tree, which doesn't have any child node, is called leaf node. Leaf node is the bottom most node of the tree. There can be any number of leaf nodes present in a general tree. Leaf nodes can also be called external nodes.",
         "Path :- The sequence of consecutive edges is called path. In the tree shown in the above image, path to the node E is A-> B -> E."
         ]],
         "url": ""
      },
      {
         "slide_number": 4,
         "title": "Tree Traversals",
         "description": "",
         "enumeration": [["Three types of Traversals", "Inorder", "Preorder", "Postorder"]],
         "url": ""
      },
      {
         "slide_number": 5,
         "title": "Application of Trees",
         "description": "",
         "enumeration": [["Various applications", "File Systems: Representing the structure of directories and files in operating systems.",
           "Network Routing: Used in routing algorithms such as OSPF and BGP",
           "Syntax Tree: Representing the structure of program code in compilers and interpreters for parsing and analysis."]],
         "url": ""
      }
      ]
}
        """
    }
]

tbl_var_prompt = [("system", "You are a helpful code assistant. You have access to internet resources."),
                            ("human", """
I am providing some instructions to modify a LaTeX table.
Given the inital latex code, modify it such that:
1. The table should have {BACKGROUND} background. 
2. The font size should be {FONT_SIZE} points, font color should be {FONT_COLOR}
3. The table should have {BORDERS}.\n

Do not add any additional tags like documents and packages. (Assume they already exist). Also do not provide any conversation. Just the output.\n
The original latex code is as follows:\n
{input}
\n      
""")]
text_generation_ex_prompt = [
                ("human", """I am providing you with some instructions given to generate content for a presentation on {topic} of the subject {subject}\n
The instructions have Slide Title as key and the value is a list of object describing what text/visual elements are required to explain that concept\n
I want you to focus on generating the actual content for only the text elements, i.e. description, enumeration, and url.\n
Following are the instructions:\n
{instructions}\n
While generating content keep the following in mind:\n
1. Description should be between 15 to 30 words long and be rendered as a string.\n
2. Enumeration should have short pithy points related to the slide content. It should be rendered as a list of strings where the first element of the list is the heading of the enumeration.\n
3. URL should be a weblink to a related resource in the web and it should be rendered as a string\n

Enumeration should not have more than 5 points.
For a particular slide if there is just one element which is a text element, then generate more content for it compared to when there are other elements along with that element.      
                 
Do not generate additional text elements other than one mentioned in the instruction. Keep your responses as detailed as possible.\n
        """),
                 ("ai", "{output}")
            ]



def construct_generation_prompts(instruct_content, topic):
    prompts = [f"I am providing some instructions which are related to generating structural content for a presentation like tables and equations on {topic}.\n"
               , f"I am providing some instructions which are related to generating plots for a presentation on {topic}.\n"
               , f"I am providing some instructions which are related to generating diagrams and figures for a presentation on {topic}.\n"
               , f"I am providing some instructions which are related to generating code for a particular example being discuseed in a presentation on {topic}.\n"]
    # prompts -> ['text', 'structural (LaTeX)', 'plots (Matplotlib)', 'figures (DOT + GraphViz)']
    positions = [{
                  "tables": {},
                  "equations": {}   
                 },
                 {
                  "plot": {},
                  "bar-chart": {},
                  "line-chart": {},
                  "pie-chart": {},
                  "3d-plot": {}
                 },
                 {
                    "architecture-diagram": {},
                    "class-diagram": {},
                    "flow-chart": {},
                    "sequence-diagram": {} 
                 },
                 {
                     "code": {}
                 }]
    
    captions = [{
                  "tables": {},
                  "equations": {}   
                 },
                 {
                  "plot": {},
                  "bar-chart": {},
                  "line-chart": {},
                  "pie-chart": {},
                  "3d-plot": {}
                 },
                 {
                    "architecture-diagram": {},
                    "class-diagram": {},
                    "flow-chart": {},
                    "sequence-diagram": {} 
                 },
                 {
                     "code": {}
                 }]


    i = 0
    n_s = 0
    n_p = 0
    n_f = 0
    n_c = 0
    for slide, elements in instruct_content.items():
        for element in elements:
            context_line = f"For the section title '{slide}'(Slide Number {i+1})"
            element_type = element["element_type"]
            element_caption = element["element_caption"]
            if element_type in ["table", "equation"]:
                n_s += 1
                element_type += 's'
                positions[0][element_type][n_s] = i + 1
                captions[0][element_type][n_s] = element_caption
                prompts[0] += (context_line + f" generate LaTeX code for a simple {element_type} given the caption: {element_caption}.\n")
                # if element_type == 'table':
                #     prompts[0] += f"You will have to generate the content that goes into the table and the table should have {COLUMNS} columns and {ROWS} rows with {BACKGROUND} background. For the text inside the table, the font size should be {FONT_SIZE} points, font color should be {FONT_COLOR} and the table itself should have {BORDERS}."
            elif element_type in ["plot", "bar-chart", "line-chart", "pie-chart", "3d-plot"]:
                n_p += 1
                positions[1][element_type][n_p] = i + 1
                captions[1][element_type][n_p] = element_caption
                prompts[1] += (context_line + f" generate Matplotlib code for a simple {element_type} given the caption: {element_caption}\n")
            elif element_type in ['flow-chart', 'architecture-diagram', 'class-diagram', 'sequence-diagram']:
                n_f += 1
                positions[2][element_type][n_f] = i + 1
                captions[2][element_type][n_f] = element_caption
                prompts[2] += (context_line + f" generate DOT language code for a simple {element_type} given the caption: {element_caption}. Refer the internet to understand the structure of the diagram and color-code it properly using vibrant colors and shapes.\n")
            elif element_type in ["code"]:
                LANGUAGE = pick_random('prog_langs')
                n_c += 1
                positions[3][element_type][n_c] = i + 1
                captions[3][element_type][n_c] = element_caption
                prompts[3] += (context_line + f"generate {LANGUAGE} language code for: {element_caption}. Do not provide any input and output examples in the code. Just the basic code function. Do not provide more than 20 lines of code in any case.")
        i+=1
                
  
    prompts[0] += """
    Generate LaTeX code as plain text seperated by ```latex<content>``` and three line breaks.\n
    Do not add a caption to the table/equation and do not provide any conversation.\n
    For equations do not generate equation numbers like (1) as these are single equations to be rendered in a presentation.\n
    Keep the following in mind:\n
    Verify the syntax of the LaTeX code that you generate.\n
    Do not generate additional elements unless they are part of the above request. Once generating the all the code snipptes, verify that the total number of snippets generated are the same as total number of requests."""
    prompts[1] += """
    Generate python code using Matplotlib as plain text seperated by ```python<content>``` and three line breaks.\n
    Each generated plot shoule be saved to 'code/buffer/figures/<num>.png' where <num> is numerical order of the code snippet. (First snippet is 1, Second is 2, etc.)\n
    Keep the following in mind:\n
    Verify the syntax of the matplotlib code that you generate and do not import additional libraries.\n
    Do not generate a title for the plot and do not give any conversation.\n
    Do not generate additional elements unless they are part of the above request. Once generating the all the code snipptes, verify that the total number of snippets generated are the same as total number of requests."""
    prompts[2] += """
    Generate DOT language code as plain text seperated by ```dot<content>``` and three line breaks. Make sure to not make any syntax errors, and hence double check each output code snippet.\n
    Keep the following in mind:\n
    Verify the syntax of the DOT Language code that you generate.\n
    Strictly DO NOT add any textual caption in the figure. It should be a figure with no caption at the bottom. And do not provide any conversation.\n
    Do not generate additional elements unless they are part of the above request. Once generating the all the code snipptes, verify that the total number of snippets generated are the same as total number of requests."""
    prompts[3] += """
    Generate code as plain text seperated by ```code<content>``` and three line breaks. Make sure to not make any syntax errors, and hence double check each output code snippet.\n
    Keep the following in mind:\n
    Do not generate additional elements unless they are part of the above request. Once generating the all the code snipptes, verify that the total number of snippets generated are the same as total number of requests."""
    # Return the constructed prompts
    return [prompts, positions, captions, [n_s, n_p, n_f, n_c]]
