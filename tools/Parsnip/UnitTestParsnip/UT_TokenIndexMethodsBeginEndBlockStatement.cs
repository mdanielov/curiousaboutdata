using Microsoft.SqlServer.TransactSql.ScriptDom;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Parsnip.NodeMarkers;
using System;
using UnitTestParsnip.TestTraversers;

namespace UnitTestParsnip
{
    [TestClass]
    public class UT_TokenIndexMethodsBeginEndBlockStatement
    {
        TSqlFragment fragment;
        string retValue;

        [TestMethod]
        public void BeginEndBlockBegin_EndClause_IndexIs0()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesEnd(fragment);
            Assert.IsNotNull(fragment);

        }


        [TestMethod]
        public void BeginEndBlockBegin_BeginClause_IndexIs0()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesBegin(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 0);
        }


        [TestInitialize]
        public void tokenIndexMethodInit()
        {
            fragment = TestTSqlFragmentInit.SqlStatementFragment("BEGIN DROP TABLE Names END","BeginEndBlockStatement"); // .SelectStatement();
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
