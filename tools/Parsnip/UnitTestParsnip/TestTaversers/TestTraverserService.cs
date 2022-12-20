using Microsoft.SqlServer.TransactSql.ScriptDom;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UnitTestParsnip.TestTraversers
{
    public class TestTraverserService
    {
        public static TestTSqlFragmentVisitor visitor { get; set; }

        public static void Parse(string sql, IVisitorProcessor processor)
        {
            visitor = new TestTSqlFragmentVisitor();
            visitor.Processor = processor;
            IList<ParseError> errors = null;
            TSqlFragment tree = null;
            using (var sr = new StringReader(sql))
            {
                var parser = new TSql150Parser(true, SqlEngineType.All);
                tree = parser.Parse(sr, out errors); // returns a fragment (a parse tree)
                try
                {
                    VisitTree( tree);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Message);
                }
            }
        }

        private static void VisitTree( TSqlFragment tree)
        {
            tree.Accept(visitor);
        }
    }
}
