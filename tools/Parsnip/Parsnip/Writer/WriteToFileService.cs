using Parsnip.Common;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Writer
{
    public static class WriteToFileService
    {
        public static void Write(string sqlOutput)
        {
            var _targetFile = SettingsReader.ReadSetting("TargetPath");
            using (var writer = new StreamWriter(_targetFile))
            {
                writer.Write(sqlOutput);
            }
        }

        public static void Write(string sqlOutput, string _targetFile)
        {
            using (var writer = new StreamWriter(_targetFile))
            {
                writer.Write(sqlOutput);
            }
        }
    }
}
