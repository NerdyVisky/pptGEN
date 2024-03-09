
class CustomLayouts:
    def __init__(self):
        self.dimensions = {'title' : {'left': 0.5, 'top': 0.3, 'width': 9, 'height': 1.25}}
    
    def get_layout_dimensions(self, layout_id):
        match layout_id:

            ## Only Title
            case 0:
                pass
            ## Title and One Big Element
            case 1:
                self.dimensions['body'] = [{'left': 0.5, 'top': 2, 'width': 9, 'height': 5}] 
            ## Title and two elements in two-column format
            case 2:
                self.dimensions['body'] = [{'left': 0.5, 'top': 2, 'width': 4.5, 'height': 4}, {'left': 5   , 'top': 2, 'width': 4.5, 'height': 4}]
            ## Title and two elements in two-row format
            case 3:
                self.dimensions['body'] = [{'left': 0.5, 'top': 2, 'width': 9, 'height': 2.5}, {'left': 0.5, 'top': 4.5, 'width': 4.5, 'height': 2.5}] 
            # Layout Error Default
            case _:
                raise Exception("Layout Definition Error : No layout defined")

        return self.dimensions 
