import random
from datetime import datetime

FONT_STYLES = [
    "Arial",
    "Calibri",
    "Times New Roman",
    "Verdana",
    "Georgia",
    "Tahoma",
    "Garamond",
    "Trebuchet MS",
    "Gill Sans MT",
    "Century Gothic",
    "Palatino Linotype",
    "Cambria",
    "Franklin Gothic Book",
    "Lucida Sans"
]

TITLE_COLORS_DARK = [
    {"r": 0, "g": 0, "b": 128},    # Navy Blue
    {"r": 220, "g": 20, "b": 60},   # Crimson
    {"r": 0, "g": 128, "b": 0},     # Emerald Green
    {"r": 218, "g": 165, "b": 32},  # Goldenrod
    {"r": 75, "g": 0, "b": 130},    # Royal Purple
    {"r": 0, "g": 128, "b": 128},   # Teal
    {"r": 204, "g": 85, "b": 0},    # Burnt Orange
    {"r": 128, "g": 0, "b": 32},    # Burgundy
    {"r": 112, "g": 128, "b": 144}, # Slate Gray
    {"r": 255, "g": 0, "b": 255}    # Magenta
]
TITLE_COLORS_LIGHT = [
    {"r": 255, "g": 215, "b": 0},     # Gold
    {"r": 255, "g": 69, "b": 0},       # Orange-Red
    {"r": 65, "g": 105, "b": 225},     # Royal Blue
    {"r": 0, "g": 206, "b": 209},      # Turquoise
    {"r": 255, "g": 165, "b": 0},      # Orange
    {"r": 255, "g": 140, "b": 0},      # Dark Orange
    {"r": 255, "g": 20, "b": 147},     # Deep Pink
    {"r": 128, "g": 0, "b": 128},      # Purple
    {"r": 255, "g": 69, "b": 0},       # Red-Orange
    {"r": 255, "g": 192, "b": 203}     # Pink
]

H_ALIGNMENTS = [
    'left',
    'center',
    'right',
    'justify'
]

V_ALIGNMENTS = [
    'top',
    'middle',
    'bottom'
]
DAYS = list(range(1, 28))
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
YEARS = list(range(2014, 2024))

ABBR_MONTHS = [
    "Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.",
    "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."
]

PRESENTERS = [
    "Dr. Marcella Nguyen",
    "Prof. Benjamin Frost",
    "Dr. Isabella Patel",
    "Prof. Nathanial Lawson",
    "Dr. Lydia Chen",
    "Prof. Winston Harper",
    "Dr. Gabrielle Santiago",
    "Prof. Marcus Sinclair",
    "Dr. Elena Petrov",
    "Prof. Desmond Washington",
    "Dr. Sophia Alvarez",
    "Prof. Samuel Fitzgerald",
    "Dr. Emily Roberts",
    "Prof. Xavier Lee",
    "Dr. Fiona O'Malley",
    "Prof. Harrison Grant",
    "Dr. Vivian Chang",
    "Prof. Gregory Jensen",
    "Dr. Jasmine Khan",
    "Prof. Oliver Martin"
]


def generate_random_color(PROB=0.6):
    if random.random() > PROB:
        return {"r": random.randint(0, 255), "g": random.randint(0, 255), "b": random.randint(0, 255)}
    else:
        return {"r": 255, "g": 255, "b": 255}   

def generate_random_font(element):
    bold = False
    underline = False
    italics = False
    if element == "title":
        font_size = random.randint(16, 28) * 2
    elif element == "description":
        font_size = random.randint(18, 28)
    elif element == 'enumeration':
        font_size = random.randint(22, 32)
    elif element == 'url':
        font_size = random.randint(12, 18)
    return {
        "font_size": font_size,
        "bold": bold,
        "underline": underline,
        "italics": italics
    }

def generate_random_value(type, lb, ub):
    if type == int:
        return random.randint(lb, ub)
    elif type == float:
        return random.uniform(lb, ub)

def pick_random_presenter():
    return pick_random(PRESENTERS)

