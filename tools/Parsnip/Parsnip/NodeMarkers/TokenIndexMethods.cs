using Microsoft.SqlServer.TransactSql.ScriptDom;
using System.Linq;
using System;
using System.Collections.Generic;

namespace Parsnip.NodeMarkers
{
    public static class TokenIndexMethods
    {
        public static int[] GetTokenIndexesAll(TSqlFragment node)
        {
            return new int[] { node.FirstTokenIndex, node.LastTokenIndex };
        }
        public static int[] GetTokenIndexesProcedureReference(TSqlFragment node)
        {
            var retval = new int[] { 0, 0 };
            var typeName = node.GetType().Name;
            if (typeName.Equals("AlterProcedureStatement"))
            {
                retval = new int[] { ((AlterProcedureStatement)node).FirstTokenIndex, ((AlterProcedureStatement)node).ProcedureReference.LastTokenIndex };
            }
            if (typeName.Equals("CreateProcedureStatement"))
            {
                retval = new int[] { ((CreateProcedureStatement)node).FirstTokenIndex, ((CreateProcedureStatement)node).ProcedureReference.LastTokenIndex };
            }
            return retval;
        }

        public static int[] GetTokenIndexesDeclare(TSqlFragment node)
        {
            var retval = new int[] { 0, 0 };
            var typeName = node.GetType().Name;
            if (typeName.Equals("AlterProcedureStatement"))
            {
                retval = new int[] { ((AlterProcedureStatement)node).ProcedureReference.LastTokenIndex  };
            }
            if (typeName.Equals("CreateProcedureStatement"))
            {
                retval = new int[] { ((CreateProcedureStatement)node).ProcedureReference.LastTokenIndex };
            }
            return retval;
        }

        public static int[] GetTokenIndexAs(TSqlFragment node)
        {
            int token = NodeMarkerHelper.GetTokenTypeIndex(node, node.FirstTokenIndex,+1, TSqlTokenType.As);
            return new int[] { token};
        }

        public static int[] GetTokenIndexExitProc(TSqlFragment node)
        {
            // int token = NodeMarkerHelper.GetTokenTypeIndex(node, node.FirstTokenIndex, TSqlTokenType.Exit);
            int token = NodeMarkerHelper.GetTokenIndexOfString(node, node.FirstTokenIndex, node.LastTokenIndex, "EXITPROCEDURE:");
            
            return new int[] { token, node.LastTokenIndex };
        }

        public static int[] GetTokenIndexesBegin(TSqlFragment node)
        {
            
            var prevNodeIndex = NodeMarkerHelper.GetNextorPrevTokenIndex(node, node.FirstTokenIndex, -1);
            var isAsBegin = node.ScriptTokenStream[prevNodeIndex].TokenType == TSqlTokenType.As && prevNodeIndex>=0;
            return (isAsBegin) ? new int[] { node.FirstTokenIndex, node.FirstTokenIndex } : new int[] { };
        }

        public static int[] GetTokenIndexesEnd(TSqlFragment node)
        {
            var isEnd = GetTokenIndexesBegin(node).Length > 0;
            return (isEnd) ? new int[] { node.LastTokenIndex, node.LastTokenIndex } : new int[] { };
        }

        public static int[] GetTokenIndexesDropTable(TSqlFragment node)
        {
            return new int[] { node.FirstTokenIndex - 1, ((CreateTableStatement)node).SchemaObjectName.BaseIdentifier.FirstTokenIndex};
        }

        public static int[] GetTokenIndexesInsertStatement(TSqlFragment node)
        {
            var targetIndex = ((InsertStatement)node).InsertSpecification.Target.FirstTokenIndex;

            var isTemp = node.ScriptTokenStream[targetIndex].Text.StartsWith("#");
           
            return (isTemp) ? new int[] { }:new int[] { node.FirstTokenIndex , ((InsertStatement)node).InsertSpecification.InsertSource.FirstTokenIndex - 1 };

        }

        public static int[] GetTokenIndexesInsertedTableNames(TSqlFragment node)
        {
            var insertSpecification = ((InsertStatement)node).InsertSpecification.Target;
            var targetIndex = insertSpecification.FirstTokenIndex;
            return (node.ScriptTokenStream[targetIndex].Text.StartsWith("#")) ?
                 new int[] { } : new int[] { insertSpecification.FirstTokenIndex,insertSpecification.LastTokenIndex };
        }

        public static int[] GetTokenIndexesSelectTableNames(TSqlFragment node)
        {
            var queryExpression = (QuerySpecification)((SelectStatement)node).QueryExpression;
            //!item.ScriptTokenStream[item.FirstTokenIndex].Text.StartsWith("#") &&
            var targetIndex = queryExpression.FromClause.TableReferences
                .Where(item => item != null)
                .Select(item => item.FirstTokenIndex)
            .ToArray<int>();
            return targetIndex;
            //var targetIndex2 = queryExpression.FromClause.TableReferences
            //    .Where(item => item != null)
            //    .Select(item => item.LastTokenIndex)
            //    .ToArray<int>();
            //foreach (int i in targetIndex)
            //{
            //    return new int[] { targetIndex[i], targetIndex2[i] };
            //}
            //return new int[] { };
        }

