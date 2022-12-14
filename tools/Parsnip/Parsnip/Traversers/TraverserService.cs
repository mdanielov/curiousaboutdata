using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.SqlServer.TransactSql.ScriptDom;
using Parsnip.NodeMarkers;

namespace Parsnip.Traverser
{
    public class TraverserService
    {
        private static NodeMarkerContainer _nodeMarkerContainer { get; set; }
        private static string _sqlFileName { get; set; }
        public TraverserService(NodeMarkerContainer nodeMarkerContainer, string sqlFileName)
        {
            _nodeMarkerContainer = nodeMarkerContainer;
            _sqlFileName = sqlFileName;
        }
        public TSqlFragment Traverse()
        {
            TSqlFragment tree = null;
            using (var rdr = new StreamReader(_sqlFileName))
            {
                tree = Parse(rdr);
                try
                {
                    
                    VisitTree(tree);
                }
                catch (Exception e)
                {
                    Program.log.Debug(e.Message);
                }
            }
            return tree;
        }

        public static TSqlFragment Parse(StreamReader rdr)
        {
            IList<ParseError> errors = null;

            var parser = new TSql150Parser(true, SqlEngineType.All);
            var tree = parser.Parse(rdr, out errors); // returns a fragment (a parse tree)

            foreach (ParseError err in errors)
            {
                Program.log.Info(">>> Error num" + err.Number + err.Message + err.Line);
            }
            return tree;
        }

        private static void VisitTree(TSqlFragment tree)
        {
            var fragVisitor = new FragmentVisitor(_nodeMarkerContainer);
            tree.Accept(fragVisitor);
        }

    }
}
