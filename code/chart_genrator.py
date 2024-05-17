import matplotlib.pyplot as plt

data = {
    "Title": 298,
    "Description": 273,
    "Enumeration": 35,
    "URL": 15,
    "Tables": 24,
    "Equations": 25,
    "Block-diagram": 33,
    "Graph": 58,
    "Flow-chart": 33,
    "Bar-chart": 17,
    "Line-chart": 13,
    "Pie-chart": 11,
    "2D-plot": 26,
    "3D-plot": 3,
    "Tree": 12,
    "SlideNo": 268,
    "Date": 103,
    "Footnote": 59
}

ppts = 20
slides = 298

text_elements = ["Title", "Description", "Enumeration", "URL", "SlideNo", "Date", "Footnote"]
visual_elements = ["Tables", "Equations", "Block-diagram", "Graph", "Flow-chart", "Bar-chart", "Line-chart", "Pie-chart", "2D-plot", "3D-plot", "Tree"]
visual_data = {key: data[key] for key in visual_elements}

# Bar plot for number of elements with color according to classification with legend
plt.figure(figsize=(10, 6))
plt.bar(data.keys(), data.values())
plt.xlabel('Elements')
plt.ylabel('Number of Elements')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# # 4 - Distribution of Visual Elements - Circle plot
# plt.figure(figsize=(10, 6))
# explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
# plt.pie(visual_data.values(), labels=visual_data.keys(), autopct='%1.1f%%', pctdistance=0.85, explode=explode, colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#FF5733'])
# plt.axis('equal')
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# plt.tight_layout()
# plt.show()

# topics = {
#     "Comp Science": 8,
#     "Economics": 4,
#     "Mathematics": 5,
#     "Physics": 3
# }

# # 5 - Distribution of Topics - Donut plot
# plt.figure(figsize=(10, 6)) 
# explode = (0.05, 0.05, 0.05, 0.05)
# plt.pie(topics.values(), labels=topics.keys(), autopct='%1.1f%%', pctdistance=0.85, explode=explode, startangle=90)
# plt.axis('equal')
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# plt.tight_layout()
# plt.show()


#Slides SPaSe (Ours) 2000 14 6 4 ✓