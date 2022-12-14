using Microsoft.SqlServer.TransactSql.ScriptDom;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UnitTestParsnip.TestTraversers
{
    public class VisitorProcessor : IVisitorProcessor
    {
        public TSqlFragment SqlFragment { get; set; }
        private string TSqlFragmentName { get; set; }

        public VisitorProcessor(string fragmentName)
        {
            TSqlFragmentName = fragmentName;
            SqlFragment = null;
        }

        public void Process(TSqlFragment sqlFragment)
        {
            if (sqlFragment.GetType().Name.Equals(TSqlFragmentName))
            {
                SqlFragment = sqlFragment;
            }
        }
    }
}
