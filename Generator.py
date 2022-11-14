from drawBot import _drawBotDrawingTool as draw
import networkx as nx

# import matplotlib.pyplot as plt
import numpy as np
import string
from itertools import combinations

# return list of all subsets of length r from arr
def rSubset(arr, r):

    # return list of all subsets of length r
    # to deal with duplicate subsets use
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))


# Return a list of edge tuples (ex: (1,2))
# given arr = list of edge keys (ex = A)
def getEdges(arr):
    # return a list of all edge values
    # arr is a tuple of keys in edges
    # uses list comprehension
    return [edges[k] for k in arr]


# Given a path length generate
# Generate all possible graphs (forest) with
# path_len edges in a graph with nodes (global)
def generateGraphs(path_len, forest=False):

    graphs = []
    paths = rSubset(edges, path_len)
    graphs_len = len(paths)
    for i in range(graphs_len):
        # get edge tuple list (A -> (1,2))
        # for each edge key in paths[i]
        lst_of_edges = getEdges(paths[i])
        # create graph
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(lst_of_edges)
        # diferentiate between forest and trees
        if forest and nx.is_forest(G):
            graphs.append(G)
        elif not forest:
            graphs.append(G)

    return graphs


# Draw preatty graph using matplotlib
# Currently broken without positions array dictionary
def drawGraph(g):
    nx.draw(
        G,
        pos=positions,
        with_labels=False,
        node_color="#000000",
        node_size=5200,
        width=75,
        font_weight="bold",
    )


# Draw graph using matplotlib
def drawBareGraph(g):
    nx.draw(G, pos=positions, with_labels=True, width=2, font_weight="bold")


# calculate number of forest
# with between min_edges and max_edges
def calcNumForest(min_edges, max_edges):
    count = 0
    for i in range(min_edges, max_edges + 1):
        all_g = generateGraphs(i, forest=True)
        count = count + len(all_g)
    return count


# Graph Contants
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 1 A 2 B 3
# C   D   E
# 4 F 5 G 6
# H   I   J
# 7 K 8 L 9
edges = {
    "A": (1, 2),
    "B": (2, 3),
    "C": (1, 4),
    "D": (2, 5),
    "E": (3, 6),
    "F": (4, 5),
    "G": (5, 6),
    "H": (4, 7),
    "I": (5, 8),
    "J": (6, 9),
    "K": (7, 8),
    "L": (8, 9),
}
## Edges List format flat (for debugging)
all_edges = np.array(list(edges.values()))

# canvas size
# This varaible is manually modified and caclulated
# This was done to keep the code readable
dimension = 198
# grid cell dimension
diviser = 3
# canvas space division
part = dimension / diviser
# cell division
div = part // 2

# Graph Node Positions for drawBot drawing
# 1 2 3 c
# 4 5 6 b
# 7 8 9 a
# a b c
a = div
b = div + part
c = div + part * 2
positions = {
    1: (a, c),
    2: (b, c),
    3: (c, c),
    4: (a, b),
    5: (b, b),
    6: (c, b),
    7: (a, a),
    8: (b, a),
    9: (c, a),
}


# ------- DRAWBOT SPACE --------

# --- FUNCTIONS

# Draw Grid
def drawGrid(width=1):
    draw.stroke(0, 0.1)
    draw.strokeWidth(width)

    draw.line((part, 0), (part, dimension))
    draw.line((part * 2, 0), (part * 2, dimension))
    draw.line((0, part), (dimension, part))
    draw.line((0, part * 2), (dimension, part * 2))


