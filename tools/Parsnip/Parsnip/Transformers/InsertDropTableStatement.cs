using Microsoft.SqlServer.TransactSql.ScriptDom;
using Parsnip.NodeMarkers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Transformers
{
    class InsertDropTableStatement : ITransformer
    {
        //public List<String> Transform(TSqlFragment tree, NodeMark nodeMark)
        //{
        //    List<string> dropTableList = new List<string>();
        //    dropTableList.Add("DROP");
        //    return new List<string>();
        //}

        public void Transform(TokenIndexMapList tokenMapList, NodeMark nodeMark)
        {
            //string drop = "IF OBJECT_ID('tempdb..#TempTable') IS NOT NULL BEGIN DROP TABLE #TempTable END";

            var tblNameIndex = nodeMark.TokenIndexes[1];
            var tblName = tokenMapList.GetTokenOfIndex(tblNameIndex);
            string[] dropTblStmnt = new string[] {"\n","IF"," ","OBJECT_ID('tempdb..",""+tblName+"","')"," ","IS"," ","NOT"," ","NULL","\n","BEGIN","\n","\t","DROP"," ","TABLE"," ", "" + tblName + "", "\n","END","\n" };

            tokenMapList.Insert(nodeMark.TokenIndexes[0], dropTblStmnt);

        }
    }
}
