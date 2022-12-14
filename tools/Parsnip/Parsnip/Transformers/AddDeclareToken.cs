using Microsoft.SqlServer.TransactSql.ScriptDom;
using Parsnip.NodeMarkers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Transformers
{
    class AddDeclareToken : ITransformer
    {
        //public List<string> Transform(TSqlFragment tree, NodeMark nodeMark)
        //{
        //    List<string> Declarelist = new List<string>();
        //    Declarelist.Add("DECLARE");
        //    Declarelist.Add(" ");
        //    return Declarelist;
        //}

        public void Transform(TokenIndexMapList tokenMapList, NodeMark nodeMark)
        {
            var insertStmnt = new string[] { "DECLARE", " " };
            tokenMapList.Insert(nodeMark.TokenIndexes[0], insertStmnt);
        }
    }
}
