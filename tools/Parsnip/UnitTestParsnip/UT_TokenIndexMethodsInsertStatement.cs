using Microsoft.SqlServer.TransactSql.ScriptDom;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Parsnip.NodeMarkers;
using System;
using UnitTestParsnip.TestTraversers;

namespace UnitTestParsnip
{
    [TestClass]
    public class UT_TokenIndexMethodsInsertStatement
    {
        TSqlFragment fragment;
        string retValue;

        [TestMethod]
        public void InsertedTableNames_TableName_IndexIs4and4()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesInsertedTableNames(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 2);
            Assert.AreEqual( tokenIndex[0], 4);
            Assert.AreEqual(tokenIndex[1], 4);
        }


        [TestMethod]
        public void SelectedTableNames_TableName_IndexIs12()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesSelectedTableNames(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 1);
            Assert.AreEqual(tokenIndex[0], 12);
        }

        [TestMethod]
        public void InsertedTableNames_RightParens_IndexIs4and4()
        {
            var tokenIndex = TokenIndexMethods.GetRightParenthesesIndexes(fragment);
            Assert.AreEqual(tokenIndex.Length, 0);
        }

        [TestInitialize]
        public void tokenIndexMethodInit()
        {
            fragment = TestTSqlFragmentInit.SqlStatementFragment("INSERT INTO Names SELECT name FROM client c LEFT JOIN customer c1 ON c.Name = c1.Name", "InsertStatement"); // .SelectStatement();
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
