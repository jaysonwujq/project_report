#!/usr/bin/env python
#-*-coding:utf-8-*-

#Author:    Wu Jianqiang
#Version:   v1.0


import os,re,sys

class latexPDF:
    def __init__(self,out_file):
        self.out_file = open(out_file,'w')

    #指定目录查找指定文件
    def search_file(self,search_path, file_name):
        all_file = []
        g= os.walk('%s'%search_path)
        for path,d,filelist in g:
            for filename in filelist:  
                all_file.append(os.path.join(path, filename))
        match_file = []
        for i in all_file:
            if re.search(r'%s'%file_name, r'%s'%i):
                match_file.append(i)
        return match_file

    #加载latex包
    def add_package(self):
        out_str = r"""\documentclass[10pt]{article}
\usepackage{supertabular}
\usepackage{geometry}
\geometry{left=2cm,right=1.5cm,top=2.5cm,bottom=2.5cm}
%设置纸张大小
\usepackage{graphicx}
\usepackage{ctex}
\usepackage{indentfirst}
\usepackage[colorlinks,linkcolor=black,anchorcolor=black,citecolor=black]{hyperref}
\usepackage{booktabs} %table
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{ctable}
%\usepackage{multirow}
\usepackage{fancyhdr}
\usepackage{setspace}
\usepackage[section]{placeins}
\usepackage[font={bf, footnotesize}, textfont=md]{caption}
\usepackage{float}
\usepackage{subfigure}
\usepackage{caption}
\makeatletter
        \newcommand\fcaption{\def\@captype{figure}\caption}
\makeatother
"""
        self.out_file.write(out_str) 

