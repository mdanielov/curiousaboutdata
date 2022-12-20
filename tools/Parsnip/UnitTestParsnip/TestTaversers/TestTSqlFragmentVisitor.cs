using Microsoft.SqlServer.TransactSql.ScriptDom;

namespace UnitTestParsnip.TestTraversers
{
    public class TestTSqlFragmentVisitor : TSqlFragmentVisitor
    {
        public IVisitorProcessor Processor { get; set; }
        public override void Visit(TSqlFragment node)
        {
            Processor.Process(node);
        }
    }
}
