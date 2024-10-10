
namespace Parsley
{
    partial class ParsleyForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.grpBoxRecipes = new System.Windows.Forms.GroupBox();
            this.radBtnRemoveGrant = new System.Windows.Forms.RadioButton();
            this.radBtnTables = new System.Windows.Forms.RadioButton();
            this.radBtnTestScript = new System.Windows.Forms.RadioButton();
            this.radbtnExecute = new System.Windows.Forms.RadioButton();
            this.btnClearOneFle = new System.Windows.Forms.Button();
            this.lblCount = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.btnParseFiles = new System.Windows.Forms.Button();
            this.btnFindSqlFiles = new System.Windows.Forms.Button();
            this.lstBoxFiles = new System.Windows.Forms.ListBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.txtFolderPath = new System.Windows.Forms.TextBox();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.btnClearFiles = new System.Windows.Forms.Button();
            this.btnFindDirectory = new System.Windows.Forms.Button();
            this.grpBoxRecipes.SuspendLayout();
            this.SuspendLayout();
            // 
            // grpBoxRecipes
            // 
            this.grpBoxRecipes.Controls.Add(this.radBtnRemoveGrant);
            this.grpBoxRecipes.Controls.Add(this.radBtnTables);
            this.grpBoxRecipes.Controls.Add(this.radBtnTestScript);
            this.grpBoxRecipes.Controls.Add(this.radbtnExecute);
            this.grpBoxRecipes.Location = new System.Drawing.Point(19, 200);
            this.grpBoxRecipes.Name = "grpBoxRecipes";
            this.grpBoxRecipes.Size = new System.Drawing.Size(147, 140);
            this.grpBoxRecipes.TabIndex = 27;
            this.grpBoxRecipes.TabStop = false;
            this.grpBoxRecipes.Text = "Recipes";
            // 
            // radBtnRemoveGrant
            // 
            this.radBtnRemoveGrant.AutoSize = true;
            this.radBtnRemoveGrant.Location = new System.Drawing.Point(19, 111);
            this.radBtnRemoveGrant.Name = "radBtnRemoveGrant";
            this.radBtnRemoveGrant.Size = new System.Drawing.Size(121, 21);
            this.radBtnRemoveGrant.TabIndex = 14;
            this.radBtnRemoveGrant.TabStop = true;
            this.radBtnRemoveGrant.Text = "Remove Grant";
            this.radBtnRemoveGrant.UseVisualStyleBackColor = true;
            // 
            // radBtnTables
            // 
            this.radBtnTables.AutoSize = true;
            this.radBtnTables.Location = new System.Drawing.Point(19, 83);
            this.radBtnTables.Name = "radBtnTables";
            this.radBtnTables.Size = new System.Drawing.Size(76, 21);
            this.radBtnTables.TabIndex = 13;
            this.radBtnTables.TabStop = true;
            this.radBtnTables.Text = "Tables ";
            this.radBtnTables.UseVisualStyleBackColor = true;
            // 
            // radBtnTestScript
            // 
            this.radBtnTestScript.AutoSize = true;
            this.radBtnTestScript.Location = new System.Drawing.Point(19, 55);
            this.radBtnTestScript.Name = "radBtnTestScript";
            this.radBtnTestScript.Size = new System.Drawing.Size(97, 21);
            this.radBtnTestScript.TabIndex = 12;
            this.radBtnTestScript.TabStop = true;
            this.radBtnTestScript.Text = "Test Script";
            this.radBtnTestScript.UseVisualStyleBackColor = true;
            this.radBtnTestScript.CheckedChanged += new System.EventHandler(this.radBtnTestScript_CheckedChanged);
            // 
            // radbtnExecute
            // 
            this.radbtnExecute.AutoSize = true;
            this.radbtnExecute.Location = new System.Drawing.Point(19, 26);
            this.radbtnExecute.Name = "radbtnExecute";
            this.radbtnExecute.Size = new System.Drawing.Size(127, 21);
            this.radbtnExecute.TabIndex = 11;
            this.radbtnExecute.TabStop = true;
            this.radbtnExecute.Text = "Execute Recipe";
            this.radbtnExecute.UseVisualStyleBackColor = true;
            // 
            // btnClearOneFle
            // 
            this.btnClearOneFle.Location = new System.Drawing.Point(494, 378);
            this.btnClearOneFle.Name = "btnClearOneFle";
            this.btnClearOneFle.Size = new System.Drawing.Size(120, 38);
            this.btnClearOneFle.TabIndex = 26;
            this.btnClearOneFle.Text = "Clear File";
            this.btnClearOneFle.UseVisualStyleBackColor = true;
            this.btnClearOneFle.Click += new System.EventHandler(this.btnClearOneFle_Click_1);
            // 
            // lblCount
            // 
            this.lblCount.AutoSize = true;
            this.lblCount.Location = new System.Drawing.Point(297, 392);
            this.lblCount.Name = "lblCount";
            this.lblCount.Size = new System.Drawing.Size(0, 17);
            this.lblCount.TabIndex = 25;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(202, 392);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(79, 17);
            this.label3.TabIndex = 24;
            this.label3.Text = "File Count: ";
            // 
            // btnParseFiles
            // 
            this.btnParseFiles.Location = new System.Drawing.Point(620, 378);
            this.btnParseFiles.Name = "btnParseFiles";
            this.btnParseFiles.Size = new System.Drawing.Size(166, 38);
            this.btnParseFiles.TabIndex = 23;
            this.btnParseFiles.Text = "Parse Selected Files";
            this.btnParseFiles.UseVisualStyleBackColor = true;
            this.btnParseFiles.Click += new System.EventHandler(this.btnParseFiles_Click_1);
            // 
            // btnFindSqlFiles
            // 
            this.btnFindSqlFiles.Location = new System.Drawing.Point(9, 135);
            this.btnFindSqlFiles.Name = "btnFindSqlFiles";
            this.btnFindSqlFiles.Size = new System.Drawing.Size(168, 38);
            this.btnFindSqlFiles.TabIndex = 21;
            this.btnFindSqlFiles.Text = "Find SQL files";
            this.btnFindSqlFiles.UseVisualStyleBackColor = true;
            this.btnFindSqlFiles.Click += new System.EventHandler(this.btnFindSqlFiles_Click);
            // 
            // lstBoxFiles
            // 
            this.lstBoxFiles.FormattingEnabled = true;
            this.lstBoxFiles.HorizontalScrollbar = true;
            this.lstBoxFiles.ItemHeight = 16;
            this.lstBoxFiles.Location = new System.Drawing.Point(195, 118);
            this.lstBoxFiles.Name = "lstBoxFiles";
            this.lstBoxFiles.SelectionMode = System.Windows.Forms.SelectionMode.MultiExtended;
            this.lstBoxFiles.Size = new System.Drawing.Size(752, 244);
            this.lstBoxFiles.TabIndex = 20;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(189, 92);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(141, 17);
            this.label2.TabIndex = 19;
            this.label2.Text = "Sql Files in Directory:";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(197, 35);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(85, 17);
            this.label1.TabIndex = 18;
            this.label1.Text = "Folder Path:";
            // 
            // txtFolderPath
            // 
            this.txtFolderPath.Location = new System.Drawing.Point(197, 55);
            this.txtFolderPath.Name = "txtFolderPath";
            this.txtFolderPath.Size = new System.Drawing.Size(755, 22);
            this.txtFolderPath.TabIndex = 17;
            this.txtFolderPath.TextChanged += new System.EventHandler(this.txtFolderPath_TextChanged_1);
            // 
            // folderBrowserDialog1
            // 
            this.folderBrowserDialog1.Description = "Choose a File or Folder";
            this.folderBrowserDialog1.RootFolder = System.Environment.SpecialFolder.Windows;
            this.folderBrowserDialog1.SelectedPath = "C:\\Git";
            this.folderBrowserDialog1.ShowNewFolderButton = false;
            // 
            // btnClearFiles
            // 
            this.btnClearFiles.Location = new System.Drawing.Point(370, 378);
            this.btnClearFiles.Name = "btnClearFiles";
            this.btnClearFiles.Size = new System.Drawing.Size(118, 38);
            this.btnClearFiles.TabIndex = 22;
            this.btnClearFiles.Text = "Clear All Files";
            this.btnClearFiles.UseVisualStyleBackColor = true;
            this.btnClearFiles.Click += new System.EventHandler(this.btnClearFiles_Click);
            // 
            // btnFindDirectory
            // 
            this.btnFindDirectory.BackColor = System.Drawing.SystemColors.ButtonFace;
            this.btnFindDirectory.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btnFindDirectory.Location = new System.Drawing.Point(9, 51);
            this.btnFindDirectory.Name = "btnFindDirectory";
            this.btnFindDirectory.Size = new System.Drawing.Size(168, 38);
            this.btnFindDirectory.TabIndex = 16;
            this.btnFindDirectory.Text = "Navigate to Directory";
            this.btnFindDirectory.UseVisualStyleBackColor = false;
            this.btnFindDirectory.Click += new System.EventHandler(this.btnFindDirectory_Click);
            // 
            // ParsleyForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(967, 450);
            this.Controls.Add(this.grpBoxRecipes);
            this.Controls.Add(this.btnClearOneFle);
            this.Controls.Add(this.lblCount);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.btnParseFiles);
            this.Controls.Add(this.btnFindSqlFiles);
            this.Controls.Add(this.lstBoxFiles);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.txtFolderPath);
            this.Controls.Add(this.btnClearFiles);
            this.Controls.Add(this.btnFindDirectory);
            this.Name = "ParsleyForm";
            this.Text = "Sql File Parser";
            this.grpBoxRecipes.ResumeLayout(false);
            this.grpBoxRecipes.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox grpBoxRecipes;
        private System.Windows.Forms.RadioButton radBtnRemoveGrant;
        private System.Windows.Forms.RadioButton radBtnTables;
        private System.Windows.Forms.RadioButton radBtnTestScript;
        private System.Windows.Forms.RadioButton radbtnExecute;
        private System.Windows.Forms.Button btnClearOneFle;
        private System.Windows.Forms.Label lblCount;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button btnParseFiles;
        private System.Windows.Forms.Button btnFindSqlFiles;
        private System.Windows.Forms.ListBox lstBoxFiles;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtFolderPath;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.Button btnClearFiles;
        private System.Windows.Forms.Button btnFindDirectory;
    }
}

