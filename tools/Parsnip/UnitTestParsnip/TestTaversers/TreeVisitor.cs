using Microsoft.SqlServer.TransactSql.ScriptDom;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UnitTestParsnip.TestTraversers
{
    public class TreeVisitor : TSqlFragmentVisitor
    {
        private VisitorProcessor _visitNodeProcess { get; set; }

        public TreeVisitor(VisitorProcessor visitNodeProcess)
        {
            _visitNodeProcess = visitNodeProcess;
        }

        public override void Visit(TSqlFragment node)
        {
            _visitNodeProcess.Process(node);
        }
    }
}