def generate_random_date():
    day = random.choice(DAYS)
    month = random.choice(MONTHS)
    abbrev_month = ABBR_MONTHS[MONTHS.index(month)]
    year = random.choice(YEARS)
    
    formats = [
        f"{day} {month} {year}",
        f"{day} {abbrev_month} {year}",
        f"{month} {day}th",
        f"{abbrev_month} {day}th",
        f"{day}th {month}",
        f"{day}th {abbrev_month}",
        f"{month} {year}"
        f"{abbrev_month} {year}",
        f"Spring {year}",
        f"Fall {year}"
    ]
    
    return random.choice(formats)

def generate_footer_obj():
    showSN = random.random() > 0.25
    showDt = random.random() > 0.5
    showFN = random.random() > 0.75 
    total_footer_elements = 0
    if showSN:
        total_footer_elements += 1
    if showDt:
        total_footer_elements += 1
    if showFN:
        total_footer_elements += 1
    inds = random.sample(range(3), total_footer_elements)
    i = 0
    footer_inds = []
    if showSN:
        footer_inds.append({"slideNr": inds[i]})
        i+=1
    if showDt:
        footer_inds.append({"date": inds[i]})
        i+=1
    if showFN:
        footer_inds.append({"footnote": inds[i]})
        i+=1
    return footer_inds


    
def generate_random_style_obj():
    style_obj = {}
    style_obj["bg_color"] = generate_random_color(0.6)
    style_obj["title_font_family"] = pick_random(FONT_STYLES) 
    style_obj["title_font_bold"] = random.random() > 0.75
    style_obj["title_font_attr"] = generate_random_font("title")
    style_obj["title_align"] = 'center' if random.random() > 0.33 else 'left'
    style_obj['title_font_dark'] = pick_random(TITLE_COLORS_DARK)
    style_obj['title_font_light'] = pick_random(TITLE_COLORS_LIGHT)
    style_obj["desc_font_family"] = pick_random(FONT_STYLES)
    style_obj["desc_font_attr"] = generate_random_font("description")
    style_obj["date"] = generate_random_date()
    return style_obj

def pick_random(list_name):
    if list_name == 'alignments':
        return [random.choice(H_ALIGNMENTS), random.choice(V_ALIGNMENTS)]
    else:
        return random.choice(list_name)

def generate_random_layout(total_body_elements):
    layout_mapping = {
        0: [0],
        1: [1], 
        2: [2, 3],
        3: [4, 5, 6, 7, 8]
        }
    return random.choice(layout_mapping[total_body_elements])

def generate_n_numbers_with_sum(sum_value, n):
    numbers = [0] * n
    for i in range(n-1):
        numbers[i] = random.randint(0, sum_value - sum(numbers))

    numbers[-1] = sum_value - sum(numbers[:-1])
    return numbers

def calculate_relative_luminance(color):
    """
    Calculate the relative luminance of a color.
    Input: color - a dictionary with 'r', 'g', 'b' keys representing RGB values.
    Output: float - relative luminance value.
    """
    r, g, b = color['r'], color['g'], color['b']
    # Convert RGB values to sRGB
    r_srgb = r / 255.0
    g_srgb = g / 255.0
    b_srgb = b / 255.0
    
    # Calculate relative luminance
    luminance = 0.2126 * r_srgb + 0.7152 * g_srgb + 0.0722 * b_srgb
    return luminance

def generate_contrasting_font_color(bg_color, title_dark, title_light):
    """
    Generate a contrasting font color for a given background color.
    Input: bg_color - a dictionary with 'r', 'g', 'b' keys representing RGB values.
    Output: dictionary - a dictionary with 'r', 'g', 'b' keys representing RGB values of the font color.
    """
    luminance = calculate_relative_luminance(bg_color)
    
    # Choose a contrasting color based on the luminance
    if luminance > 0.5:
        # Background is light, use dark font color
        font_color = {"r": 0, "g": 0, "b": 0} # Black
        title_font = title_dark
    else:
        # Background is dark, use light font color
        font_color = {"r": 255, "g": 255, "b": 255} # White
        title_font = title_light
        
    return title_font, font_color

