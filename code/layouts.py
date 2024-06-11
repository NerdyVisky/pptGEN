import random
MUL_FAC = 1.333
class CustomLayouts:
    def __init__(self):
        self.dimensions = {'title' : {'type': 1, 'left': 1, 'top': 0.3, 'width': 8*MUL_FAC, 'height': 1.25},
                           'footer': [{'type' : 1, 'left': 0.5 , 'top': 7, 'width': 3*MUL_FAC, 'height': 0.5}, {'type' : 2, 'left': 3.5*MUL_FAC, 'top': 7, 'width': 3*MUL_FAC, 'height': 0.5}, {'type' : 3, 'left': 6.5*MUL_FAC, 'top': 7, 'width': 3*MUL_FAC, 'height': 0.5}],
                           'topic_slide': [
    {
        "left": 0,
        "top": 0,
        "width": 6.6665,
        "height": 3.75
    },
    {
        "left": 0,
        "top": 3.75,
        "width": 6.6665,
        "height": 3.75
    },
    {
        "left": 6.6665,
        "top": 0,
        "width": 6.6665,
        "height": 2.5
    },
    {
        "left": 6.6665,
        "top": 2.5,
        "width": 6.6665,
        "height": 2.5
    },
    {
        "left": 6.6665,
        "top": 5,
        "width": 6.6665,
        "height": 2.5
    }

]
        }
    
    def get_layout_dimensions(self, layout_id):
        match layout_id:

            ## Only Title
            case 0:
                self.dimensions['title'] = {'type': 0, 'left': 0.5 , 'top': 2, 'width': 9*MUL_FAC, 'height': 1.25}
            ## No Title and One Big Element
            case 1:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type': 0,  'left': 0.5 , 'top': 0.5, 'width': 9*MUL_FAC, 'height': 6.5}]
            ## Title and One Big Element
            case 2:
                self.dimensions['body'] = [{'type': 0,  'left': 0.5 , 'top': 2, 'width': 9*MUL_FAC, 'height': 5}] 
            ## No Title and Two-column Elements
            case 3:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type': 1, 'left': 0.5 , 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 6.5}, {'type': 1, 'left': 5*MUL_FAC, 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 6.5}]
            ## Title and Two-column Elements
            case 4:
                self.dimensions['body'] = [{'type': 1, 'left': 0.5 , 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}, {'type': 1, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}]
            ## No title and Two-row elements
            case 5:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type' : 2, 'left': 0.5 , 'top': 0.5, 'width': 9*MUL_FAC, 'height': 3.25}, {'type' : 2, 'left': 0.5 , 'top': 3.75, 'width': 9*MUL_FAC, 'height': 3.25}] 
            ## Title and Two-row elements
            case 6:
                self.dimensions['body'] = [{'type' : 2, 'left': 0.5 , 'top': 2, 'width': 9*MUL_FAC, 'height': 2.5}, {'type' : 2, 'left': 0.5 , 'top': 4.5, 'width': 9*MUL_FAC, 'height': 2.5}] 
            ## No title and three column elements
            case 7:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type' : 3, 'left': 0.5 , 'top': 0.5, 'width': 3*MUL_FAC, 'height': 6.5}, {'type' : 3, 'left': 3.5*MUL_FAC, 'top': 0.5, 'width': 3*MUL_FAC, 'height': 6.5}, {'type' : 3, 'left': 6.5*MUL_FAC, 'top': 0.5, 'width': 3*MUL_FAC, 'height': 6.5}]
            case 8:
                self.dimensions['body'] = [{'type' : 3, 'left': 0.5 , 'top': 2, 'width': 3*MUL_FAC, 'height': 5}, {'type' : 3, 'left': 3.5*MUL_FAC, 'top': 2, 'width': 3*MUL_FAC, 'height': 5}, {'type' : 3, 'left': 6.5*MUL_FAC, 'top': 2, 'width': 3*MUL_FAC, 'height': 5}]
            case 9:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type': 1, 'left': 0.5 , 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 6.5}, {'type': 4, 'left': 5*MUL_FAC, 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 3.25}, {'type': 4, 'left': 5*MUL_FAC, 'top': 3.75, 'width': 4.5*MUL_FAC, 'height': 3.25}]
            case 10: 
                self.dimensions['body'] = [{'type': 1, 'left': 0.5 , 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}, {'type': 4, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type': 4, 'left': 5*MUL_FAC, 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}]
            case 11:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type': 4, 'left': 0.5 , 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 3.25}, {'type': 4, 'left': 0.5 , 'top': 3.75, 'width': 4.5*MUL_FAC, 'height': 3.25}, {'type': 1, 'left': 5*MUL_FAC, 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 6.5}]
            case 12:
                self.dimensions['body'] = [{'type': 4, 'left': 0.5 , 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type': 4, 'left': 0.5 , 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type': 1, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 5}]
            case 13:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5 , 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 3.25}, {'type' : 4, 'left': 5*MUL_FAC, 'top': 0.5, 'width': 4.5*MUL_FAC, 'height': 3.25}, {'type' : 2, 'left': 0.5 , 'top': 3.75, 'width': 9*MUL_FAC, 'height': 3.25}]
            case 14:
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5 , 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 4, 'left': 5*MUL_FAC, 'top': 2, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 2, 'left': 0.5 , 'top': 4.5, 'width': 9*MUL_FAC, 'height': 2.5}]
            case 15:
                self.dimensions['title'] = {}
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5 , 'top': 3.75, 'width': 4.5*MUL_FAC, 'height': 3.25}, {'type' : 4, 'left': 5*MUL_FAC, 'top': 3.75, 'width': 4.5*MUL_FAC, 'height': 3.25}, {'type' : 2, 'left': 0.5 , 'top': 0.5, 'width': 9*MUL_FAC, 'height': 3.25}] 
            case 16:
                self.dimensions['body'] = [{'type' : 4, 'left': 0.5 , 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 4, 'left': 5*MUL_FAC, 'top': 4.5, 'width': 4.5*MUL_FAC, 'height': 2.5}, {'type' : 2, 'left': 0.5 , 'top': 2, 'width': 9*MUL_FAC, 'height': 2.5}] 
            # Layout Error Default
            case _:
                raise Exception("Layout Definition Error : No layout defined")
        return self.dimensions
