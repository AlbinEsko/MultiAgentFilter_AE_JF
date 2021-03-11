/*
 * Here for getting studied and converted to python
 */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tower_Maul
{
    class Graph
    {
        List<int>[] adjacency;
        int startNode, endNode;

        public Graph(int nrNodes)
        {
            adjacency = new List<int>[nrNodes];
            for (int i = 0; i < adjacency.Length; i++)
            {
                adjacency[i] = new List<int>();
            }
            startNode = 0;
            endNode = adjacency.Length - 1;
        }

        public void Clear()
        {
            for (int i = 0; i < adjacency.Length; i++)
            {
                adjacency[i].Clear();
            }
        }

        public void CreateGraph(Tile[,] tiles)
        {
            int rows = tiles.GetLength(1);
            int cols = tiles.GetLength(0);
            for (int y = 0; y < rows; y++)
            {
                for (int x = 0; x < cols; x++)
                {
                    if (tiles[x, y].currentType != Tile.Type.BLOCKING)
                    {
                        CreateConnections(tiles, rows, cols, y, x);
                    }
                }
            }
        }

        private void CreateConnections(Tile[,] tiles, int rows, int cols, int y, int x)
        {
            bool leftFree = x - 1 >= 0 && tiles[x - 1, y].currentType != Tile.Type.BLOCKING;
            bool rightFree = x + 1 < cols && tiles[x + 1, y].currentType != Tile.Type.BLOCKING;
            bool topFree = y - 1 >= 0 && tiles[x, y - 1].currentType != Tile.Type.BLOCKING;
            bool botFree = y + 1 < rows && tiles[x, y + 1].currentType != Tile.Type.BLOCKING;
            //Horizontal Connections
            if (leftFree)
                adjacency[x + y * cols].Add((x - 1) + y * cols);
            if (rightFree)
                adjacency[x + y * cols].Add((x + 1) + y * cols);

            //Vertical Connections
            if (topFree)
                adjacency[x + y * cols].Add(x + (y - 1) * cols);
            if (botFree)
                adjacency[x + y * cols].Add(x + (y + 1) * cols);

            //Diagonal Connections
            if (topFree && leftFree)
                adjacency[x + y * cols].Add(x - 1 + (y - 1) * cols);
            if (botFree && leftFree)
                adjacency[x + y * cols].Add(x - 1 + (y + 1) * cols);
            if (topFree && rightFree)
                adjacency[x + y * cols].Add(x + 1 + (y - 1) * cols);
            if (botFree && rightFree)
                adjacency[x + y * cols].Add(x + 1 + (y + 1) * cols);
        }

        private int[] CreateMinSpanTree(int from)
        {
            bool[] enqueued = new bool[adjacency.Length];
            int[] minSpanningTree = new int[adjacency.Length];
            Queue<int> nodeQue = new Queue<int>();
            nodeQue.Enqueue(from);
            enqueued[nodeQue.Peek()] = true;
            while (nodeQue.Count > 0)
            {
                int activeNode = nodeQue.Dequeue();
                foreach (int edge in adjacency[activeNode])
                {
                    int toIndex = edge;
                    if (!enqueued[toIndex])
                    {
                        enqueued[toIndex] = true;
                        minSpanningTree[edge] = activeNode;
                        nodeQue.Enqueue(toIndex);
                    }
                }
            }
            return minSpanningTree;
        }
        public List<int> FindShortestPathToGoal(int from)
        {
            if (from == -1)
                throw new ArgumentOutOfRangeException("tried using node \"-1\"");
            List<int> path = new List<int>();
            int[] minSpanTree = CreateMinSpanTree(from);
            for (int nodeId = endNode; nodeId != from; nodeId = minSpanTree[nodeId])
            {
                path.Add(nodeId);
            }
            path.Add(from);
            return path;
        }
    }
}
