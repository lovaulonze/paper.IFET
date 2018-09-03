import re
import os, os.path
import shutil
import glob
import subprocess
import multiprocessing
from multiprocessing import Pool
import warnings
import re



# color definition
class TColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# tex_file = "paper.tex"
# tex_tmp = "tmp.tex"

# Replace the ref with bbl
def tex_process(tex_file):
    if tex_file is None:
        return False
    file_base, ext = os.path.splitext(tex_file)
    if ext not in (".tex", ".latex", ".xelatex", "xetex"):
        raise NameError("File is not a tex file!")
    
    bbl_file = file_base + ".bbl.bak"
    bbl_content = None
    with open(bbl_file, "r", encoding="utf-8") as fo:
        bbl_content = fo.read()
    pattern = re.compile("emph\{(\d+)\}([\s,]+)")
    # for i, line in enumerate(bbl_content):
        # res = re.findall(pattern, line)
        # if (len(res) > 0) and ("," not in res[1]):
    new_content = re.sub(pattern,
                         "emph{\\1}, ",
                         bbl_content)
        
    contents = []
    with open(tex_file, "r", encoding="utf-8") as fo:
        contents = fo.readlines()
        # Modify the title and date
        for i, line in enumerate(contents):
            if "thebiblio" in line:
                print("Not converted!")
                return False         # already converted?
            if re.search("\\\\bibliographystyle\{\w+\}", line) is not None:
                contents[i] = "%" + line
            if re.search("\\\\bibliography\{\w+\}", line) is not None:
                contents[i] = "%" + line + new_content
        
        # contents[i] = contents[i] + new_content
    # out_file = file_base + "_adv_mate.tex"
    out_file = tex_file
    with open(out_file, "w", encoding="utf-8") as fw:
        fw.writelines(contents)
    print("Converted!")


if __name__ == "__main__":
    import sys
    try:
        ifile = sys.argv[1]
    except IndexError:
        ifile = None
    file_list = []
    # TeX process
    if tex_process(ifile):
        print(TColors.OKBLUE + "Converted TeX file: {}".format(ifile) + TColors.ENDC)

    # PDF Process 
    # for ifile in glob.glob(os.path.join(RAW_PATH, "*.pdf")):
    #     if img_path is None:
    #         file_list.append((ifile))
    #     else:
    #         file_list.append((ifile, img_path))
    # N_cores = multiprocessing.cpu_count()
    # # multicore
    # with Pool(N_cores) as p:
    #     p.map(convert_pdf, file_list)
