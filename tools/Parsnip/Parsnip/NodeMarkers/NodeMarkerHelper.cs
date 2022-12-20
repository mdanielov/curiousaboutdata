using System.Collections.Generic;
using System.Linq;
using Microsoft.SqlServer.TransactSql.ScriptDom;

namespace Parsnip.NodeMarkers
{
    public static class NodeMarkerHelper
    {
        public static string GetTokenText(TSqlFragment node, int[] tokenIndexes)
        {
            if( tokenIndexes is null || tokenIndexes.Length == 0 ) { return $"{node.GetType().Name} null or no tokenIndexes";  }
            return string.Join( ",", tokenIndexes.Select(x => node.ScriptTokenStream[x].Text).ToArray());
        }

        public static int GetTokenTypeIndex(TSqlFragment node, int startIndex, int nextOrPrev, TSqlTokenType tokenType)
        {
            var len = node.LastTokenIndex - node.FirstTokenIndex;
            //var retval = node.ScriptTokenStream
            //    .Skip(startIndex + nextOrPrev)
            //    .Take(len)
            //    .Where(item => item.TokenType == tokenType)
            //    .Select((item,ii) => ii)
            //    .First<int>();

            //return retval;
            while (node.ScriptTokenStream[startIndex].TokenType != tokenType && startIndex <= node.LastTokenIndex)
            {
                startIndex = startIndex + nextOrPrev;
            }
            return startIndex;
        }

        public static int GetTokenIndexOfString(TSqlFragment node, int startIndex, int endIndex, string word)
        {
        //    var retval = node.ScriptTokenStream
        //        .Skip(startIndex)
        //        .Take(node.LastTokenIndex - node.FirstTokenIndex)
        //        .Where(item => item.Text == word)
        //        .Select(item => item)

            while (node.ScriptTokenStream[startIndex].Text != word && startIndex <= endIndex)
            {
                startIndex++;
            }
            
            if(node.ScriptTokenStream[startIndex].Text != word)
            {
                startIndex = node.LastTokenIndex;
            }
            //else
            //{
            //    startIndex--;
            //}

            return startIndex;
        }

        public static int GetNextorPrevTokenIndex(TSqlFragment node, int startIndex, int nextorprev)
        {
            //node.ScriptTokenStream
            //    .Skip(startIndex)
            //    .Take(startIndex+nextorprev)
            //    .TakeWhile(item => item.TokenType == TSqlTokenType.WhiteSpace)
            //    .Select(item => )
            while (startIndex > 0)
            {
                while (node.ScriptTokenStream[startIndex+nextorprev].TokenType == TSqlTokenType.WhiteSpace)
                {
                    startIndex = startIndex + nextorprev;

                }
                return startIndex+nextorprev;
            }
            return startIndex;
        }


    }
}
