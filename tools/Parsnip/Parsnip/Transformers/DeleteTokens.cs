using Parsnip.NodeMarkers;
using System.Linq;

namespace Parsnip.Transformers
{
    class DeleteTokens: ITransformer
    {
        public void Transform(TokenIndexMapList tokenMapList, NodeMark nodeMark)
        {
            if (nodeMark.TokenIndexes.Length >0)//added this to do nothing for null token index arrays 
            {
                if(nodeMark.TokenIndexes.Length == 2)
                {
                    tokenMapList.Delete(nodeMark.TokenIndexes[0], nodeMark.TokenIndexes[1]);
                } else {
                    //Enumerable
                    //    .Range(0, nodeMark.TokenIndexes.Length)
                    //    .ToList()
                    //    .ForEach( indx => tokenMapList.Delete( indx, indx));
                    nodeMark.TokenIndexes
                        .ToList()
                        .ForEach(index => tokenMapList.Delete(index, index));
                }
            }
        }
    }
}
