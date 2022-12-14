using Microsoft.SqlServer.TransactSql.ScriptDom;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Parsnip.NodeMarkers;
using System;
using UnitTestParsnip.TestTraversers;

namespace UnitTestParsnip
{
    [TestClass]
    public class UT_TokenIndexMethodsCreateAlterProcStatements
    {
        TSqlFragment fragment;
        string retValue;

        [TestMethod]
        public void CreateProcedureStatement_GetAllTokens_Index0AndEnd()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesAll(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 2);
            Assert.AreEqual(tokenIndex[0], 0);
            Assert.AreEqual(tokenIndex[1], 16);
        }

        [TestMethod]
        public void CreateProcedureStatement_ProcedureReference_Index0And4()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesProcedureReference(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 2);
            Assert.AreEqual(tokenIndex[0], 0);
            Assert.AreEqual(tokenIndex[1], 4);
        }
        [TestMethod]
        public void CreateProcedureStatement_DeclareToken_Index4()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesDeclare(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 1);
            Assert.AreEqual(tokenIndex[0], 4);
        }

        [TestMethod]
        public void CreateProcedureStatement_ExitProc_Indexis16And16()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexExitProc(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 2);
            Assert.AreEqual(tokenIndex[0], 16);
            Assert.AreEqual(tokenIndex[1], 16);
        }

        [TestInitialize]
        public void tokenIndexMethodInit()
        {
            fragment = TestTSqlFragmentInit.SqlStatementFragment("CREATE PROCEDURE SelectAllCustomers AS SELECT * FROM Customers GO","CreateProcedureStatement"); // .SelectStatement();
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
