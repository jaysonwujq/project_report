我们日常工作中经常会遇到需要快速给出网页版及PDF版结题报告的情况，自动化生成结题报告是一项可以节省大量时间的事情，本项目利用Python类封装了html和latex2种标记语言，可以实现短时间生成美观的报告。

Html4Report.py网页版使用方法：
#导入模块
import Html4Report
#原src文件路径
source_src_path = os.path.join(script_path, "../src")
#result_path为结果文件
out_path = os.path.join(result_path,'report')
index_html = os.path.join(out_path,'index.html')
src_path = os.path.join(out_path,'src')
if not os.path.exists(out_path):
    os.makedirs(src_path)
content_html = os.path.join(src_path,'content.html')

#实例化，初始化
html = Html4Report.HtmlSection(content_html,index_html)
html.copy_file(source_src_path,src_path)
html.add_begin()

#添加index.html
html.add_index_html(analyse_type='xxx 分析')

#添加一个section,sid为标识的id, sname为标题名称
html.add_section(sid='xxx',sname='一级标题')

#添加一个二级标题，sname为二级标题名称，注意本流程目前只能实现一、二级标题的添加。
html.add_subsection(sname='二级标题')

#添加段落
html.add_p(desc='这是一段文字描述‘)

#添加图片
html.add_img(img='图片相对路径',img_name='图片名称',desc='这是图片的描述，展示在图片右侧')

#添加表格
html.add_table(tab='表格绝对路径',tab_name='表格名称',row_limit='最大行数',col_limit='最大列数')

#添加结尾
html.add_end()

#latex2PDF.py使用方法与网页版使用方法大同小异，需要注意的是要安装latex软件（texlive）才能生成PDF报告。
