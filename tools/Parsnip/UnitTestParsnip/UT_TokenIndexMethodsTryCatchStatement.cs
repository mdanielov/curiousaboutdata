using Microsoft.SqlServer.TransactSql.ScriptDom;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Parsnip.NodeMarkers;
using System;
using UnitTestParsnip.TestTraversers;

namespace UnitTestParsnip
{
    /// <summary>
    /// Summary description for UT_TokenIndexMethodsTryCatchStatement
    /// </summary>
    [TestClass]
    public class UT_TokenIndexMethodsTryCatchStatement
    {
        TSqlFragment fragment;
        string retValue;

        [TestMethod]
        public void TryCatchStatement_BeginTry_IndexIs0And3()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesBeginTry(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 2);
            Assert.AreEqual(tokenIndex[0], 0);
            Assert.AreEqual(tokenIndex[1],3);
        }


        [TestMethod]
        public void TryCatchStatement_BeginTry_IndexIs0()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesCatchStatements(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 2);
            Assert.AreEqual(tokenIndex[0], 17);
            Assert.AreEqual(tokenIndex[1], 28);
        }


        [TestInitialize]
        public void tokenIndexMethodInit()
        {
            fragment = TestTSqlFragmentInit.SqlStatementFragment("BEGIN TRY SELECT 1 / 0; END TRY BEGIN CATCH EXECUTE usp_GetErrorInfo; END CATCH","TryCatchStatement"); // .SelectStatement();
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
