using Parsnip.NodeMarkers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Transformers
{
    class AddLine : ITransformer
    {
        public void Transform(TokenIndexMapList tokenMapList, NodeMark nodeMark)
        {
            if (nodeMark.TokenIndexes.Length > 0)//added this to do nothing for null token index arrays 
            {
                var insertStmnt = new string[] { $"\nInserted-" };
                tokenMapList.Insert(nodeMark.TokenIndexes[0] - 1, insertStmnt);
                insertStmnt = new string[] { $"\nSelected-" };
                tokenMapList.Insert(nodeMark.TokenIndexes[1] + 1, insertStmnt);
            }

        }
    }
}
