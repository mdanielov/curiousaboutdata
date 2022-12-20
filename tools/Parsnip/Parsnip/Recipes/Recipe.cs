using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Xml.Serialization;

namespace Parsnip.Recipes
{

    public class Recipe
    {
        private List<Rule> _rules;
        public List<Rule> Rules { get { return _rules; } }

        public Recipe()
        {
            _rules = new List<Rule>();

        }

        public class Rule
        {
            public string Fragment { get; set; }
            public string TokenIndexMethod { get; set; }
            public string Action { get; set; }
            public string Match { get; set; }
            public string Replace { get; set; }
            public string Format { get; set; }
            public string Comment { get; set; }

            public Rule()
            {
            }
        }

        public static Recipe XmlLoad(string recipeFileName)
        {
            using (var stream = new FileStream(recipeFileName, FileMode.Open))
            {
                return XmlDeserialize(stream);
            }
        }

        public static void XmlSerialize(Recipe recipe, StreamWriter stream)
        {
            var xmlSerializer = new XmlSerializer(typeof(Recipe));

            xmlSerializer.Serialize(stream, recipe);
        }

        public static Recipe XmlDeserialize(Stream stream)
        {
            var xmlSerializer = new XmlSerializer(typeof(Recipe));

            return (Recipe)xmlSerializer.Deserialize(stream);
        }

        public static Recipe JsonLoad(string recipeFileName)
        {
            var jsonString = File.ReadAllText(recipeFileName);
            return JsonConvert.DeserializeObject<Recipe>(jsonString);
        }

        public static void JsonSerialize(Recipe recipe, string recipeFileName)
        {
            File.WriteAllText(recipeFileName, JsonConvert.SerializeObject(recipe));
        }

        public static Recipe JsonDeserialize( string jsonString)
        {
            return JsonConvert.DeserializeObject<Recipe>(jsonString);
        }
    }
}
