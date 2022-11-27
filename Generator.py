from drawBot import _drawBotDrawingTool as draw
import networkx as nx

# import matplotlib.pyplot as plt
import numpy as np
import string
from itertools import combinations

from Graph import generate_graphs

# canvas size
# This varaible is manually modified and caclulated
# This was done to keep the code readable
dimension = 198
# grid cell dimension
DIVISER = 3
# canvas space division
PART = dimension / DIVISER
# cell division
DIV = PART // 2

path = (
    "/Users/josesaravia/Projects/Typography/Generative_Typeface/glyph_design_space.pdf"
)

# Graph Node Positions for drawBot drawing
# 1 2 3 c
# 4 5 6 b
# 7 8 9 a
# a b c
A = DIV
B = DIV + PART
C = DIV + PART * 2
POSITIONS = {
    1: (A, C),
    2: (B, C),
    3: (C, C),
    4: (A, B),
    5: (B, B),
    6: (C, B),
    7: (A, A),
    8: (B, A),
    9: (C, A),
}


# ------- DRAWBOT SPACE --------

# --- FUNCTIONS


def draw_grid(width: int = 1) -> None:
    """
    Draw Grid of PART X PART

    Parameters
    ----------
    width : int, optional
        Width of Grid Stroke, by default 1
    """
    # Set drawing stroke
    draw.stroke(0, 0.1)
    draw.strokeWidth(width)

    # Draw PART * PART Grid
    draw.line((PART, 0), (PART, dimension))
    draw.line((PART * 2, 0), (PART * 2, dimension))
    draw.line((0, PART), (dimension, PART))
    draw.line((0, PART * 2), (dimension, PART * 2))


