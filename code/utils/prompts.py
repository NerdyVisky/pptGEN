outline_prompt = [
            ("system", "You are a helpful university professor and you are guiding your PhD student to create an outline for the lecture he will deliver to a class."),
            ("human", "Hello professor, I would like to get help designing a detailed Table of Contents for an advanced university lecture on {topic}. Please help me create the Table of Content form of a {format}. Just return the output without the conversation.")
        ]

instruction_prompt = [
                ("system", "You are a helpful undergraduate student at the university. Your job is to provide suggestions to the lecturer on the lecture slides for the topic of {topic}"),
                ("human", """Hello. I want you to help me prepare lecture slides on {topic}. I am providing you with the outline of the lecture in form of a nested dictionary.\n
                 Outline :{outline}
                 Each subsection has empty values. I want you to add two keys namely 'element_type' and 'element_caption' for each subsection and determine which types of elements would be most beneficial to understand that subsection.\n
                 The elements can be as follows: {elements}.\n
                 An example can be:
                 Topic: Djisktra's Algorithm.\n
                 Section: Implementing Djisktra's algorithm.\n
                 Subsection: Edge Relaxation\n
                 \n
                 Expected Output:\n 
                 [\n
                 {{"element_type: "description", "element_caption": "Defining what Relaxing a node" }}
                 {{"element_type": "graph", "element_caption": "The graph which represent relaxing a node in Djisktra's algorithm"}},\n,
                 {{"element_type": "equation", "element_caption": "An equation which represents the cost of a relaxed edge mathematically"}},\n
                 {{"element_type": "url", "element_caption": "A weblink to an article explaining relaxation of nodes in detail"}},\n
                 ]\n

                 You can have upto 3 elements per subsection, and I want you to generate the results within the outline and only output the revised outline without any conversation.\n
                 """)
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
                 \t a. For element_type = 'description', you can generate either a paragraph style element named description, or point-wise style element named enumeration.\n
                 \t b. For element_type = 'equation' or 'table' or 'pseudocode', you have to generate LaTex Code depending on the instruction given in element_caption.\n
                 \t c. For element_type = 'chart' or 'graph' or 'diagram', you have to generate an image depending on the instruction given in element_caption and provide the link to the image path\n

                 The presentation content should be generated in form of a JSON object. The presentation ID is {presentation_ID}

                 """)
            ]