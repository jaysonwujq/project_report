#!/usr/bin/env python
#-*-coding:utf-8-*-

#Author:    Wu Jianqiang
#Version:   v1.0

import os,re,sys,shutil
from collections import OrderedDict

class HtmlSection:
    def __init__(self,out_file,index_file):
        self.out_file = open(out_file,'w')
        self.index_file = open(index_file,'w')
    sect_cnt = {'menu_cnt':0, 'submenu_cnt':0, 'img_cnt':0, 'tab_cnt':0, 'multi_tab_num':0}

    #指定目录查找指定文件
    def search_file(self,search_path, file_name):
        all_file = []
        g= os.walk('%s'%search_path)
        for path,d,filelist in g:
            for filename in filelist:  
                all_file.append(filename)
        match_file = []
        for i in all_file:
            if re.search(r'%s'%file_name, r'%s'%i):
                match_file.append(i)
        return match_file

    def copy_file(self,src_path,out_path):
        os.system('cp -r %s/* %s'%(src_path,out_path))

    def add_begin(self):
        add_str='''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
	<head>
		<!-- 基本信息 -->
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>xx公司 结题报告</title>
		
		<!-- CSS文档 -->
		<link rel="stylesheet" type="text/css" href="css/jquery.dataTables.min.css" />
		<link rel="stylesheet" type="text/css" href="css/report.css" />
		<link rel="stylesheet" type="text/css" href="css/jumpto.css" />
		<link rel="stylesheet" type="text/css" href="css/easy-responsive-tabs.css" />

		<!-- JS脚本 -->
		<script src="js/jquery-1.9.1-min.js"></script>
		<script src="js/jquery.jumpto-min.js"></script>
		<script src="js/jquery.nicescroll-min.js"></script>
		<script src="js/easyResponsiveTabs-min.js"></script>
		<script src="js/jquery.dataTables.min.js"></script>
		<script src="js/iframe_auto.js"></script>
		<script src="js/show_help-min.js"></script>
	</head>
	<body>
		<div id="report_body">
'''
        self.out_file.write(add_str)

    def project_info(self,project_id,group_file):
        group2sample = OrderedDict()
        sample = []
        gd = open(group_file, 'r')
        for line in gd:
            if line.startswith('samples') or line.startswith('sample') or line.startswith('Sample') or line.startswith('Samples'):continue
            line = line.strip().split('\t')
            group2sample.setdefault(line[1], []).append(line[0])
            sample.append(line[0])
        gd.close()
        group_info = []
        sample_name = ', '.join(sample)
        for item in group2sample.items():
            group_info.append(item[0] + '(' + ', '.join(item[1]) + ')')
        group_info = '; '.join(group_info)
        add_str = '''
 <table border="1px" cellspacing="0px" style="margin:auto;width:80%%;border:1px #FFD39B sloid;border-collapse: collapse;font-size:14px;text-align:left;">
 <tr height=22px><td width = 10%%>项目编号</td><td>%s</td></tr>
 <tr height=22px><td width = 10%%>样品名称</td><td>%s</td></tr>
 <tr height=22px><td width = 10%%>分组信息</td><td>%s</td></tr>
 </table>
'''%(project_id, sample_name, group_info)
        self.out_file.write(add_str)

    def add_section(self, sid, sname):
        self.sect_cnt['menu_cnt'] += 1
        self.sect_cnt['submenu_cnt'] = 0
        self.sect_cnt['img_cnt'] = 0
        self.sect_cnt['tab_cnt'] = 0 
        #print self.sect_cnt['menu_cnt'],self.sect_cnt['submenu_cnt']
        add_str = r'''
<section id="%s" class="normal_cont">
<h3 >%s %s</h3>
'''%(sid, self.sect_cnt['menu_cnt'], sname)
        self.out_file.write(add_str)

    def add_subsection(self, sname):
        self.sect_cnt['submenu_cnt'] += 1
        self.sect_cnt['img_cnt'] = 0
        self.sect_cnt['tab_cnt'] = 0
        add_str = r'''
<h5 >%s.%s %s</h5>
'''%(self.sect_cnt['menu_cnt'], self.sect_cnt['submenu_cnt'], sname)
        self.out_file.write(add_str)

    def add_p(self,desc):
        add_str = r'''
<p >%s</p>
'''%desc
        self.out_file.write(add_str)

    def add_note(self,desc):
        add_str = r'''
<p style="font-size:12px;">%s</p>
'''%desc
        self.out_file.write(add_str)

    def add_html(self,desc):
        self.out_file.write(desc)

    def add_table(self, tab, tab_name, max_char=30, row_limit=51, col_limit=50, header='T', css_class='func_table nowrap',width='100',style=''):
        self.sect_cnt['tab_cnt'] += 1
        add_str = r'''
<table class="%s" width='%s%%' %s>
	<caption>Tab %s-%s-%s %s</caption>
'''%(css_class, width, style, self.sect_cnt['menu_cnt'], self.sect_cnt['submenu_cnt'], self.sect_cnt['tab_cnt'], tab_name)
        self.out_file.write(add_str)
        with open(tab,'r') as df:
            line_num = 0
            for line in df:
                line_num += 1
                line = line.strip().split('\t')[0:col_limit]
                new_line = []
                for i in line:
                    try:
                        i = round(float(i),3)
                        new_line.append(i)
                    except ValueError:
                        if len(i) > int(max_char):
                            a = i[0:int(max_char)] + '...'
                            new_line.append(a)
                        else:
                            new_line.append(i)
                if line_num > int(row_limit): break
                if line_num == 1 and header=='T':
                    add_str = ''.join(['<th>%s</th>'%i for i in new_line])
                    add_str = '\t<thead><tr>' + add_str + '</tr></thead>\n'
                    self.out_file.write(add_str + '\t<tbody>\n')
                elif line_num == 1 and header!='T':
                    add_str = ''.join(['<td>%s</td>'%i for i in new_line])
                    add_str = '\t<tbody>\n<tr>' + add_str + '</tr>\n'
                else:
                    add_str = ''.join(['<td>%s</td>'%i for i in new_line])
                    add_str = '\t\t<tr>' + add_str + '</tr>\n'
                    self.out_file.write(add_str)
        self.out_file.write('\t</tbody>\n</table>\n')

    def add_img_only(self, img, img_name):
        self.sect_cnt['img_cnt'] += 1
        add_str = r'''
<table class="pic_table">
        <tr>
                <td style="width: 50%%"><a href="%s" target="_blank"><img src="%s" /></td>
        </tr>
        <tr>
                <td class="img_title">Fig %s-%s-%s %s</td>
        </tr>
</table>
<br />
'''%(img, img, self.sect_cnt['menu_cnt'], self.sect_cnt['submenu_cnt'], self.sect_cnt['img_cnt'], img_name)
        self.out_file.write(add_str)


    def add_img(self, img, img_name, desc):
        self.sect_cnt['img_cnt'] += 1
        add_str = r'''
<table class="pic_table">
	<tr>
		<td style="width: 50%%"><a href="%s" target="_blank"><img src="%s" /></td>
		<td class="pic_table_desc" style="width: 50%%"><p>%s</p></td>
	</tr>
	<tr>
		<td class="img_title">Fig %s-%s-%s %s</td>
		<td></td>
	</tr>
</table>
<br />
'''%(img, img, desc, self.sect_cnt['menu_cnt'], self.sect_cnt['submenu_cnt'], self.sect_cnt['img_cnt'], img_name)
        self.out_file.write(add_str)

    def add_2img(self, img1, img1_name, img2, img2_name):
        self.sect_cnt['img_cnt'] += 1
        img_cnt1 = self.sect_cnt['img_cnt']
        self.sect_cnt['img_cnt'] += 1
        img_cnt2 = self.sect_cnt['img_cnt']
        add_str = r'''
<table class="pic_table">
	<tr>
		<td style="width: 45%%"><a href="%s" target="_blank"><img src="%s" /></a></td>
		<td style="width: 10%%"></td>
		<td style="width: 45%%"><a href="%s" target="_blank"><img src="%s" /></a></td>
	</tr>
	<tr>
		<td class="img_title">Fig %s-%s-%s %s</td>
		<td style="width: 10%%"></td>
		<td class="img_title">Fig %s-%s-%s %s</td>
	</tr>
	<tr>
		<td align="left"></td>
		<td style="width: 10%%"></td>
		<td align="left"></td>
	</tr>
</table>
<br />
'''%(img1, img1, img2, img2, self.sect_cnt['menu_cnt'], self.sect_cnt['submenu_cnt'], img_cnt1, img1_name, self.sect_cnt['menu_cnt'], self.sect_cnt['submenu_cnt'], img_cnt2, img2_name)
        self.out_file.write(add_str)

    def add_multi_imgs(self,imgs,img_name):
        self.sect_cnt['img_cnt'] += 1
        self.sect_cnt['multi_tab_num'] += 1
        imgs_name = [os.path.basename(img).replace('.png','').replace('_venn','') for img in imgs]
        add_str = r'''
<div id="parentVerticalTab%s" class="VerticalTab">
	<ul id="resp-tabs-list%s" class="resp-tabs-list hor_%s">
'''%(self.sect_cnt['multi_tab_num'],self.sect_cnt['multi_tab_num'],self.sect_cnt['multi_tab_num'])
        self.out_file.write(add_str)
        for i in imgs_name:
            self.out_file.write('\t\t<li>'+i+'</li>')
        add_str = r'''
	</ul>
	<div id="resp-tabs-container%s" class="resp-tabs-container hor_%s">
'''%(self.sect_cnt['multi_tab_num'],self.sect_cnt['multi_tab_num'])
        self.out_file.write(add_str)
        for i in imgs:
             self.out_file.write('<div><a href="%s" target="_blank"><img src="%s" /></a></div>\n'%(i,i))
        self.out_file.write('</div>')
        self.out_file.write('<div><p class="img_title">Fig %s-%s-%s %s</p></div>'%(self.sect_cnt['menu_cnt'], self.sect_cnt['submenu_cnt'], self.sect_cnt['img_cnt'], img_name))
        self.out_file.write('</div>')

    def add_question_section(self,sname):
        self.sect_cnt['menu_cnt'] += 1
        add_str='''
<section id="paper" class="normal_cont">
<h3 >%s %s<a href="doc/help.html#help" target="help_page" onclick="show_help();"><img src="image/help.png" class="help_logo"></a></h3>
</section>
'''%(self.sect_cnt['menu_cnt'], sname)
        self.out_file.write(add_str)
        
    def add_advert(self):
        add_str='''
<section class="normal_cont" id="advertisement">
<pre style="font-size:12px;line-height:15px;">

地址: 广东省广州市xxx402单元<img align="right" src="../src/image/wechat.jpg" width=120 heigth=120/>

电话：020-xxx     邮编：510000     微信公众号：xxx

咨询热线：xxx                　官网：<a target="_blank" href="http://xxx.com">www.xxx.com</a>

邮箱: xxx.com
</pre>
</section>
'''
        self.out_file.write(add_str)

    def add_end(self):
        add_str='''
<div id='btn_top'><img src='../src/image/gotop.png' /></ div></section>
		<!-- JS插件初始化 -->

                <!-- 帮助文档窗口 -->
                <div id="show_help">
                        <h3>帮助文档</h3>
                        <iframe id="help_page" name="help_page" src="http://http://www.magigene.com"></iframe>
                </div>
   
		<script type="text/javascript">
			$(document).ready(function() {
				
				$("#report_body").jumpto({
					innerWrapper: "section",
					firstLevel: "> h3",
					secondLevel: "> h5",
					offset: 0,
					anchorTopPadding: 0,
					animate: 600,
					showTitle: "目录",
					closeButton: false
				});
				for (var i = 1; i <= 5; i++){
					$('#resp-tabs-list' + i).niceScroll({cursoropacitymax:0.5,cursorwidth:"8px"});
					$('#resp-tabs-container' + i).niceScroll({cursoropacitymax:0.5,cursorwidth:"8px"});
					$('#parentVerticalTab' + i).easyResponsiveTabs({
						type: 'vertical', //Types: default, vertical, accordion
						width: 'auto', //auto or any width like 600px
						fit: true, // 100% fit in a container
						closed: 'accordion', // Start closed if in accordion view
						tabidentify: 'hor_' + i, // The tab groups identifier
						activate: function(event) { // Callback function if tab is switched
							var $tab = $(this);
							var $info = $('#nested-tabInfo2');
							var $name = $('span', $info);
							$name.text($tab.text());
							$info.show();
						}
					});
				}
			});

		window.onload=function(){ 
			$('.jumpto-first').css('max-height', ($(window).height()*0.98 - 48) + 'px');
			$('.jumpto-first').niceScroll({cursoropacitymax:0.5,cursorwidth:"6px",cursorborder:"0px"});
		} 

			/****表格悬浮显示全部内容****/
			function messshow (info) {
			var str='<div class="topBg"><div class="toppicBox"><div class="inBox" style="text-align:center;"><br><textarea class="pinfo" cols=56>'+info+'</textarea><br><br></div><img class="topClose" width="27" height="27" src="image/topclose.png" onclick="topclose()"></div></div>';
				  $("body").append(str);}

			function topclose(){
			$(".topBg").remove();
			}

			$(function(){
				$(".abbrTab").each(function(){
				var len=$(this).attr("data");
				var mess=$(this).text();
				$(this).attr("title",mess);
				if(mess.length>len-1){
				mess=mess.substring(0,len-1);
				mess +='<span class="brief">...</span>';
			}
				$(this).html(mess);

				});

				$(".brief").click(function(){
				var info=$(this).parent().attr("title");
				  messshow (info);
				 });
				
				$(".func_table").DataTable({"scrollX": true} );
			});
			
			$('.hl_table tr').has('td').each(function(){
				$(this).attr('onmouseover', 'this.style.backgroundColor = "#DDDDDD"');
				$(this).attr('onmouseout', 'this.style.backgroundColor = "#FFFFFF"');
			});
			
			$('.func_table tr').has('td').each(function(){
				$(this).attr('onmouseover', 'this.style.backgroundColor = "#DDDDDD"');
				$(this).attr('onmouseout', 'this.style.backgroundColor = "#FFFFFF"');
			});
			
			$(".logo").click(function(){$(window).scrollTop(0);});

                        /****返回顶部****/
                        $(function () {
                                $(window).scroll(function () {
                                        if ($(window).scrollTop() >= 200) {
                                        $('#btn_top').fadeIn();
                                }
                                else {
                                $('#btn_top').fadeOut();
                                }
                        });
                        });
                        $('#btn_top').click(function () {
                                $('html,body').animate({ scrollTop: 0 }, 500);
                        });

		</script>
	</body>
</html>	
'''
        self.out_file.write(add_str)
        self.out_file.close()

    def add_index_html(self, analyse_type):
        add_str='''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
	<head>
		<!-- 基本信息 -->
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link rel="shortcut icon" href="src/image/logo3.ico"/>
		<link rel="bookmark" href="src/image/logo3.ico"/>
		<title>xxx 结题报告</title>
		
		<!-- CSS文档 -->
		<link rel="stylesheet" type="text/css" href="src/css/index.css" />
		
		<!-- JS脚本 -->
		<script src="src/js/jquery-1.9.1-min.js"></script>
	</head>
	<body>

		<!-- 结题报告页眉 -->
		<section>
			<table id="logo_table">
				<tr>
				<td width="15%%" align="center"><img src="src/image/logo1.png" /></td>
				<td width="67%%" align="center"><span id="headtxt">美格基因<span id="analyse_type">&nbsp;%s&nbsp;</span>结题报告</span></td>
				<td width="18%%" align="right"><img src="src/image/logo2.png" /></td>
				</tr>
			</table>
		</section>

		<!-- 结题报告主内容 -->
		<section>
			<iframe id="iframepage" src="src/content.html"></iframe>
		</section>
		
		<!-- JS脚本初始化 -->
		<script language="javascript">
			function frameresize(){
				var iframeheight = $(window).height();
				$('#iframepage').css('height', iframeheight - 85 + 'px');
			};
			if(window.attachEvent){
				document.getElementById("iframepage").attachEvent('onload', frameresize);
			}
			else{
				document.getElementById("iframepage").addEventListener('load', frameresize, false);
			} 
			$(window).resize(frameresize);
			frameresize();
		</script>
	</body>
</html>
'''%(analyse_type)
        self.index_file.write(add_str)
        self.index_file.close()

if __name__ == '__main__':
    pass
