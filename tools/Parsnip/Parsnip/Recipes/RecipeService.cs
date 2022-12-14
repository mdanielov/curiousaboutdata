using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Parsnip.Recipes
{
    public static class RecipeService
    {
        private static Recipe _recipe;

        public static void Load(string recipeFileName)
        {
            if( !File.Exists(recipeFileName))
            {
                Program.log.Error($"{recipeFileName} does not exist.");
                return;
            }
            try
            {
                var ext = Path.GetExtension(recipeFileName);
                if (ext.Equals(".xml", StringComparison.InvariantCultureIgnoreCase))
                {
                    _recipe = Recipe.XmlLoad(recipeFileName);
                }
                if (ext.Equals(".json", StringComparison.InvariantCultureIgnoreCase))
                {
                    _recipe = Recipe.JsonLoad(recipeFileName);
                }
            } catch( Exception e)
            {
                Program.log.Error(e.Message);
            }
        }

        public static bool HasRecipe()
        {
            return (_recipe == null || _recipe.Rules.Count == 0) ? false : true;
        }

        public static List<Recipe.Rule> GetRules(string fragment)
        {
            return (_recipe == null) ? new List<Recipe.Rule>() : _recipe.Rules.Where(item => item.Fragment == fragment).ToList();
        }
    }
}
