#define DEBUG
#undef DEBUG

using Microsoft.SqlServer.TransactSql.ScriptDom;
using Parsnip.NodeMarkers;


namespace Parsnip.Traverser
{
    public class FragmentVisitor : TSqlFragmentVisitor
    {
        private NodeMarkerContainer _nodeMarkerContainer { get; set; }

        public FragmentVisitor(NodeMarkerContainer nodeMarkerContainer)
        {
            _nodeMarkerContainer = nodeMarkerContainer;
        }

        //==================================================
        // Uncomment this to display each node to be visited
        //==================================================

        public override void Visit(TSqlFragment node)
        {

#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} in Fragment Visitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in Fragment Visitor");
#endif

        }

/*


        public override void Visit(TSqlScript node)//keep 
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} in FragmentVisitor");
#endif

            _nodeMarkerContainer.Mark(node);

#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }


        public override void Visit(ReturnStatement node)//keep 
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} in FragmentVisitor");
#endif

            _nodeMarkerContainer.Mark(node);

#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

        public override void Visit(InsertStatement node)//keep
        {

#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} in FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif

        }


        public override void Visit(CreateProcedureStatement node)
        {
# if (DEBUG) 
            Program.log.Info($"BEGIN {node.GetType().Name} in FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

        public override void Visit(AlterProcedureStatement node)
        {

#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} in FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }


        public override void Visit(CreateTableStatement node)
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} in FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }


        public override void Visit(SetOnOffStatement node)
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

        public override void Visit(TryCatchStatement node)
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

        public override void Visit(BeginEndBlockStatement node)
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

        public override void Visit(ProcedureParameter node)
        {
#if DEBUG
            Program.log.Info("BEGIN Procedure Parameter in FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

        public override void Visit(NamedTableReference node)
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

        public override void Visit(PredicateSetStatement node)
        {
#if DEBUG
            Program.log.Info($"BEGIN {node.GetType().Name} FragmentVisitor");
#endif
            _nodeMarkerContainer.Mark(node);
#if DEBUG
            Program.log.Info($"END {node.GetType().Name} in FragmentVisitor");
#endif
        }

*/

    }
}
