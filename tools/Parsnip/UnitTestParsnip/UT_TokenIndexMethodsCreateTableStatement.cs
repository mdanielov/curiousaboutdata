using System;
using Microsoft.SqlServer.TransactSql.ScriptDom;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Parsnip.NodeMarkers;
using UnitTestParsnip.TestTraversers;

namespace UnitTestParsnip
{
    [TestClass]
    public class UT_TokenIndexMethodsCreateTableStatement
    {
        TSqlFragment fragment;
        string retValue;

        [TestMethod]
        public void CreateTableStatement_DropTable_Index1()
        {
            var tokenIndex = TokenIndexMethods.GetTokenIndexesDropTable(fragment);
            Assert.IsNotNull(fragment);
            Assert.AreEqual(tokenIndex[0], -1);

        }

        [TestInitialize]
        public void tokenIndexMethodInit()
        {
            fragment = TestTSqlFragmentInit.SqlStatementFragment("CREATE TABLE Persons ( PersonID int, LastName varchar(255), FirstName varchar(255), Address varchar(255), City varchar(255)); ", "CreateTableStatement");
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
