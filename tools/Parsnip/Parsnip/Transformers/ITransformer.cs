using Microsoft.SqlServer.TransactSql.ScriptDom;
using Parsnip.NodeMarkers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Transformers
{
    public interface ITransformer
    {
        void Transform(TokenIndexMapList tokenMapList, NodeMark nodeMark);
    }
}
