using Parsnip.Common;
using log4net;
using log4net.Config;

namespace Parsnip
{
    class Program
    {
        public static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        
        // private static readonly ILog log = LogManager.GetLogger(typeof(Parsnip));
        static void Main(string[] args)
        {
            log4net.GlobalContext.Properties["LogFileName"] = Properties.Settings.Default.LogFileName;
            XmlConfigurator.Configure(new System.IO.FileInfo(SettingsReader.Log4NetConfigFile));
            log.Info("---- Begin -----");
            MasterConductor.Run();
            log.Info("---- End -----");
        }
    }
}
