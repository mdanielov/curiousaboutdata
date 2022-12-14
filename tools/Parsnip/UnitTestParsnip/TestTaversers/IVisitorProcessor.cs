using Microsoft.SqlServer.TransactSql.ScriptDom;

namespace UnitTestParsnip.TestTraversers
{
    public interface IVisitorProcessor
    {
        void Process(TSqlFragment sqlFragment);
    }
}
