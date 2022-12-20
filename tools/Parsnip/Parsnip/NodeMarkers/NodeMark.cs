using System;
using System.Linq;

/* individual marker for a node to instruct the transfomrer what function to do on the result tree */
namespace Parsnip.NodeMarkers
{
    public class NodeMark
    {
        public string NodeType { get; set; }
        public int[] TokenIndexes { get; set; }
        public string Action { get; set; }
        private string sql { get; set; }

        public string FormatMarker()
        {
            if( this.TokenIndexes is null) { return $"{NodeType} Token indexes are null";  }
            var sTokens = String.Join(",", this.TokenIndexes.Select(p => p.ToString()).ToArray());
            return string.Format("{0}: {1} {2} {3}", NodeType, sTokens, Action, sql);
        }

        public NodeMark( string nodeType, int[] tokens, string action = null, string sqlStmnt = null)
        {
            NodeType = nodeType;
            TokenIndexes = tokens;
            Action = action;
            sql = sqlStmnt;
        }
    }
}
