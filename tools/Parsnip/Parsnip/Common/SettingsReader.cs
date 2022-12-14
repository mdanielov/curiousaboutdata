using System;
using System.IO;
using System.Linq;
using System.Xml;

namespace Parsnip.Common
{
    class SettingsReader
    {
        private static XmlDocument _settingsDoc;
        private static string _settingsFilePath = null;
        public static string SettingsFilePath {  get { return _settingsFilePath;  }}
        public static string Log4NetConfigFile { get { return getLog4NetConfigFile(); } }

        public static string ReadSetting( string xmlPath)
        {
            Init();
            XmlNode Server = _settingsDoc.SelectSingleNode("root/"+xmlPath);
            return Server.InnerText;
        }

        private static string getLog4NetConfigFile()
        {
            string log4netFile = Properties.Settings.Default.Log4NetConfig ?? "Log4Net.xml";
            var parentDir = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.Parent.FullName;
            return Path.Combine(parentDir, log4netFile);
        }

        private static void Init()
        {
            if( _settingsDoc == null)
            {
                InitSettingsFilePath();
                LoadSettingsDoc();
            }
        }

        private static void InitSettingsFilePath()
        {
            if( String.IsNullOrEmpty(_settingsFilePath))
            {
                var parentDir = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.Parent.FullName;
                _settingsFilePath = Path.Combine(parentDir, "settings.xml");
            }
        }
        private static void LoadSettingsDoc()
        {

            _settingsDoc = new XmlDocument();
            _settingsDoc.Load(_settingsFilePath);
        }
    }
}
