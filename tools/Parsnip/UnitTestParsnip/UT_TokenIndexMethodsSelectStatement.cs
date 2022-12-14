using Microsoft.SqlServer.TransactSql.ScriptDom;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Parsnip.NodeMarkers;
using System;
using UnitTestParsnip.TestTraversers;

namespace UnitTestParsnip
{
    [TestClass]
    public class UT_TokenIndexMethodsSelectStatement
    {
        TSqlFragment fragment;
        string retValue;

        [TestMethod]
        public void SelectStatement_TableName_IndexIs6and11()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesSelectTableNames(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 2);
            Assert.AreEqual( tokenIndex[0], 6);
            Assert.AreEqual( tokenIndex[1], 11);
        }

        [TestMethod]
        public void SelectedStatement_RightParens_IndexZeroLength()
        {
            var tokenIndex = TokenIndexMethods.GetRightParenthesesIndexes(fragment);
            Assert.AreEqual(tokenIndex.Length, 0);
        }

        [TestInitialize]
        public void tokenIndexMethodInit()
        {
            //fragment = TestTSqlFragmentInit.SqlStatementFragment("SELECT name FROM client c JOIN customer c1 ON c1.client_id = c.id", "SelectStatement");
            fragment = TestTSqlFragmentInit.SqlStatementFragment("SELECT name FROM client c, customer c1 WHERE c1.client_id = c.id", "SelectStatement");
            // fragment = TestTSqlFragmentInit.SelectStatement(); // .SelectStatement();
            retValue = "done";
        }
        [TestCleanup]
        public void tokenIndexMethodCleanup()
        {
            fragment = null;
            retValue = String.Empty;
        }

    }
}
