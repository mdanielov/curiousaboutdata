using Microsoft.SqlServer.TransactSql.ScriptDom;
using System;
using static Parsnip.Recipes.Recipe;

namespace Parsnip.NodeMarkers
{
    public class NodeMarker : INodeMarker
    {
        public NodeMarkerContainer Container { get; set; }

        public void Mark(TSqlFragment node)
        {
            try
            {


                Recipes.RecipeService.GetRules(node.GetType().Name).ForEach(rule =>
               {
                   processRule(rule, node);
               });
            }
            catch(Exception e)
            {
                Program.log.Info(e.Message+" "+ e.StackTrace);
            }
        }

        private void processRule(Rule rule, TSqlFragment node)
        {
            try
            {
                var tokenIndexes = TokenIndexMethodsServer.GetTokenIndexes(rule.TokenIndexMethod, node);
                var sqlStmnt = NodeMarkerHelper.GetTokenText(node, tokenIndexes);
                InsertNodeMarker(node.GetType().Name, tokenIndexes, rule.Action, sqlStmnt);
                Program.log.Info($"{rule.Fragment} {rule.Action}: {sqlStmnt}");
            } catch( Exception e)
            {
                Program.log.Error($"{rule.Fragment} {rule.Action} {rule.TokenIndexMethod}] {e.Message}");

            }
        }

        protected int[] GetTokenIndexes(TSqlFragment node) { return new int[2] { 0, 0 }; }

        protected void GetIndexesAndInsertMarker(TSqlFragment node, string action)
        {
            Program.log.Info($"BEGIN {this.GetType().Name}");
            var tokenIndexes = GetTokenIndexes(node);
            var sqlStmnt = NodeMarkerHelper.GetTokenText(node, tokenIndexes);
            InsertNodeMarker(node.GetType().Name, tokenIndexes, action, sqlStmnt);
            Program.log.Info(sqlStmnt);
            Program.log.Info($"END {this.GetType().Name}");
        }

        protected void InsertNodeMarker(string nodeType, int[] tokenIndexes, string action, string sqlStmnt)
        {
            if (Container != null)
            {
                Container.InsertNodeMarker(nodeType, tokenIndexes, action, sqlStmnt);
            }
        }

    }
}
