import re
import plotly.graph_objects as go
import plotly.express as px

def get_sentence(text, index):
    sentence = text[max(0, text.rfind('.', 0, index)) + 1 : text.find('.', index) + 1].strip()
    return sentence

def get_paragraph(text, index):
    start_index = text.rfind('\n\n', 0, index) + 1
    if start_index == 0:
        start_index = text.rfind('\n\n', 0, index) + 2
    end_index = text.find('\n\n', index)
    if end_index == -1:
        end_index = text.find('\n\n', index)
    if end_index == -1:
        end_index = len(text)
    paragraph = text[start_index : end_index].strip()
    return paragraph

def add_line_breaks(text, max_line_length):
    words = text.split(' ')
    lines = ['']
    for word in words:
        if len(lines[-1]) + len(word) + 1 > max_line_length:
            lines.append(word)
        else:
            lines[-1] += ' ' + word
    return '<br>'.join(lines)

# Or?
# def get_paragraph(text, index):
#     start_index = text.rfind('\n\n', 0, index)
#     if start_index == -1:
#         start_index = 0
#     else:
#         start_index += 2  # Skip past the "\n\n"
#
#     end_index = text.find('\n\n', index)
#     if end_index == -1:
#         end_index = len(text)
#     else:
#         end_index += 1  # Include the first "\n" in the paragraph
#
#     paragraph = text[start_index: end_index].strip()
#     return paragraph

fig = go.Figure()

# with open(r"C:\PythonProjects\BibleViz\nt_bible_clean.txt", "r") as file:
#     text = file.read()

characters = ["Jesus", "Christ", "Peter", "Paul",
              'OBAMA', 'blessed are the', 'love thy neighbour', "John the Baptist", "John",  "Mary Magdalene",  "Judas Iscariot", 'Judas', "Pilate", "Matthew", "Mark", "Luke", "James", "Thomas", "Satan"]
# characters = ["ogybogy"]



colors = px.colors.qualitative.Plotly

chapters = [
    'The Gospel According to Saint Matthew',
    'The Gospel According to Saint Mark',
    'The Gospel According to Saint Luke',
    'The Gospel According to Saint John',
    'The Acts of the Apostles',
    'The Epistle of Paul the Apostle to the Romans',
    'The First Epistle of Paul the Apostle to the Corinthians',
    'The Second Epistle of Paul the Apostle to the Corinthians',
    'The Epistle of Paul the Apostle to the Galatians',
    'The Epistle of Paul the Apostle to the Ephesians',
    'The Epistle of Paul the Apostle to the Philippians',
    'The Epistle of Paul the Apostle to the Colossians',
    'The First Epistle of Paul the Apostle to the Thessalonians',
    'The Second Epistle of Paul the Apostle to the Thessalonians',
    'The First Epistle of Paul the Apostle to Timothy',
    'The Second Epistle of Paul the Apostle to Timothy',
    'The Epistle of Paul the Apostle to Titus',
    'The Epistle of Paul the Apostle to Philemon',
    'The Epistle of Paul the Apostle to the Hebrews',
    'The General Epistle of James',
    'The First Epistle General of Peter',
    'The Second General Epistle of Peter',
    'The First Epistle General of John',
    'The Second Epistle General of John',
    'The Third Epistle General of John',
    'The General Epistle of Jude',
    'The Revelation of Saint John the Divine'
]
# Calculate the new total length of the text
total_length = len(text)

character_positions = {character: [] for character in characters}
for character in characters:
    if character == "Peter":
        # If the character is "Peter", also search for "Simon"
        character_positions[character] = [m.start() for m in re.finditer(rf"\b{'Peter'}\b|\b{'Simon'}\b", text, re.IGNORECASE)]
    elif character == "Mary Magdalene":
        # If the character is "Mary Magdalene", only match "Mary Magdalene", not "Mary"
        character_positions[character] = [m.start() for m in re.finditer(rf"\b{character}\b", text, re.IGNORECASE)]
        # Remove the mentions of "Mary Magdalene" from "Mary"
        character_positions["Mary"] = [pos for pos in character_positions["Mary"] if pos not in character_positions["Mary Magdalene"]]
    elif character == "John the Baptist":
        # If the character is "John the Baptist", only match "John the Baptist", not "John"
        character_positions[character] = [m.start() for m in re.finditer(rf"\b{character}\b", text, re.IGNORECASE)]
        # Remove the mentions of "John the Baptist" from "John"
        character_positions["John"] = [pos for pos in character_positions["John"] if pos not in character_positions["John the Baptist"]]
    elif character == "Judas Iscariot":
        # If the character is "Judas Iscariot", only match "Judas Iscariot", not "Judas"
        character_positions[character] = [m.start() for m in re.finditer(rf"\b{character}\b", text, re.IGNORECASE)]
        # Remove the mentions of "Judas Iscariot" from "Judas"
        character_positions["Judas"] = [pos for pos in character_positions["Judas"] if
                                       pos not in character_positions["Judas Iscariot"]]
    else:
        character_positions[character] = [m.start() for m in re.finditer(rf"\b{character}\b", text, re.IGNORECASE)]

