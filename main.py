#!/usr/bin/env python
from Generator import (
    drawColoredGlyph,
    draw_glyph,
    draw_grid,
    draw_nodes,
    draw_graph_skeleton,
    draw_graph_simple,
    openPreview,
)
from Graph import generate_graphs
from drawBot import _drawBotDrawingTool as draw

DIMENSION = 198


def main():
    # HOLDS ALL GRAPHS
    all_graphs = generate_graphs(8, forest=True)

    i = 1
    G = all_graphs[i]
    # print("Graph", i, "is a forest:", nx.is_forest(G))
    print("Number of forest: ", len(all_graphs))

    # ---- DRAWING

    draw.newDrawing()
    draw.size(DIMENSION * 3, DIMENSION * 3)
    draw_grid()
    draw_nodes(10)
    # drawGraph(G)
    draw_glyph(all_graphs[0], inner_strokes=3)
    draw.translate(DIMENSION, 0)
    # draw_graph_simple(all_graphs[1])
    draw_glyph(all_graphs[28], inner_strokes=7)
    draw.translate(DIMENSION, 0)
    # drawEularianGraph(all_graphs[17])
    # drawGlyph(all_graphs[28], innerLines=4)
    drawColoredGlyph(all_graphs[20])
    # draw.translate(0, DIMENSION)
    # # drawGlyph(all_graphs[28], innerLines=5)
    # drawColoredGlyph(all_graphs[23])
    # draw.translate(-DIMENSION, 0)
    # # drawGlyph(all_graphs[28])
    # drawColoredGlyph(all_graphs[2])
    # draw.translate(-DIMENSION, 0)
    # drawColoredGlyph(all_graphs[28])
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

    path = "/Users/josesaravia/Projects/Typography/Generative_Typeface/glyph_design_space.pdf"
    draw.saveImage(path)
    # openPreview(path)

    # Typeface ______
    # 8 edge forest
    # 192 combinations


if __name__ == "__main__":
    main()
