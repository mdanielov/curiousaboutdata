using Parsnip.NodeMarkers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Transformers
{
    class SelectTokens: ITransformer
    {
        public void Transform(TokenIndexMapList tokenMapList, NodeMark nodeMark)
        {
            if (nodeMark.TokenIndexes.Length > 0)//added this to do nothing for null token index arrays 
            {
                if (nodeMark.TokenIndexes.Length == 2)
                {
                    tokenMapList.Select(nodeMark.TokenIndexes[0], nodeMark.TokenIndexes[1]);
                }
                else
                {
                    Enumerable
                        .Range(0, nodeMark.TokenIndexes.Length)
                        .ToList()
                        .ForEach(indx => tokenMapList.Select(nodeMark.TokenIndexes[indx], nodeMark.TokenIndexes[indx]));
                }
            }
            
        }
    }
}
