using Parsnip.Traverser;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Parsnip.NodeMarkers;
using Parsnip.Transformers;
using Parsnip.Writer;
using Parsnip.Common;
using Parsnip.Recipes;
using System.IO;

namespace Parsnip
{
    public static class MasterConductor
    {
        public static void Run()
        {
            if( LoadRecipe())
            {
                RunRecipe();
            }
        }

        private static bool LoadRecipe()
        {
            var xmlRules = SettingsReader.ReadSetting("RecipePath");
            RecipeService.Load(xmlRules);
            return RecipeService.HasRecipe();
        }

        private static void RunRecipe()
        {

                var sqlFile = SettingsReader.ReadSetting("SourceFile");
                NodeMarkerContainer myContainer = new NodeMarkerContainer();
                TraverserService traverserService = new TraverserService(myContainer, sqlFile);
                var tree = traverserService.Traverse();
                Program.log.Info("--- End Traversal and Marking ---");
                var finalScript = TransformerService.Run(tree, myContainer.NodeMarkerList);
                WriteToFileService.Write(finalScript);

        }

        public static void RunRecipe(string sqlFile, string recipeFileName)
        {
            RecipeService.Load(recipeFileName);
            NodeMarkerContainer myContainer = new NodeMarkerContainer();
            TraverserService traverserService = new TraverserService(myContainer, sqlFile);
            var tree = traverserService.Traverse();
            var finalScript = TransformerService.Run(tree, myContainer.NodeMarkerList);
            if (myContainer.NodeMarkerList.Count != 0)
            {
                WriteToFileService.Write(finalScript, sqlFile);

            }

            //WriteToFileService.Write(finalScript);

        }
    }
}
