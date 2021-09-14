import os
import filecmp
import sys
import configparser

config = configparser.ConfigParser()
config.read('C:/Git/cynet-work/directory_compare/settings.ini')
source_dir = config.get('compare', 'src_dir')
destination_dir = config.get('compare', 'dst_dir')
report_dir = config.get('compare', 'report_dir')
com_dirs=[]
same_files=[]
diff_files=[]
left_only=[]
right_only=[]
file_compare=[]
folder_compare=[]

def compare_directories(right_dir, left_dir):
    result = filecmp.dircmp(right_dir, left_dir)
    com_dirs.extend([os.path.join(right_dir,folder) for folder in result.common_dirs])
    same_files.extend([os.path.join(right_dir,folder) for folder in result.same_files])
    diff_files.extend([os.path.join(right_dir,folder) for folder in result.diff_files])
    left_only.extend([os.path.join(right_dir,folder) for folder in result.left_only])
    right_only.extend([os.path.join(right_dir,folder) for folder in result.right_only])

    for folder in result.common_dirs:
        for root, dirs, files in os.walk(os.path.join(right_dir,folder)):
            for name in dirs:
                compare_directories(os.path.join(right_dir,folder),os.path.join(left_dir,folder))

def sort_result_lists(dir1=source_dir, dir2=destination_dir):
    for root, dirs, files in os.walk(dir1):
        right = os.path.join(dir2,os.path.basename(root))

        for file in files:
            if os.path.join(root,file) in same_files:
                file_compare.append([os.path.join(root,file),os.path.join(root,file),"Same files"])
            elif os.path.join(root,file) in diff_files:
                file_compare.append([os.path.join(root,file),os.path.join(root,file),"Different files"])
            elif os.path.join(right,file) in right_only:
                file_compare.append("-",[os.path.join(root,file),"Missing file in {}".format(destination_dir)])
                right_only.remove(os.path.join(root,file))
            elif os.path.join(root,file) in left_only:
                file_compare.append([os.path.join(root,file),"-","Missing file in {}".format(source_dir)])
        
        for dir in dirs:
            if os.path.join(root,dir) in com_dirs:
                folder_compare.append([os.path.join(root,dir),os.path.join(root,dir),"Same Folders"])
            elif os.path.join(root,dir) in left_only:
                folder_compare.append([os.path.join(root,dir),"-","Missing Folder in {}".format(destination_dir)])
    
    for right in right_only:
        folder_compare.append(["-",right,"Missing Folder in {}".format(source_dir)])

    
      
def create_html_report():
    with open(report_dir+"report.html","w")as  report:
        html = """<html>
                <head>
                <style>
                table {
                    table-layout: auto;   
                    border: 1px solid black;
                }
                .sort_header{
                        border: solid 2px;
                }
                tr{
                                        border: 1px solid black;
                }
                th, td {
                padding: 8px;                                        
                border: 1px solid black;
                }
                .same{
                    color:green;
                }
                .missing{
                    color:red;
                }
                .different{
                    color:red;
                }                </style>
            </head>
            <body>
            <h2>Directories Compare:</h2>
            <table><tr><th>Source Directory</th><th>Destination Directory</th><th>Report</th></tr>"""
        report.write(html)
        for row in folder_compare:
            class_name = row[2].split()[0].lower()
            report.write("<tr class={}><td>{}</td><td>{}</td><td>{}</td></tr>".format(class_name,row[0],row[1],row[2]))    

        report.write("</table><h2>Files Compare:<h2><table><tr><th>Source Directory</th><th>Destination Directory</th><th>Report</th></tr>")
        for row in file_compare:
            class_name = row[2].split()[0].lower()
            report.write("<tr class={}><td>{}</td><td>{}</td><td>{}</td></tr>".format(class_name,row[0],row[1],row[2]))    

        report.write("</table></body></html>")    


if __name__ == "__main__":
    compare_directories(source_dir , destination_dir)
    sort_result_lists()
    create_html_report()