#编写页眉页脚
    def add_header(self,pic1,pic2):
        add_str = r"""
%设置页眉页脚高
\headheight 30pt
\footskip 15pt
\pagestyle{fancy}
%\lhead{\usebox{\headpic}\bfseries xxx公司} 
\lhead{\usebox{\headpic}}
%调用页眉：rhead是logo图标放在右上角，左上角为lhead，中间位chead
\newsavebox{\headpic}
"""
        add_str += r"""\sbox{\headpic}{\includegraphics[scale=0.70]{%s}}
\rhead{\usebox{\headpicr}}
\newsavebox{\headpicr}
\sbox{\headpicr}{\includegraphics[scale=0.70]{%s}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.4pt}
\cfoot{xxx公司\\-\,\thepage\,-}

"""% (pic1, pic2)
        self.out_file.write(add_str)

    #加封面
    def add_cover(self, analyse_type='Geochip'):
        add_str = r"""
\thispagestyle{empty}
\vspace*{2.5\baselineskip}
\begin{center}
\Huge\textbf{xxx%s分析结题报告}
\end{center}
\vspace*{0.58\textheight}
\setlength{\parskip}{0.6ex plus0.25ex minus0.25ex}
\par{\hspace{5.0cm}\Large 项目编号:}
\par{\hspace{5.0cm}\Large 项目类型:}
\par{\hspace{5.0cm}\Large 客户姓名:}
\par{\hspace{5.0cm}\Large 客户单位:}
\par{\hspace{5.0cm}\Large 日\hspace{1cm}期:}
\newpage

\setlength{\parskip}{0.6ex plus0.25ex minus0.25ex}
\tableofcontents\thispagestyle{empty}
\newpage
"""%analyse_type
        self.out_file.write(add_str+"\n")

    #整个pdf内容开始处，添加开始标志
    def begin(self):
        add_str = r"""
\begin{document}
"""
        self.out_file.write(add_str)

    #整个pdf内容开始处，添加结束标志
    def end(self):
        add_str = r"""
\end{document}
"""
        self.out_file.write(add_str)

    #将某页设置为页码起始，在内容的第一页添加
    def start_page_num(self):
        add_str = r"""
\pagestyle{fancy}
\setcounter{page}{1}
"""
        self.out_file.write(add_str)

    #添加一个章节，section_name为标题，desc为内容
    def add_section(self,section_name,desc=''):
        add_str = r"""
\section{%s}
\par{%s}
"""%(section_name,desc)
        self.out_file.write(add_str)

    #添加一个子章节，section_name为标题，desc为内容
    def add_subsection(self,section_name,desc='', opt=''):
        add_str = r"""
\subsection%s{%s}
\par{%s}
"""%(opt,section_name,desc)
        self.out_file.write(add_str)

    def add_subsubsection(self,section_name,desc=''):
        add_str = r"""
\subsubsection{%s}
\par{%s}
"""%(section_name,desc)
        self.out_file.write(add_str)

    #添加一段文字内容
    def add_desc(self,desc):
        add_str = r"""
    \par{%s}
""" %desc
        self.out_file.write(add_str)

    #添加一段黑体加粗文字内容
    def add_hei(self,desc):
        add_str = r"""
    \par\textbf{{%s}}
""" %desc
        self.out_file.write(add_str)


    #添加一张图片，desc为图片前说明，pic文图片路径，pic_name为该图片对应的名称，pic_note为图片注释说明
    def add_picture(self,pic,pic_name,pic_width=5,pci_height=5,desc='',pic_note=''):
        add_str = r"""
\par{%s}
\begin{figure}[H]
\centering
\includegraphics[width=%sin, height=%sin]{%s}
\caption{%s}
\end{figure}
\par{{\footnotesize{%s}}}
""" %(desc,pic_width,pci_height,pic,pic_name,pic_note)
        self.out_file.write(add_str+"\n")

    #添加并排的2张图片,合并命名,
    def add_2picture(self,pic1,pic2,desc='',pic_name='',pic_note='',caption=''):
        add_str = r"""
\par{%s}
\begin{figure}[H]
\begin{minipage}[t]{0.5\linewidth}
\centering
\includegraphics[width=3.3in]{%s}
\label{fig:side:a}
\end{minipage}
\begin{minipage}[t]{0.5\linewidth}
\centering
\includegraphics[width=3.3in]{%s}
\label{fig:side:b}
\end{minipage}
%s\caption{%s}
\end{figure}
\par{{\footnotesize{%s}}}""" %(desc,pic1,pic2,caption,pic_name,pic_note)
        self.out_file.write(add_str+"\n")

    #添加并排的2张图片,分别命名
    def add_2pictures(self,pic1,pic2,desc='',pic1_name='',pic2_name='',pic_note=''):
        add_str = r"""
\par{%s}
\begin{figure}[H]
\begin{minipage}[t]{0.5\linewidth}
\centering
\includegraphics[width=3.3in]{%s}
\caption{%s}
\label{fig:side:a}
\end{minipage}
\begin{minipage}[t]{0.5\linewidth}
\centering
\includegraphics[width=3.3in]{%s}
\caption{%s}
\label{fig:side:b}
\end{minipage}
\end{figure}
\par{{\footnotesize{%s}}}""" %(desc,pic1,pic1_name,pic2,pic2_name,pic_note)
        self.out_file.write(add_str+"\n")

    #添加表格
    def add_table(self,table,desc='',table_title='',table_note_sign='',table_note='',row_limit=20,column_limit=7,max_char=30):
        row_limit = int(row_limit)
        column_limit = int(column_limit)
        table = open(table, 'rU')
        all_lines = table.readlines()
        table.close()
        #加表格标题
        add_str = """
\par{%s}
\ctable[
caption=%s,
pos=H,
]{ccccccccccc}
{\\tnote[%s]{%s}}
{\FL
"""%(desc,table_title,table_note_sign,table_note)

        for i, v in enumerate(all_lines):
            v = v.replace('_', '\_')
            v = v.replace('%', '\%')
            v = v.replace('#', '\#')
            v = v.replace('\[', '{[')
            v = v.replace('\]', ']}')
            v = v.replace('__', '\__')
            item = v.strip().split("\t")[0:column_limit]
            items = []
            for j in item:
                try:
                    j = str(round(float(j),3))
                    items.append(j)
                except ValueError:
                    if len(j) > int(max_char):
                        a = j[0:int(max_char)] + '...'
                        items.append(a)
                    else:
                        items.append(j)

            temp_str = '&'.join(items)
            if i == 0:
                add_str += temp_str + " \\ML\n"
            elif i >= row_limit or i == len(all_lines)-1:
                add_str += temp_str + " \\LL\n"
                break
            else:
                add_str += temp_str + " \\NN\n"
        add_str += '}\n'
        self.out_file.write(add_str+"\n")

    #添加脚注
    def add_foot_note(self,desc):
        add_str = """
{\\footnotesize{%s}}
"""%desc
        self.out_file.write(add_str)
    def add_new_page(self):
        add_str = """
\\newpage
"""
        self.out_file.write(add_str)   

if __name__ == '__main__':
    pass
