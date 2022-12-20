using Microsoft.SqlServer.TransactSql.ScriptDom;

namespace UnitTestParsnip.TestTraversers
{
    public class TestTSqlFragmentInit
    {
        private static VisitorProcessor _processor;
        public static TSqlFragment SqlFragment { get { return _processor.SqlFragment; } }

        public static TSqlFragment SqlStatementFragment(string sqlStatement, string fragmentName)
        {
            _processor = new VisitorProcessor(fragmentName);
            TestTraverserService.Parse(sqlStatement, _processor);
            return _processor.SqlFragment;

        }

        public static TSqlFragment SelectStatement()
        {
            return SqlStatementFragment("SELECT name FROM client", "SelectStatement");
        }

        public static TSqlFragment InsertStatement()
        {
            return SqlStatementFragment("INSERT INTO client(name) VALUES ( 'John');", "InsertStatement");
        }
    }
}
