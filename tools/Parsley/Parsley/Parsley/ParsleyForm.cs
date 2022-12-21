using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Parsnip;

namespace Parsley
{
    public partial class ParsleyForm : Form
    {
        string DirectoryPath = "";
        string RecipeName = "";
        string[] AllFiles;
        public ParsleyForm()
        {
            InitializeComponent();
        }

        private void btnFindDirectory_Click(object sender, EventArgs e)
        {
            using (var fbd = new FolderBrowserDialog())
            {
                DialogResult result = fbd.ShowDialog();
                if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(fbd.SelectedPath))
                {
                    DirectoryPath = fbd.SelectedPath;
                    txtFolderPath.Text = DirectoryPath;
                }
            }

        }

        private void btnClearFiles_Click(object sender, EventArgs e)
        {
            lstBoxFiles.Items.Clear();
            lblCount.Text = lstBoxFiles.Items.Count.ToString();
        }

        private void btnFindSqlFiles_Click(object sender, EventArgs e)
        {
            if (DirectoryPath == "")
            {
                MessageBox.Show("You need to choose a directory.", "Message");
                return;
            }
            AllFiles = Directory.GetFiles(DirectoryPath, "*.sql", SearchOption.AllDirectories);

            foreach (var file in AllFiles)
            {
                lstBoxFiles.Items.Add(file);
            }

            //System.Windows.Forms.MessageBox.Show("Files found: " + AllFiles.Length.ToString(), "Message");
            lblCount.Text = lstBoxFiles.Items.Count.ToString();
        }

        private void GetRecipeName()
        {
            if (radbtnExecute.Checked)
            {
                RecipeName = "ExecuteRecipe.xml";
            }
            else if (radBtnRemoveGrant.Checked)
            {
                RecipeName = "RemoveGrantRecipe.xml";
            }
            else if (radBtnTables.Checked)
            {
                RecipeName = "TableRecipe.xml";
            }
            else if (radBtnTestScript.Checked)
            {
                RecipeName = "testScriptRecipe.xml";
            }
        }

        private void txtFolderPath_TextChanged_1(object sender, EventArgs e)
        {
            DirectoryPath = txtFolderPath.Text;
        }

        private void btnParseFiles_Click_1(object sender, EventArgs e)
        {

            GetRecipeName();

            if (DirectoryPath == "" || RecipeName == "" || lstBoxFiles.SelectedItems.Count == 0)
            {
                MessageBox.Show("You need to choose a recipe and files to parse.", "Message");
                return;

            }
            var parentPath = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory()).Parent.Parent.Parent.Parent.FullName, "Parsnip\\Recipes\\");
            //var curFiles = ;
            foreach (var curSqlFile in lstBoxFiles.SelectedItems)
            {
                var recipePath = Path.Combine(parentPath, RecipeName);
                txtFolderPath.Text = recipePath;
                MasterConductor.RunRecipe(curSqlFile.ToString(), recipePath);
            }
            System.Windows.Forms.MessageBox.Show("Completed parsing files successfully", "Message");

        }

        private void btnClearOneFle_Click_1(object sender, EventArgs e)
        {
            if (lstBoxFiles.SelectedIndex == -1)
            {
                MessageBox.Show("Please select an Item first!");
            }
            else
            {
                lstBoxFiles.Items.RemoveAt(lstBoxFiles.SelectedIndex);
                lblCount.Text = lstBoxFiles.Items.Count.ToString();

            }
        }

        private void radBtnTestScript_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}
