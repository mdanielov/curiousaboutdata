using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.SqlServer.TransactSql.ScriptDom;

namespace Parsnip.NodeMarkers
{
    public class NodeMarkerContainer
    {
        public List<NodeMark> NodeMarkerList;

        public NodeMarkerContainer()
        {
            NodeMarkerList = new List<NodeMark>();
        }

        public void Mark(TSqlFragment sqlFragment)
        {
            NodeMarker nm = new NodeMarker(); //  NodeMarkerFactory.GetNodeMarker(sqlFragment);
            nm.Container = this;
            nm.Mark(sqlFragment);
        }

        public void InsertNodeMarker(string nodeType, int[] tokens, string action, string sqlStmnt = null)
        {
            //removes action if exists for nodeType+tokens combo 
            // NodeMarkerList.Remove(NodeMarkerList.Find(item => item.NodeType == nodeType && item.TokenIndexes == tokens));
            //var originalNodeMark = NodeMarkerList.Find(item => item.NodeType == nodeType && ((item.TokenIndexes == null && tokens == null) || item.TokenIndexes?[0] == tokens?[0] && item.TokenIndexes?[1] == tokens?[1]));
            //if (originalNodeMark != null)
            //{
            //    originalNodeMark.Action = action;
            //}
            //else
            //{
                NodeMarkerList.Add(
                    new NodeMark(nodeType,
                        tokens,
                        action,
                        sqlStmnt
                        )
                    );
            //}
            
        }

    }
}
