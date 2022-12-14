using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.SqlServer.TransactSql.ScriptDom;


namespace Parsnip.NodeMarkers
{
    public interface INodeMarker
    {
        void Mark(TSqlFragment node);
    }
}