def draw_nodes(rad: int = 1, color: tuple = (1, 0, 0, 1)) -> None:
    """
    Draws All Grid Graph Nodes

    Parameters
    ----------
    rad : int, optional
        Radius of Node, by default 1
    color : tuple, optional
        Color(rgba) of Node, by default RED
    """
    # Pen Setup
    (r, g, b, a) = color
    draw.fill(r, g, b, a)
    draw.stroke(None)

    # Draw Nodes
    for point in POSITIONS.values():
        (x, y) = point
        # Subtract rad//2 to compensate for Drawbot Drawing
        # Ensures written in center
        draw.oval(x - rad // 2, y - rad // 2, rad, rad)


def draw_graph_skeleton(G: nx.Graph, width: int = 1) -> None:
    """
    Draws a simple skeleton of the Graph. Mostly used for debugging.
    This drawing is a primative line drawing, not a Drawbot Path that is drawn recursively.

    Parameters
    ----------
    G : nx.Graph
        Graph to draw skeleton of
    width : int, optional
        Width of Graph Skeleton Stroke, by default 1
    """
    # Pen Setup
    draw.stroke(0)
    draw.strokeWidth(width)
    draw.stroke(1, 0, 0)

    # Iteratively draw lines
    for e in list(G.edges):
        # Tuple of ints corresponding to keys in POSITIONS
        a, b = e
        draw.line(POSITIONS[a], POSITIONS[b])


def draw_graph_simple(G: nx.Graph, width: int = 30) -> None:
    """
    Draws a simple Graph using disconnected DrawBot paths.
    Path is not drawn recursively.

    Parameters
    ----------
    G : nx.Graph
        Graph to draw
    width : int, optional
        Width of Graph Stroke, by default 30
    """
    draw.newPath()
    # Set up
    draw.stroke(0)
    draw.fill(None)
    draw.strokeWidth(width)
    draw.lineCap("round")
    draw.lineJoin("miter")
    draw.miterLimit(5)

    # Iteratively add lines to path
    for e in list(G.edges):
        a, b = e
        draw.moveTo(POSITIONS[a])
        draw.lineTo(POSITIONS[b])

    draw.drawPath()


# TODO: Deal with decimal innerlines (font weight)
# TODO: Make width and innerLine proportional
# TODO: Add R (readability) variable (font abstraction)
# TODO: Add rounding of glyph variable
# TODO: Make sure each varient looks nice
# TODO: Create Recursive Version
# TODO: Move drawing mechanism to a differnt location, instead return a Path
def draw_glyph(G: nx.Graph, stroke_width=3, inner_strokes=7) -> None:
    """
    Given a graph ``G``, use its nodes and edges to create a glyph with n-``inner_strokes`` white paths

    Parameters
    ----------
    G : nx.Graph
        Graph to draw into a Glyph
    stroke_width : int, optional
        Width of glyph stroke, by default 3
    inner_strokes : int, optional
        Number of white paths inside the glyph, by default 7
    """
    # D: Dimensions of Glyps (D x D)
    # S: Spacers, the number of micro-grid partitions (S x S). Think of them as channels.
    # R: Readability controlled by the spacing between stroke groups (Disabled for now)
    # C: Spacer (Channel) dimmension
    # Each S is CxC, and SxS = DxD = (3C)^6

    # Size of glyph
    D = dimension
    # Grid is broken into a smaller parts.
    S = (inner_strokes * DIVISER) + DIVISER
    R = 0
    C = (D - (R * stroke_width)) / S

    # Set up
    src_shape = draw.BezierPath()
    draw.stroke(0)
    draw.fill(None)
    draw.strokeWidth(stroke_width)
    draw.lineCap("round")
    draw.lineJoin("round")

    # Draw Source path based on graph
    for e in list(G.edges):
        a, b = e
        src_shape.moveTo(POSITIONS[a])
        src_shape.lineTo(POSITIONS[b])
        print("Travel: ", get_move_direction(POSITIONS[a], POSITIONS[b]))
    print("_________")

    # Create a russian doll like patter around the source path stroke (created above)
    # Turn original stroke into a shape, | -> |=|
    # TODO: Turn this into a recursive function that build the shape from the inside out
    for i in range(inner_strokes, 0, -2):
        expShape = src_shape.expandStroke(C * i, lineCap="square", lineJoin="round")
        # Remove any overlap lines (shapes)
        expShape.removeOverlap()
        draw.drawPath(expShape)

    # If even space draw the middle line
    if inner_strokes % 2 == 0:
        draw.drawPath(src_shape)


def get_move_direction(start: tuple, end: tuple) -> int:
    """
    Determines the direction of travel between two cords
    NOTE: only handles straight travel, no diagonals

    Parameters
    ----------
    start : tuple
        Start coordinate (x1,y1)
    end : tuple
        End coordinate (x2, y2)

    Returns
    -------
    int
        1 for horizontal x travel \n
        0 for vertical y travel
    """
    # Check if x cord are equal, if so return 1, return 0
    return int(start[0] == end[0])


def drawPolygon(points, vColor=(0, 0, 0), hColor=(0, 0, 0)):

    print(len(points))

    for i in range(len(points) - 1):
        srcShape = draw.BezierPath()
        print(points[i], get_move_direction(points[i], points[i + 1]))
        if get_move_direction(points[i], points[i + 1]) == 1:
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
    S = (innerLines * DIVISER) + DIVISER
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
        srcShape.moveTo(POSITIONS[a])
        srcShape.lineTo(POSITIONS[b])

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
        path.moveTo(POSITIONS[sink])
        for n in nodes[1::]:
            path.lineTo(POSITIONS[n])
        # End at sink
        path.lineTo(POSITIONS[sink])

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
        draw.moveTo(POSITIONS[someNode])
        draw.lineTo(POSITIONS[n])
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
    draw.moveTo(POSITIONS[n])
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
def drawAllGraphsLand(graphs, w=30, dim=DIVISER, hasGrid=False, hasLabel=True):
    draw.newDrawing()
    # 612 * 792
    draw.newPage("LetterLandscape")
    # cell division
    d = draw.height() / dim
    i = 0

    # loop until no more graphs can be drawn
    while i < len(graphs):

        # draw correct number of labels based
        if hasLabel and len(graphs) - i < dim ** 2:
            drawLabelsLand(i // (dim ** 2), len(graphs) - i)
        elif hasLabel:
            drawLabelsLand(i // (dim ** 2))
        elif not hasLabel:
            drawCoverLand(graphs[0].number_of_edges(), len(graphs))

        # number of glyphs to draw
        sub = len(graphs) - i if (len(graphs) - i < dim ** 2) else dim ** 2

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
                        draw_glyph(graphs[i - sub], 0.25, inner_strokes=5)
                        sub -= 1
                    # First loop draw graphs
                    elif not i >= len(graphs):
                        if hasGrid:
                            draw_grid()
                        draw_graph_simple(graphs[i], w)
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


def drawAllGraphs(graphs, w=30, dim=DIVISER, hasGrid=False, hasLabel=True):
    draw.newDrawing()
    # 612 * 792
    draw.newPage("Letter")
    # cell division
    d = draw.width() / dim
    i = 0
    # loop until no more graphs can be drawn
    while i < len(graphs):

        # draw correct number of labels
        if hasLabel and len(graphs) - i < dim ** 2:
            drawLabels(i // (dim ** 2), len(graphs) - i)
        elif hasLabel:
            drawLabels(i // (dim ** 2))
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
                    draw_grid()
                # drawGlyph(graphs[i - sub], w, innerLines=7)
                draw_graph_simple(graphs[i], w)
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