        public static int[] GetTokenIndexesSelectedTableNames(TSqlFragment node)
        {
            var targetIndex = ((InsertStatement)node).InsertSpecification.Target.FirstTokenIndex;
            var selectStatement = (SelectInsertSource)((InsertStatement)node).InsertSpecification.InsertSource;
            var specification = (QuerySpecification)selectStatement.Select; // as QuerySpecification;
            //Identifier tableName;
            //int[] tableNamesArray;
            if (specification.FromClause != null)
            {
                var tableNames1 = specification.FromClause.TableReferences
                    .Where(item => item != null )//&& !item.ScriptTokenStream[targetIndex].Text.StartsWith("#"))
                    .Select(item =>  item.FirstTokenIndex)
                    .ToArray<int>();
                var tableNames2 = specification.FromClause.TableReferences
                    .Where(item => item != null )//&& !item.ScriptTokenStream[targetIndex].Text.StartsWith("#"))
                    .Select(item => item.LastTokenIndex)
                    .ToArray<int>();

                //Enumerable.Range(tableNames1[0], tableNames1.Length).Select(x => x).ToList().ForEach(x=>{return new int [] { tableNames1[x], tableNames2[x] };
                for(var i=0; i<tableNames1.Length; i++)
                {
                    return new int[] { tableNames1[i], tableNames2[i] };
                }


            }

            return new int[] { };
        }

        public static int[] GetLeftParenthesesIndexes(TSqlFragment node)
        {
            var nextNodeIndex = NodeMarkerHelper.GetNextorPrevTokenIndex(node, node.FirstTokenIndex, -1);
            var isPar = node.ScriptTokenStream[nextNodeIndex].TokenType == TSqlTokenType.LeftParenthesis;
            return (isPar)? new int[] { nextNodeIndex,nextNodeIndex}: new int[] { };
        }

        public static int[] GetRightParenthesesIndexes(TSqlFragment node)
        {
            var prevNodeIndex = NodeMarkerHelper.GetNextorPrevTokenIndex(node, node.FirstTokenIndex, +1);
            var isPar = node.ScriptTokenStream[prevNodeIndex].TokenType == TSqlTokenType.RightParenthesis;
            return (isPar) ? new int[] { prevNodeIndex, prevNodeIndex } : new int[] { };
            
        }

        public static int[] GetTokenIndexesReturnStatement(TSqlFragment node)
        {
            return new int[] { node.FirstTokenIndex, node.LastTokenIndex };
        }

        public static int[] GetTokenIndexesSetOnOff(TSqlFragment node)
        {
            return new int[] { node.FirstTokenIndex, node.LastTokenIndex + 2 };
        }

        public static int[] GetTokenIndexesBeginTry(TSqlFragment node)
        {
            
            return new int[] { node.FirstTokenIndex, ((TryCatchStatement)node).TryStatements.FirstTokenIndex - 1 };
        }

        public static int[] GetTokenIndexesCatchStatements(TSqlFragment node)
        {
            int Catchindex = ((TryCatchStatement)node).CatchStatements.FirstTokenIndex;
            var beginCatchindex = NodeMarkerHelper.GetTokenTypeIndex(node, Catchindex, -1, TSqlTokenType.Begin);
            return new int[] { beginCatchindex, node.LastTokenIndex };
        }

        public static int[] GetTokenIndexesEndTry(TSqlFragment node)
        {
            return new int[] { ((TryCatchStatement)node).TryStatements.LastTokenIndex + 1, ((TryCatchStatement)node).LastTokenIndex + 1 };
        }

        public static int[] GetTokenIndexesComments(TSqlFragment node)
        {

            var retval = node.ScriptTokenStream
                .Where(x => x.TokenType == TSqlTokenType.MultilineComment || x.TokenType == TSqlTokenType.SingleLineComment)
                .Select( (item, ii) => ii)
                .ToArray<int>();

            return retval;
        }
        public static int[] GoStatements(TSqlFragment node)
        {
            int[] retval = Array.Empty<int>();
            List<int> vals = new List<int>();

            for (int i = 0; i < node.ScriptTokenStream.Count(); i++)
            {
                if (node.ScriptTokenStream[i].TokenType == TSqlTokenType.Go){vals.Add(i);}
           
            }
            retval = vals.ToArray();
            return (retval.Length == 0) ? new int[] { -1, -1 } : retval;
        }

        public static int[] GetTokenIndexesGrantStatement(TSqlFragment node)
        {
            //var retval = new int[] { 0, 0 };
            int retval = NodeMarkerHelper.GetTokenTypeIndex(node, node.FirstTokenIndex, node.LastTokenIndex, TSqlTokenType.Grant);

            return (retval == 0) ? new int[] { -1, -1 } : new int[] { retval };
        }

        public static int[] GetTokenIndexesIndexStatement(TSqlFragment node)
        {
            //var retval = new int[] { 0, 0 };
            int retval = NodeMarkerHelper.GetTokenTypeIndex(node, node.FirstTokenIndex, node.LastTokenIndex, TSqlTokenType.Create);

            return (retval == 0) ? new int[] { -1, -1 } : new int[] { retval };
        }

        public static int[] GetTokenIndexExecuteSP(TSqlFragment node)
        {
            int retval = 0;
            var tokenIndexSP_addextendedroperty = NodeMarkerHelper.GetTokenIndexOfString(node, node.FirstTokenIndex, node.LastTokenIndex, "sp_addextendedproperty");
            if (tokenIndexSP_addextendedroperty !=0)
            {
                 retval = NodeMarkerHelper.GetTokenTypeIndex(node, node.FirstTokenIndex, node.LastTokenIndex, TSqlTokenType.Execute);
            }
            return (retval == 0) ? new int[] { -1, -1 } : new int[] { retval-2, node.LastTokenIndex +3 };
        }

    }
}
