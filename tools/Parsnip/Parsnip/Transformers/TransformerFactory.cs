using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Transformers
{
    public static class TransformerFactory
    {
        public static ITransformer GetTransformer(string action)
        {
            switch (action)
            {
                case "Delete":
                    return new DeleteTokens();
                case "DropTable":
                    return new InsertDropTableStatement();
                case "AddDeclare":
                    return new AddDeclareToken();
                case "Select":
                    return new SelectTokens();
                case "AddLine":
                    return new AddLine();
                //case "RemoveLine":
                    //return new RemoveLine();
                default:
                    return null;
            }
        }

    }
}
