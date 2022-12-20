using Microsoft.SqlServer.TransactSql.ScriptDom;
using Parsnip.NodeMarkers;
using System.Collections.Generic;

namespace Parsnip.Transformers
{
    public static class TransformerService
    {
        static TokenIndexMapList treeTokenIndexMapList;
        public static string Run(TSqlFragment tree, List<NodeMark> nodeMarkers)
        {
            treeTokenIndexMapList = new TokenIndexMapList(tree);
            //List<string> transformedString; 
            nodeMarkers.ForEach((item) =>
            {
                Program.log.Info(item.FormatMarker());
                var transformer = TransformerFactory.GetTransformer(item.Action);
                transformer.Transform(treeTokenIndexMapList, item);
            });
            var finalScript = string.Join("", treeTokenIndexMapList.ToStringList().ToArray());

            Program.log.Info(finalScript);
            return finalScript;
        }
    }
}
