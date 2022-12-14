using Microsoft.SqlServer.TransactSql.ScriptDom;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Parsnip.NodeMarkers
{
    public static class TokenIndexMethodsServer
    {
        private static Dictionary<string, Func<TSqlFragment, int[]>> _methodMap = new Dictionary<string, Func<TSqlFragment, int[]>>()
		{
			{ "All", TokenIndexMethods.GetTokenIndexesAll }
			, { "Begin", TokenIndexMethods.GetTokenIndexesBegin}
			, { "BeginTry", TokenIndexMethods.GetTokenIndexesBeginTry}
			, { "CatchStatements", TokenIndexMethods.GetTokenIndexesCatchStatements}
			, { "Declare", TokenIndexMethods.GetTokenIndexesDeclare}
			, { "DropTable", TokenIndexMethods.GetTokenIndexesDropTable}
			, { "End", TokenIndexMethods.GetTokenIndexesEnd}
			, { "EndTry", TokenIndexMethods.GetTokenIndexesEndTry}
			, { "ExitProc", TokenIndexMethods.GetTokenIndexExitProc}
			//, { "GoStatement", TokenIndexMethods.GoStatements}
			, { "IndexAs", TokenIndexMethods.GetTokenIndexAs}
			, { "InsertStatement", TokenIndexMethods.GetTokenIndexesInsertStatement}
			, { "LeftParenthesesIndexes", TokenIndexMethods.GetLeftParenthesesIndexes}
			, { "ProcedureReference", TokenIndexMethods.GetTokenIndexesProcedureReference}
			, { "ReturnStatement", TokenIndexMethods.GetTokenIndexesReturnStatement}
			, { "RightParenthesesIndexes", TokenIndexMethods.GetRightParenthesesIndexes}
			, { "SelectedTableName", TokenIndexMethods.GetTokenIndexesSelectedTableNames}
			, { "SetOnOff", TokenIndexMethods.GetTokenIndexesSetOnOff}
			, { "InsertedTableName", TokenIndexMethods.GetTokenIndexesInsertedTableNames}
			,{"Go", TokenIndexMethods.GoStatements}
			,{"GrantStatement", TokenIndexMethods.GetTokenIndexesGrantStatement}
			,{"ExecuteStatement",TokenIndexMethods.GetTokenIndexExecuteSP}
			,{"CreateIndexStatement",TokenIndexMethods.GetTokenIndexesIndexStatement}
		};

        public static int[] GetTokenIndexes( string indexMethod, TSqlFragment sqlFragment)
        {
            return _methodMap[indexMethod](sqlFragment);
        }
    }
}