chapter_positions = {chapter: text.find(chapter) / total_length * 100 for chapter in chapters}

chapter_names = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '', '', '', 'The Epistles', '', '', '', '', '', '', '', '', 'Hebrews', '', '', '', '', '', '', '', 'Revelations']

# chapter_xs = tuple(value/100 for value in chapter_positions.values())


chapter_xs = tuple(chapter_positions.values())




# This was changed and actually worked! #shownnobody
for spot, character in enumerate(characters):
    indices = character_positions[character]
    sentences = []
    paragraphs = []
    for i in indices:
        # sentences.append(get_sentence(text, i))
        paragraphs.append(get_paragraph(text,i))
    paragraphs = [add_line_breaks(paragraph, 80) for paragraph in paragraphs]  # Adjust 80 to control line length
    percentages = [100 * i / len(text) for i in indices]
    fig.add_trace(go.Scatter(x=percentages, y=[character]*len(indices), mode='markers', name=character, text=paragraphs,
                             hovertemplate="%{text}<extra></extra>", marker=dict(color=colors[spot % len(colors)])))

# This if/else string is NOT WHAT what made show nobody work, you just needed the y-dict categoryorder=array, categoryarray=characters arguments
#     if len(indices) == 0:
#         fig.add_trace(go.Scatter(x=[], y=[character for _ in range(1)], mode='markers', name=character, text=sentences, hovertemplate="%{text}<extra></extra>", marker=dict(color=colors[spot % len(colors)])))
#     else:
#         fig.add_trace(go.Scatter(x=percentages, y=[character]*len(indices), mode='markers', name=character, text=sentences, hovertemplate="%{text}<extra></extra>", marker=dict(color=colors[spot % len(colors)])))

firstcolor = "mediumseagreen"
secondcolor = "peachpuff"
for i in range(len(chapters) - 1):
    fig.add_shape(type="rect", xref="x", yref="paper", x0=chapter_xs[i], y0=0, x1=chapter_xs[i + 1], y1=1, fillcolor=firstcolor if i % 2 == 0 else secondcolor, opacity=0.25, line_width=0)

# Color in the last book, Revelations, independently:
fig.add_shape(type="rect", xref="x", yref="paper", x0=chapter_xs[26], y0=0, x1=100, y1=1,
              fillcolor=firstcolor, opacity=0.25, line_width=0)

# Instead of adding lines and annotations seperately, we can:
# for i in range(len(chapter_names)):
#     fig.add_annotation(x=chapter_xs[i], y=1.05, yref="paper", text=chapter_names[i], showarrow=False)

# Add line and chapter names in one for loop:
for i in range(len(chapter_names)):
    fig.add_shape(type="line", xref="x", yref="paper",
        x0=chapter_xs[i], y0=0, x1=chapter_xs[i], y1=1,
        line=dict(color="peru", width=1.5),
    )
    fig.add_annotation(x=chapter_xs[i], y=1.05, yref="paper", text=chapter_names[i], showarrow=False,
                       font=dict(color='peru'))

fig.update_layout(
    title={
        'text': "Mentions of Each Entry Throughout the Bible",
        'x': 0.5,
        'xanchor': 'center',
        'font': dict(color='maroon')
    },
    titlefont=dict(color='maroon'),
    showlegend=False,
    xaxis_title="Position in Bible (%)",
    xaxis_color='maroon',
    yaxis_title="Being",
    yaxis_color='maroon',
    hoverlabel=dict(font_size=16),
    hovermode="closest",

# This was changed and actually worked! #shownnobody
    yaxis=dict(
        tickmode='array',
        tickvals=characters,
        ticktext=characters,
    # The next two lines are actually the only thing you need, that earlier if/else statement is unnecessary.
        categoryorder='array',
        categoryarray=characters[::-1]
    ),
    xaxis=dict(
        range=[0, 100],  # set the x-axis range to match your data
    ),
    autosize=True,  # disable autosizing
    margin=dict(
        l=50,  # left margin
        r=50,  # right margin
        b=100,  # bottom margin
        t=100,  # top margin
        pad=0  # padding
    ),
)
fig.update_layout(
    yaxis=dict(
        tickfont=dict(
            color='maroon'
        )
    )
)
fig.show()

