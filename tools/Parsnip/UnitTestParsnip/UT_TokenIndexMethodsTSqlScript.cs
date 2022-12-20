using System;
using Microsoft.SqlServer.TransactSql.ScriptDom;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Parsnip.NodeMarkers;
using UnitTestParsnip.TestTraversers;

namespace UT_TokenIndexMethodsTSqlScript
{
    [TestClass]
    public class UnitTest2
    {
        TSqlFragment fragment;
        string retValue;

        [TestMethod]
        public void TSqlScript_AsToken_Index17()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexAs(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex.Length, 1);
            Assert.AreEqual(tokenIndex[0], 21);
        }

        [TestInitialize]
        public void tokenIndexMethodInit()
        {
            fragment = TestTSqlFragmentInit.SqlStatementFragment("CREATE PROCEDURE SelectAllCustomers @City nvarchar(30), @PostalCode nvarchar(10) AS SELECT * FROM Customers WHERE City = @City AND PostalCode = @PostalCode GO; ", "TSqlScript"); 
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