# rad = radius
# color =
# Draw grid/graph nodes
def drawNodes(rad=1, color=(1, 0, 0, 1)):
    # Pen Setup
    (r, g, b, a) = color
    draw.fill(r, g, b, a)
    draw.stroke(None)
    # Draw Nodes
    for point in positions.values():
        (x, y) = point
        # print(x, y)
        draw.oval(x - rad // 2, y - rad // 2, rad, rad)


# Non recursive Draw
# Primitive line drawing not a path
def drawGraphSkeleton(G, width=1):
    draw.stroke(0)
    draw.strokeWidth(width)
    draw.stroke(1, 0, 0)
    for e in list(G.edges):
        # print(e)
        a, b = e
        draw.line(positions[a], positions[b])


# Non recursive Draw
# Path drawing not connected
def drawGraphSimple(g, width=30):

    draw.newPath()
    # Set up
    draw.stroke(0)
    draw.fill(None)
    draw.strokeWidth(width)
    draw.lineCap("round")
    draw.lineJoin("miter")
    draw.miterLimit(5)

    for e in list(g.edges):
        a, b = e
        draw.moveTo(positions[a])
        draw.lineTo(positions[b])

    draw.drawPath()


# TODO: Deal with decimal innrelines (font weight)
# TODO: Make width and innerLine proportional
# TODO: Add R (readability) variable
# TODO: Add rounding of glyph variable
# TODO: Make sure each varianet looks nice
# Given a graph of nodes it generates a layered glyph
# g = Graph with nodes
# width = stroke width
# innerLines = white paths inside glyph (font weigth)
def drawGlyph(g, width=3, innerLines=7):

    # Size of glyph
    D = dimension
    # Number of space channels
    S = (innerLines * diviser) + diviser
    # Increasing r in (a*width) increases readability
    # or the spacing between stroke groups
    R = 0
    # Size of channel
    C = (D - (R * width)) / S

    # print(C)
    # print(np.rint([innerLines])[0])
    # Set up
    srcShape = draw.BezierPath()
    draw.stroke(0)
    draw.fill(None)
    draw.strokeWidth(width)
    draw.lineCap("round")
    draw.lineJoin("round")

    # Draw Source path based on graph
    for e in list(g.edges):
        a, b = e
        srcShape.moveTo(positions[a])
        srcShape.lineTo(positions[b])
        print("Travel: ", getMoveDirection(positions[a], positions[b]))
    print("_________")
    # Create a russian doll like patter around the source path stroke
    # Turn original stroke into a shape
    for i in range(innerLines, 0, -2):
        expShape = srcShape.expandStroke(C * i, lineCap="square", lineJoin="round")
        expShape.removeOverlap()
        # print("POINTS: ", expShape.points)
        draw.drawPath(expShape)

    # If even space draw the middle line
    if innerLines % 2 == 0:
        draw.drawPath(srcShape)


# Determines the direction of travel between two cords
# start = (x, y) tuple
# end = (x, y) tuple
# returns int
# 1 = horizontal of x travel
# 0 = vertical or y travel
# NOTE: only handles straight travel, no diagonals
def getMoveDirection(start, end):
    return int(start[0] == end[0])


def drawPolygon(points, vColor=(0, 0, 0), hColor=(0, 0, 0)):

    print(len(points))

    for i in range(len(points) - 1):
        srcShape = draw.BezierPath()
        print(points[i], getMoveDirection(points[i], points[i + 1]))
        if getMoveDirection(points[i], points[i + 1]) == 1:
            (r, g, b) = hColor
            draw.stroke(r, g, b)
            # lineCap("square")
        else:
            (r, g, b) = vColor
            draw.stroke(r, g, b)
            # lineCap("butt")

        srcShape.line(points[i], points[i + 1])
        draw.drawPath(srcShape)
    # drawPath(srcShape)


def drawColoredGlyph(g, width=3, innerLines=7, vColor=(1, 0, 0), hColor=(0.95, 0, 0)):

    # Size of glyph
    D = dimension
    # Number of space channels
    S = (innerLines * diviser) + diviser
    # Increasing r in (a*width) increases readability
    # or the spacing between stroke groups
    R = 0
    # Size of channel
    C = (D - (R * width)) / S

    # print(C)
    # print(np.rint([innerLines])[0])
    # Set up
    srcShape = draw.BezierPath()
    draw.stroke(0)
    draw.fill(None)
    draw.strokeWidth(width)
    draw.lineCap("round")
    draw.lineJoin("round")

    # Draw Source path based on graph
    for e in list(g.edges):
        a, b = e
        srcShape.moveTo(positions[a])
        srcShape.lineTo(positions[b])

    # Create a russian doll like patter around the source path stroke
    # Turn original stroke into a shape
    for i in range(innerLines, 0, -2):
        expShape = srcShape.expandStroke(C * i, lineCap="square", lineJoin="round")
        expShape.removeOverlap()
        drawPolygon(expShape.points, vColor, hColor)

    # If even space draw the middle line
    if innerLines % 2 == 0:
        draw.drawPath(srcShape)


# Transform tree graphs to Eularian Graph
# (where each edge is treated as a pair of arcs
# Then draw a path using the nodes generated by
# the Eularian circuit
def drawEularianGraph(g, width=30):

    path = draw.BezierPath()
    # Set up
    draw.stroke(0)
    draw.fill(None)
    draw.strokeWidth(width)
    draw.lineCap("round")
    draw.lineJoin("round")

    # Generate all connected componnet graphs anf ilter out single node graphs
    S = [g.subgraph(c).copy() for c in nx.connected_components(g)]
    S = list(filter(lambda g: g.number_of_nodes() > 1, S))

    for graph in S:

        H = nx.eulerize(graph)
        nodes = [u for u, v in nx.eulerian_circuit(H)]
        sink = nodes[0]
        # Start at sink
        path.moveTo(positions[sink])
        for n in nodes[1::]:
            path.lineTo(positions[n])
        # End at sink
        path.lineTo(positions[sink])

    draw.drawPath(path)


# Recursively draw spanning edges
# someEdge = starting edge
# visited = memoized visited nodes
# count = used to count number of times path is drawn (debug)
def drawEdges(G, someNode, visited=[], count=0):
    # get neighbors
    adjs = list(G.adj[someNode])
    for n in adjs:
        count += 1
        draw.moveTo(positions[someNode])
        draw.lineTo(positions[n])
        # recursive, the stop is in built into the iteration
        # if no adj, then this isn't called
        if not (n in visited):
            drawEdges(G, n, visited + [someNode], count)


# Recursivly draw path, might offer a better solution
# currently not drawing connected path
def drawGraph(g):
    draw.newPath()
    # setup
    draw.stroke(0)
    draw.fill(None)
    draw.strokeWidth(30)
    draw.lineCap("round")
    # move to first node
    n = list(g.nodes)[0]
    draw.moveTo(positions[n])
    # Draw rest of edges
    drawEdges(g, n)
    draw.drawPath()


# n = iteration number, used for page and letter label\
# amount = number of labels
# Draw grid labels and page number
def drawLabels(n, amount=9):
    txt = draw.FormattedString(font="Helvetica", fontSize=12)
    txtU = draw.FormattedString(font="Helvetica", fontSize=12)
    page = draw.FormattedString(f"{n+1}", font="Helvetica", fontSize=12)

    for i in range(0, amount):
        # create grid text with tabs and new line
        end = "\n" if (i + 1) % 3 == 0 else ""
        txt.append(f"{format(n*9 + i,'X')}\t{end}")
        txtU.append(f"___\t{end}")

    # position
    anchor = 32
    draw.text(page, (draw.width() - anchor, draw.height() - anchor))
    draw.text(txt, (anchor, draw.height() - anchor))
    draw.text(txtU, (anchor, draw.height() - anchor * 2.5))


# n = iteration number, used for page and letter label\
# amount = number of labels
# Draw grid labels and page number landscape
def drawLabelsLand(n, amount=9):
    txt = draw.FormattedString(font="Helvetica", fontSize=12)
    txtU = draw.FormattedString(font="Helvetica", fontSize=12)
    page = draw.FormattedString(f"{(n+1)*2}", font="Helvetica", fontSize=12)

    for i in range(0, amount):
        # create grid text with tabs and new line
        end = "\n" if (i + 1) % 3 == 0 else ""
        txt.append(f"{format(n*9 + i,'X')}\t{end}")
        txtU.append(f"___\t{end}")

    # position
    anchor = 32
    draw.text(page, (draw.width() - anchor * 2, anchor))
    draw.text(txt, (draw.width() - anchor * 4, draw.height() - anchor))
    draw.text(txtU, (draw.width() - anchor * 4, draw.height() - anchor * 2.5))


# Create a PDF with dim^2 graphs per page
# graphs = list of NetworkX Graphs
# w = stroke width
# dim = grid dimensions (e.i if dim == 3 then 9 graphs per page)
# hasGrid = draw grid or not
# hasLabel = draw labels or not
def drawAllGraphsLand(graphs, w=30, dim=diviser, hasGrid=False, hasLabel=True):
    draw.newDrawing()
    # 612 * 792
    draw.newPage("LetterLandscape")
    # cell division
    d = draw.height() / dim
    i = 0

    # loop until no more graphs can be drawn
    while i < len(graphs):

        # draw correct number of labels based
        if hasLabel and len(graphs) - i < dim**2:
            drawLabelsLand(i // (dim**2), len(graphs) - i)
        elif hasLabel:
            drawLabelsLand(i // (dim**2))
        elif not hasLabel:
            drawCoverLand(graphs[0].number_of_edges(), len(graphs))

        # number of glyphs to draw
        sub = len(graphs) - i if (len(graphs) - i < dim**2) else dim ** 2

        # Draw two page spread
        for j in range(2):

            if j == 0:
                draw.translate(draw.width() - d * dim, 0)
            else:
                draw.translate(0, 0)
            # Draw 3 * 3 grid of paths
            # move to tope left corner
            draw.translate(0, d * (dim - 1))
            for r in range(0, dim):
                for c in range(0, dim):
                    # Second loop draw glyphs
                    if j == 1:
                        drawGlyph(graphs[i - sub], 0.25, innerLines=5)
                        sub -= 1
                    # First loop draw graphs
                    elif not i >= len(graphs):
                        if hasGrid:
                            drawGrid()
                        drawGraphSimple(graphs[i], w)
                    # move canvas by d
                    draw.translate(d, 0)
                    # prevent increase when drawing glyphs
                    if j != 1:
                        i += 1
                # Move back to x = 0
                # and move y to - d (down)
                draw.translate(-d * dim, -d)
                if i >= len(graphs):
                    break
            draw.newPage("LetterLandscape")

            # Offset to Right, then switch back
            # if(j != 1):
            #     translate(width() - d * 3, 0)
            # else:
            #     translate( 0, 0)

    draw.endDrawing()


def drawAllGraphs(graphs, w=30, dim=diviser, hasGrid=False, hasLabel=True):
    draw.newDrawing()
    # 612 * 792
    draw.newPage("Letter")
    # cell division
    d = draw.width() / dim
    i = 0
    # loop until no more graphs can be drawn
    while i < len(graphs):

        # draw correct number of labels
        if hasLabel and len(graphs) - i < dim**2:
            drawLabels(i // (dim**2), len(graphs) - i)
        elif hasLabel:
            drawLabels(i // (dim**2))
        elif not hasLabel:
            drawCover(graphs[0].number_of_edges(), len(graphs))

        # Draw 3 * 3 grid of paths
        # move to tope left corner
        draw.translate(0, d * (dim - 1))
        for r in range(0, dim):
            for c in range(0, dim):
                if i >= len(graphs):
                    break
                if hasGrid:
                    drawGrid()
                # drawGlyph(graphs[i - sub], w, innerLines=7)
                drawGraphSimple(graphs[i], w)
                # move canvas by d
                draw.translate(d, 0)
                i += 1
            # Move back to x = 0
            # and move y to - d (down)
            draw.translate(-d * dim, -d)

        draw.newPage("Letter")

    draw.endDrawing()


# 8 edges = 13 dim
# 7 edges = 23 dim
# 6 edges = 28 dim
# Draw cover for graph pages
# edges = edges per graph
# comb = number of graph cobinations
def drawCover(edges, comb):
    txt = draw.FormattedString(font="Helvetica", fontSize=12)
    txt.append(f"typeface: ___________\n{edges} edge forest\n{comb} combinations")
    # used if divider global variable was abstracted
    # dim = np.floor(np.sqrt(len(Gs)))
    draw.text(txt, (32, draw.height() - 64))


def drawCoverLand(edges, comb):
    txt = draw.FormattedString(font="Helvetica", fontSize=12)
    txt.append(f"typeface: ___________\n{edges} edge forest\n{comb} combinations")
    # used if divider global variable was abstracted
    # dim = np.floor(np.sqrt(len(Gs)))
    draw.text(txt, (32, draw.height() - 64))


# generate path info
def generatePathInfo():
    print("All Points:")
    print(path.points)

    print("On Curve Points:")
    print(path.onCurvePoints)

    print("Off Curve Points:")
    print(path.offCurvePoints)
    # print out all points from all segments in all contours
    for contour in path.contours:
        for segment in contour:
            for x, y in segment:
                print((x, y))
        print(["contour is closed", "contour is open"][contour.open])


# generates a path file to save drawing to
def saveDrawing(edges):
    path = f"/Users/josesaravia/Projects/Typography/Graph/glyph_design_space_combined_cover_{edges}.pdf"
    draw.saveImage(path)
    return path


# Functions as an instant preview
def openPreview(path):
    import os

    os.system(f"open --background -a Preview {path}")


# HOLDS ALL GRAPHS
all_graphs = generateGraphs(8, forest=True)

i = 1
G = all_graphs[i]
print("Graph", i, "is a forest:", nx.is_forest(G))
print("Number of forest: ", len(all_graphs))

# ---- DRAWING

draw.newDrawing()
draw.size(dimension * 3, dimension * 3)
drawGrid()
drawNodes(10)
# drawGraph(G)
drawGlyph(all_graphs[28], innerLines=2)
draw.translate(dimension, 0)
# drawGraphSimple(all_graphs[4])
drawGlyph(all_graphs[28], innerLines=3)
draw.translate(dimension, 0)
# drawEularianGraph(all_graphs[17])
# drawGlyph(all_graphs[28], innerLines=4)
drawColoredGlyph(all_graphs[20])
draw.translate(0, dimension)
# drawGlyph(all_graphs[28], innerLines=5)
drawColoredGlyph(all_graphs[23])
draw.translate(-dimension, 0)
# drawGlyph(all_graphs[28])
drawColoredGlyph(all_graphs[2])
draw.translate(-dimension, 0)
drawColoredGlyph(all_graphs[28])
draw.endDrawing()


# 6 edge forest

# --- MAIN CODE
# Generate Graphs
# graph_6 = generateGraphs(6, forest=True)
# graph_7 = generateGraphs(7, forest=True)
# graph_8 = generateGraphs(8, forest=True)
# drawAllGraphsLand(graph_6)
# path6 = saveDrawing(6)
# openPreview(path6)
# drawAllGraphsLand(graph_7)
# path7 = saveDrawing(7)
# openPreview(path7)
# drawAllGraphsLand(graph_8)
# path8 = saveDrawing(8)
# openPreview(path8)


# ---- DISPLAY
# drawAllGraphsLand(graph_7, w = 2, dim = diviser, hasLabel=False)
# path6 = saveDrawing(7)
# openPreview(path6)

path = (
    "/Users/josesaravia/Projects/Typography/Generative_Typeface/glyph_design_space.pdf"
)
draw.saveImage(path)
openPreview(path)

# Typeface ______
# 8 edge forest
# 192 combinations
