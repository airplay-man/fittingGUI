# -*- coding: utf-8 -*-

"""
for some versions
    delete:
        plt.rcParams["legend.edgecolor"] = 'black'
    overwrite:
        NavigationToolbar2Tk -> NavigationToolbar2TkAgg
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as dialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from module import calculation as cal
from module import graph as graph
from module import tkintertool_ima as tkima

'''if you add a function

1.  add it to FUNC_NAMES and FUNC_FOMULA
2.  add its initparams to INITPARAMS
3.  remember funcnumber as its index in FUNC_NAMES etc.
    (ex. Rabi:3, Sin:7)
4.  search "if you add a function" and follow senteces
5.  write the function into module/calculation
'''

PATH = os.path.abspath(os.path.dirname(__file__))

FUNC = [cal.SaturationCurve, cal.InversionCurve, cal.BuildUpCurve, cal.Rabi, cal.Ndegree, None, cal.Gaussian, cal.Sin]
FUNC_NAMES = ("SaturationCurve", "InversionCurve", "BuildUpCurve", "Rabi", "Ndegree", "(No fitting)", "Gaussian", "Sin")
FUNC_FOMULA = [ "a * exp(-x/b)", "a * exp(-x/b) + c", "a * (1 - exp(-x/b))", "a * exp(-x/b) * sin(c*x)", "ax^(n) + bx^(n-1) + ...",
                "-", "(1/sqrt[2*pi*a]) * exp(-(x-b)^2/2a^2)", "a * sin(b*x + c) + d"]
WHATPARAM = ["a:", "b:", "c:", "d:", "e:", "f:", 'g:', 'h:']
INITPARAMS = [np.array([1, 1]), np.array([1, 1, 0]), np.array([1, 1]), np.array([1, 1, 1]), np.array([1, 1, 1, 1, 1, 1, 1]), np.array([0, 0]), np.array([1, 1]), np.array([1, 1, 0, 0])]

MARKER = ("o", ".", ",","None", "v", ">", "<", "^", "+", "x", '*', '|', "_", "D", "d", "h", "H", "p", "8", "1", "2", "3", "4")
LINESTYLE = ('solid', 'dashed', 'dashdot', 'dotted')
LINESTYLE_scatter = ('None', 'solid', 'dashed', 'dashdot', 'dotted')
LOC = ('best', 'center', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center')
COLORdict = graph.COLORdict
COLORS = graph.COLORS

plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["legend.fancybox"] = False
# plt.rcParams["legend.edgecolor"] = 'black'

class Application():
    def __init__(self, master=None):
        '''
        note
            self.pagenum:全ページ数
            self.cp:今見ているページ番号(currentpage)
            self.cf[i]:iページ目で使っている関数ナンバー
            self.degrees:多項式関数を用いた時の次元

            self.popts[i][j]:iページ目のフィッティングで求めたj番目のパラメータ
            self.pcovs[i][j]:
            self.perrs[i][j]:iページ目のフィッティングで求めたj番目の誤差

            self.popup_flags:
                ポップアップウィンドウtk.Toplevelを連打できないようにする
                要素は前から[openボタン、multidataボタン、viewボタン、色選択ボタン]を押した時に出てくる奴
        '''
        self.master = master
        self.master.geometry("1300x1000")
        self.dirs = []
        self.files = []
        self.datas = []
        self.titles = []

        self.pagenum = 1
        self.cp = 1
        self.cf = [5]
        self.degrees = [2]

        self.pageframes = []
        self.graphframes= []
        self.funccomboxes = []
        self.func_fomula_strings = []
        self.funclabels = []
        self.scattersettings = []
        self.fittingsettings = []
        self.legendsettings = []
        self.fontsettings = []
        self.graph_flags = []
        self.titlestrs = []
        self.titlelabels = []
        self.ranges = []
        self.rangeentries = []
        self.rangeframes = []
        self.xunitentries = []
        self.yunitentries = []
        self.xlabelentries = []
        self.ylabelentries = []
        self.initparamframes = []
        self.initparamentries = []
        self.canvases = []
        self.toolbars = []
        self.popentries = []
        self.errentries = []
        self.resultframes = []
        self.initparams = INITPARAMS
        self.pageicons = []
        self.multidata_flags = []
        self.graphbooleanvars = []
        self.popup_flags = [False, False, False, False]
        self.degreeframes = []
        self.usepage = []

        self.popts = []
        self.pcovs = []
        self.perrs = []
        self.widgets_init()

    '''------------------------------GUIの関数------------------------------'''

    def widgets_init(self):
        '''
        widgets
            self.baseframe:全ページの下地

            self.pageiconframe:ページ番号選択ボタンの親フレーム
            self.addpageicon:ページを増やす+ボタン

        配置(self.master)
            row:
                0   空白20
                1   self.pageiconframe(minsize=20)
                2   空白20
                3   self.baseframe(weight=1)

            column:
                0   空白20
                1   self.pageiconframe, self.baseframe
        '''
        tkima.grid_config(  self.master,
                            rlist=[[(0, 1, 2), 'minsize', 20], [3, 'weight', 1]],
                            clist=[[0, 'minsize', 20], [1, 'weight', 1]])

        self.pageiconframe = tkima.Frame(self.master, bg='white', row=1, column=1, sticky='nswe')
        tkima.grid_config(self.pageiconframe, clist=[[0, 'minsize', 3], [1, 'minsize', 5]])

        self.baseframe = tkima.Frame(self.master, row=3, column=1, sticky='nswe')
        tkima.grid_config(self.baseframe, rlist=[[0, 'weight', 1]], clist=[[0, 'weight', 1]])

        self.widgets_main()

        self.addpageicon = tkima.Label(self.pageiconframe, text="+", bg='LightSkyBlue1', row=0, column=1)
        self.addpageicon.bind("<ButtonRelease-1>", self.add)
        self.pageicon_widgets()

    def widgets_main(self):
        '''
        widgets
        (self.baseframeの上)
            self.pageframes[i]:iページ目の下地(これらをtk.raise()することでページを切り替える)

        (self.pageframes[i]の上)
            self.titlelabels[i](row=0, column=0, columnspan=3):pathを載せる

            self.graphframes[i](row=2, column=0, rowspan=10):描画するCanvasがでる
            self.resultframes[i](row=14, column=0):各パラメータとその誤差がでる(gridはfittingしてから)

            self.funccomboxes[i](row=2, column=2)
            self.funclabels[i](row=3, column=2)
            self.rangeframes[i][0](row=5, column=2):xの情報
            self.rangeframes[i][1](row=7, column=2):yの情報
            self.initparamframes[i](row=9, column=2)
            self.buttonframes[i](row=11, column=1, columnspan=2)

        '''
        tkima.Frame(self.baseframe, bg='white', row=0, column=0, sticky='nswe', list=self.pageframes)

        self.ranges.append([])

        tkima.grid_config(  self.pageframes[self.pagenum-1],
                            rlist=[[0, 'minsize', 2], [1, 'minsize', 2], [4, 'minsize', 2], [6, 'minsize', 2], [8, 'minsize', 2], [10, 'minsize', 2]],
                            clist=[[0, 'weight', 3], [1, 'weight', 1], [2, 'weight', 1]])

        #タイトルを作る
        self.title_widgets()
        #グラフ関係の準備
        self.graph_widgets()
        #関数の種類を選ぶところ
        self.funccombo_widgets()
        #関数の概要を表示するところ
        self.funclabel_widgets()
        #次元を表示するところ
        self.degree_widgets()
        #レンジを入力するところ
        self.range_widgets()
        #初期値
        self.initparam_widgets()
        #実行ボタン
        self.button_widgets()
        #表示設定集
        self.set_viewsettings()
        #その他
        self.set_iroiro()
        #結果表示Frame
        tkima.Frame(self.pageframes[self.pagenum-1], grid=False, list=self.resultframes)

    def title_widgets(self):
        '''
        タイトル欄を作る

        note
            self.titlestrs[page]:タイトルの文字のみ
            self.titlelabels[page]:その文字を表示するLabel
        '''
        tkima.StringVar(set='', list=self.titlestrs)
        tkima.Label(self.pageframes[self.pagenum-1], textvariable=self.titlestrs[self.pagenum-1], row=0, column=0, columnspan=3, list=self.titlelabels)

    def graph_widgets(self):
        '''
        グラフ欄を作る

        note
            self.graphframes[page]:グラフを貼り付けるフレーム
            self.graph_flags[page]:そのページにグラフが表示されているかを示すT/F
        '''
        tkima.Frame(self.pageframes[self.pagenum-1], propagate=True, bg='gray', row=2, column=0, sticky='nswe', rowspan=10, list=self.graphframes)
        self.graph_flags.append(False)


    def funccombo_widgets(self):
        '''
        関数選択欄を作る

        note
            self.funccomboxes[page]:関数選択Combobox
        '''
        tkima.Label(self.pageframes[self.pagenum-1], text="func", row=2, column=1, sticky='e')
        tkima.Combobox(self.pageframes[self.pagenum-1], value=FUNC_NAMES, state='readonly', init=5, row=2, column=2, list=self.funccomboxes)
        self.funccomboxes[self.pagenum-1].bind("<<ComboboxSelected>>", self.changefunccombo(index=self.pagenum-1))

    def funclabel_widgets(self):
        '''
        選んだ関数の式を示すラベルを作る

        note
            self.func_fomula_strings[page]:関数の式の文字のみ
            self.funclabels[page]:その文字を表示するLabel
        '''
        tkima.StringVar(set=FUNC_FOMULA[5], list=self.func_fomula_strings)
        tkima.Label(self.pageframes[self.pagenum-1], textvariable=self.func_fomula_strings[self.pagenum-1], row=3, column=2, list=self.funclabels)

    def degree_widgets(self):
        '''
        多項式関数を選んだ場合の何次関数かを選ぶComboboxを置くFrameを作る

        note
            self.degreeframe[page]:上記のFrame
        '''
        tkima.Frame(self.pageframes[self.pagenum-1], row=3, column=1, sticky='e', list=self.degreeframes)

    def range_widgets(self):
        '''
        xとyの範囲を設定するところを作る

        note
            self.rangeframes[page][0]:x
            self.rangeframes[page][1]:y

            self.rangeentry_widgets():入力欄を作る
        '''
        tkima.Label(self.pageframes[self.pagenum-1], text="x", bg='plum', row=5, column=1, sticky='e')
        tkima.Label(self.pageframes[self.pagenum-1], text="y", bg='light coral', row=7, column=1, sticky='e')
        self.rangeframes.append([])
        tkima.Frame(self.pageframes[self.pagenum-1], highlightthickness=2, highlightbackground='plum', row=5, column=2, list=self.rangeframes[self.pagenum-1])
        tkima.Frame(self.pageframes[self.pagenum-1], highlightthickness=2, highlightbackground='light coral', row=7, column=2, list=self.rangeframes[self.pagenum-1])
        self.rangeentry_widgets()

    def rangeentry_widgets(self):
        '''
        self.rangeframes[page]に入力欄を作る

        note
            self.xlabelentries[page]:x軸ラベルの入力Entry
            self.ylabelentries[page]:y軸ラベルの入力Entry
            self.rangeentries[page][0]:xstartのEntry
            self.rangeentries[page][1]:xendのEntry
            self.rangeentries[page][2]:ystartのEntry
            self.rangeentries[page][3]:yendのEntry
            self.xunitentries[page]:xの単位のEntry
            self.yunitentries[page]:yの単位のEntry
        '''
        tkima.Entry(self.rangeframes[self.pagenum-1][0], width=15, row=0, column=0, columnspan=3, list=self.xlabelentries)
        tkima.Entry(self.rangeframes[self.pagenum-1][1], width=15, row=0, column=0, columnspan=3, list=self.ylabelentries, init="Signal Intensity")

        self.rangeentries.append([])
        tkima.Entry(self.rangeframes[self.pagenum-1][0], width=5, row=1, column=0, list=self.rangeentries[self.pagenum-1])
        tkima.Label(self.rangeframes[self.pagenum-1][0], text=" ~ ", row=1, column=1)
        tkima.Entry(self.rangeframes[self.pagenum-1][0], width=5, row=1, column=2, list=self.rangeentries[self.pagenum-1])

        tkima.Entry(self.rangeframes[self.pagenum-1][1], width=5, row=1, column=0, list=self.rangeentries[self.pagenum-1])
        tkima.Label(self.rangeframes[self.pagenum-1][1], text=" ~ ", row=1, column=1)
        tkima.Entry(self.rangeframes[self.pagenum-1][1], width=5, row=1, column=2, list=self.rangeentries[self.pagenum-1])

        for i in range(2):
            tkima.Label(self.rangeframes[self.pagenum-1][i], text=" [", row=2, column=0)
        tkima.Entry(self.rangeframes[self.pagenum-1][0], width=5, row=2, column=1, list=self.xunitentries)
        tkima.Entry(self.rangeframes[self.pagenum-1][1], width=5, init="a.u.", row=2, column=1, list=self.yunitentries)
        for i in range(2):
            tkima.Label(self.rangeframes[self.pagenum-1][i], text="] ", row=2, column=2)

    def initparam_widgets(self):
        '''
        初期値入力欄を作る

        note
            self.initparamframes[page]:self.initparam_entries()で初期値入力widgetsを配置する
        '''
        tkima.Frame(self.pageframes[self.pagenum-1], row=9, column=2, list=self.initparamframes)
        self.initparamentries.append([])
        self.initparam_entries()
        tkima.Label(tk.Frame(self.pageframes[self.pagenum-1]), text='initparam', row=9, column=1, sticky='e')

    def button_widgets(self):
        '''
        ボタン配置欄を作る

        note
            buttonframes:ボタンを貼り付けるフレーム
        '''
        buttonframes = tkima.Frame(self.pageframes[self.pagenum-1], row=11, column=1, columnspan=2)
        tkima.grid_config(buttonframes, clist=[[3, 'minsize', 50]])
        tkima.Button(buttonframes, text="OPEN", command=self.fitting, row=0, column=0)
        tkima.Button(buttonframes, text="RELOAD", command=self.reload, row=0, column=1)
        tkima.Button(buttonframes, text="SYNTH", command=self.multidata_start, row=0, column=2)
        tkima.Button(buttonframes, text="view", command=self.viewsettings, row=0, column=4)

    def set_viewsettings(self):
        '''
        表示設定の初期設定を入れる
            self.scattersettings:[color, marker, markersize, linestyle, linewidth]
            self.fittingsettings:[color, linestyle, linewidth]
            self.legendsettings:[表示するか否か, loc, bbox_to_anchor, ncol, markerscale]
            self.fontsettings:[size_label, size_legend, size_tick]
        '''
        self.scattersettings.append(['black', 'o', 5, 'None', 2])
        self.fittingsettings.append(['black', 'solid', 2])
        self.legendsettings.append([tkima.BooleanVar(set=True), 'best', '', 1, 1])
        self.fontsettings.append([14, 12, 14])

    def set_iroiro(self):
        '''
        その他初期設定など
        '''
        self.files.append('')
        self.titles.append('')
        self.datas.append('')
        self.dirs.append(PATH)
        self.multidata_flags.append(False)
        self.canvases.append('')
        self.toolbars.append('')
        self.popts.append(0)
        self.pcovs.append(0)
        self.perrs.append(0)
        self.degrees.append(2)
        tkima.BooleanVar(set=False, list=self.graphbooleanvars)
        self.usepage.append([])

    def pageicon_widgets(self):
        '''
        ページを切り替えるボタン
        '''
        n = self.pagenum
        tkima.grid_config(self.pageiconframe, clist=[[2*n, 'minsize', 3], [2*n+1, 'minsize', 5]])
        for i in range(len(self.pageicons)):
            self.pageicons[i].config(bg='white')
        tkima.Label(self.pageiconframe, text=str(n), bg='SkyBlue3', row=0, column=2*n+1, list=self.pageicons)
        self.pageicons[n-1].bind("<ButtonRelease-1>", self.changepage(index=n-1))

    '''------------------------------呼び出される関数など(GUI関係)------------------------------'''

    def getpath(self):
        '''
        self.files:使うdatファイルの絶対パス
        self.dirs:更新されたディレクトリの絶対パス
        self.datas:datファイルより得られたデータ（xが0列目、yが1列目）
        '''
        if self.popup_flags[0] == True or self.popup_flags[0] == True:
            print('\npopup window already exist')
            return
        self.popup_flags[0] = True

        fTyp = [("", "*.dat *.txt")]
        self.files[self.cp-1] = dialog.askopenfilename(initialdir=self.dirs[self.cp-1], filetypes=fTyp)

        self.popup_flags[0] = False
        if self.files[self.cp-1] == '':
            print('\ndialog cancelled')
            return

        self.titles[self.cp-1] = os.path.splitext(os.path.basename(self.files[self.cp-1]))[0]
        self.dirs[self.cp-1] = os.path.dirname(self.files[self.cp-1])
        self.datas[self.cp-1] = np.genfromtxt(self.files[self.cp-1], delimiter='\t')

    def changepage(self, index=None):
        '''
        見たいページのフレームが最前面に
        ページ番号ボタンをクリックしたら起動する
        '''
        def x(event):
            if True in self.popup_flags:
                print("\nplease close popup window")
                return
            self.pageframes[index].tkraise()
            self.cp = index + 1
            for i in range(self.pagenum):
                self.pageicons[i].config(bg='white')
            self.pageicons[self.cp-1].config(bg='SkyBlue3')
        return x

    def _changepage(self, index=None):
        '''
        changepageのeventがないver
        '''
        if True in self.popup_flags:
            print("\nplease close popup window")
            return
        self.pageframes[index].tkraise()
        self.cp = index + 1
        for i in range(self.pagenum):
            self.pageicons[i].config(bg='white')
        self.pageicons[self.cp-1].config(bg='SkyBlue3')

    def add(self, event):
        '''
        ページを増やす関数
        +ボタンを押したら起動する
        '''
        if True in self.popup_flags:
            print("\nplease close popup window")
            return
        self.pagenum += 1
        self.cf.append(5)
        self.cp = self.pagenum
        self.pageicon_widgets()
        self.widgets_main()

    def _add(self):
        '''
        addのeventがないver
        '''
        if True in self.popup_flags:
            print("\nplease close popup window")
            return
        self.pagenum += 1
        self.cf.append(5)
        self.cp = self.pagenum
        self.pageicon_widgets()
        self.widgets_main()

    def viewsettings(self):
        '''
        self.viewbuttonsを押したら実行される関数
        widgetなど毎回作り直すタイプ
        複数のデータをまとめない時はself.viewsetting_singledata()
        複数のデータをまとめる時はself.viewsetting_multidata()
        を行う

        note
            self.viewsettingwindow:専用ウインドウ
            m:ボタンを表示する行数
        '''
        if self.popup_flags[2]:
            print("\npopup window already exist")
            return
        self.popup_flags[2] = True

        self.viewsettingwindow = tkima.Toplevel(title='view settings', func_when_destroy=self.popup_flags_setFalse([2]))
        tkima.grid_config(self.viewsettingwindow, clist=[[0, 'minsize', 30]])
        if self.multidata_flags[self.cp-1] == False:
            self.viewsetting_singledata()
            m = 6
        elif self.multidata_flags[self.cp-1]:
            self.viewsetting_multidata()
            m = 8
        tkima.Button(self.viewsettingwindow, text="OK", command=self.viewsettingwindow_okbutton_pushed, row=m, column=1)

    def viewsetting_singledata(self):
        '''
        self.viewsettingのなかでの分岐
        複数のデータをまとめない時に
        self.scattersettings[page][]とself.fittingsettings[page][]とself.fontsetting[page][]を更新する目的

        note
            self.scattersettingwidgets[]:そのページのデータプロットの設定を入れるwidget
            self.fittingsettingwidgets[]:そのページのfitting結果プロットの設定を入れるwidget
            self.fontsettingwidgets[]:fontsizeなどの設定を入れるwidget

            scatterframe:データプロットの設定を表示するframe
            fittingframe:fitting結果プロットの設定を表示するframe
            fontframe:fontsizeなど
        '''

        '''
        scatter
        '''
        self.scattersettingwidgets = []
        tkima.Label(self.viewsettingwindow, text="scatter", row=0, column=0, columnspan=2, sticky='w')
        scatterframe = tkima.Frame(self.viewsettingwindow, borderwidth=1, relief="solid", row=1, column=1, sticky='w')
        tkima.grid_config(scatterframe, clist=[[1, 'minsize', 10]])
        '''
        scatterのcolor(self.scattersettingwidgets[0])
        '''
        tkima.Label(scatterframe, text='color', row=0, column=0, sticky='w')
        tkima.Label(scatterframe, text=self.scattersettings[self.cp-1][0], bg=COLORdict[self.scattersettings[self.cp-1][0]], row=0, column=2, list=self.scattersettingwidgets)
        self.scattersettingwidgets[0].bind("<ButtonRelease-1>", self.changecolor('scatter'))
        '''
        scatterのmarker(self.scattersettingwidgets[1])
        '''
        tkima.Label(scatterframe, text='marker', row=1, column=0, sticky='w')
        tkima.Combobox(scatterframe, width=5, value=MARKER, init=self.scattersettings[self.cp-1][1], list=self.scattersettingwidgets, row=1, column=2)
        '''
        サイズ(self.scattersettingwidgets[2])
        '''
        tkima.Label(scatterframe, text='size', row=2, column=0, sticky='w')
        tkima.Spinbox(scatterframe, width=5, from_=1, to=100, increment=1, init=str(self.scattersettings[self.cp-1][2]), row=2, column=2, list=self.scattersettingwidgets)
        '''
        点と点をつなぐがどうか(self.scattersettingwidgets[3])
        '''
        tkima.Label(scatterframe, text='line', row=3, column=0, sticky='w')
        tkima.Combobox(scatterframe, width=5, value=LINESTYLE_scatter, init=self.scattersettings[self.cp-1][3], row=3, column=2, list=self.scattersettingwidgets)
        '''
        線幅(self.scattersettingwidgets[4])
        '''
        tkima.Label(scatterframe, text='linewidth', row=4, column=0, sticky='w')
        tkima.Spinbox(scatterframe, width=5, from_=1, to=100, increment=1, init=str(self.scattersettings[self.cp-1][4]), row=4, column=2, list=self.scattersettingwidgets)

        '''
        fitting
        '''
        self.fittingsettingwidgets = []
        tkima.Label(self.viewsettingwindow, text="fitting", row=2, column=0, columnspan=2, sticky='w')
        fittingframe = tkima.Frame(self.viewsettingwindow, borderwidth=1, relief="solid", row=3, column=1, sticky='w')
        tkima.grid_config(fittingframe, clist=[[1, 'minsize', 10]])
        '''
        fittingのcolor(self.fittingsettingwidgets[0])
        '''
        tkima.Label(fittingframe, text='color', row=0, column=0, sticky='w')
        if self.fittingsettings[self.cp-1][0] == self.scattersettings[self.cp-1][0]:
            tkima.Label(fittingframe, text='(same)', bg='white', row=0, column=2, list=self.fittingsettingwidgets)
        else:
            tkima.Label(fittingframe, text=self.fittingsettings[self.cp-1][0], bg=COLORdict[self.fittingsettings[self.cp-1][0]], row=0, column=2, list=self.fittingsettingwidgets)
        self.fittingsettingwidgets[0].bind("<ButtonRelease-1>", self.changecolor('fitting'))
        '''
        fittingのlinestyle(self.fittingsettingwidgets[1])
        '''
        tkima.Label(fittingframe, text='linestyle', row=1, column=0, sticky='w')
        tkima.Combobox(fittingframe, width=5, value=LINESTYLE, init=self.fittingsettings[self.cp-1][1], row=1, column=2, list=self.fittingsettingwidgets)
        '''
        線幅(self.fittingsettingwidgets[2])
        '''
        tkima.Label(fittingframe, text='linewidth', row=2, column=0, sticky='w')
        tkima.Spinbox(fittingframe, width=5, from_=1, to=100, increment=1, init=str(self.fittingsettings[self.cp-1][2]), row=2, column=2, list=self.fittingsettingwidgets)

        '''
        font
        '''
        self.fontsettingwidgets = []
        tkima.Label(self.viewsettingwindow, text="font", row=4, column=0, columnspan=2, sticky='w')
        fontframe = tkima.Frame(self.viewsettingwindow, borderwidth=1, relief="solid", row=5, column=1, sticky='w')
        tkima.grid_config(fontframe, clist=[[1, 'minsize', 10]])
        '''
        fontsize(label文字)(self.fontsettingwidgets[0])
        '''
        tkima.Label(fontframe, text='size(label)', row=0, column=0, sticky='w')
        tkima.Spinbox(fontframe, width=5, from_=1, to=50, increment=1, init=str(self.fontsettings[self.cp-1][0]), row=0, column=2, list=self.fontsettingwidgets)
        '''
        fontsize(メモリ文字)(self.fontsettingwidgets[1])
        '''
        tkima.Label(fontframe, text='size(tick)', row=1, column=0, sticky='w')
        tkima.Spinbox(fontframe, width=5, from_=1, to=100, increment=1, init=str(self.fontsettings[self.cp-1][2]), row=1, column=2, list=self.fontsettingwidgets)

    def viewsetting_multidata(self):
        '''
        self.viewsettingのなかでの分岐
        複数のデータをまとめる時に
        self.legendsettings[page][]とself.fontsetting[page][]を更新する目的

        note
            self.legendsettingwidgets[]:凡例関係の設定を入れるwidget
            self.fontsettingwidgets[]:fontsizeなどの設定を入れるwidget

            legendframe:凡例をどうするかを表示するframe
            fontframe:fontsizeなど
        '''

        self.legendsettingwidgets = []
        '''
        legend(legendframe)
        '''
        tkima.Checkbutton(self.viewsettingwindow, text='legend', variable=self.legendsettings[self.cp-1][0], row=0, column=0, columnspan=2, sticky='w')
        legendframe = tkima.Frame(self.viewsettingwindow, borderwidth=1, relief="solid", row=1, column=1, sticky='w')
        tkima.grid_config(legendframe, clist=[[1, 'minsize', 10]])
        '''
        legendの有無とその名前(self.legendsettingwidgets[0]〜self.legendsettingwidgets[n-1])
        '''
        n = len(self.usepage[self.cp-1])
        for i in range(n):
            tkima.Label(legendframe, text="page "+str(self.usepage[self.cp-1][i]+1), row=i, column=0, sticky='w')
            tkima.Entry(legendframe, width=10, init=self.titles[self.usepage[self.cp-1][i]], row=i, column=2, list=self.legendsettingwidgets)

        '''
        legend(legendlayoutframe)
        '''
        tkima.Label(self.viewsettingwindow, text="legend layout", row=2, column=0, columnspan=2, sticky='w')
        legendlayoutframe = tkima.Frame(self.viewsettingwindow, borderwidth=1, relief="solid", row=3, column=1, sticky='w')
        tkima.grid_config(legendlayoutframe, clist=[[1, 'minsize', 10]])
        '''
        legendの座標にlegendのどの部分を置くか(self.legendsettingwidgets[n])
        '''
        tkima.Label(legendlayoutframe, text="loc", row=0, column=0, sticky='w')
        tkima.Combobox(legendlayoutframe, width=8, value=LOC, init=self.legendsettings[self.cp-1][1], row=0, column=2, columnspan=2, list=self.legendsettingwidgets)
        '''
        legendの座標(self.legendsettingwidgets[n+1], (self.legendsettingwidgets[n+2]))
        '''
        tkima.Label(legendlayoutframe, text="bbox_to_anchor", row=1, column=0, sticky='w')
        for i in [1, 2]:
            tkima.Entry(legendlayoutframe, width=5, row=1, column=i+1, list=self.legendsettingwidgets)
        if self.legendsettings[self.cp-1][2] != '':
            self.legendsettingwidgets[n+1].insert(0, str(self.legendsettings[self.cp-1][2][0]))
            self.legendsettingwidgets[n+2].insert(0, str(self.legendsettings[self.cp-1][2][1]))

        '''
        legend(legendotherframe)
        '''
        tkima.Label(self.viewsettingwindow, text="legend other settings", row=4, column=0, columnspan=2, sticky='w')
        legendotherframe = tkima.Frame(self.viewsettingwindow, borderwidth=1, relief="solid", row=5, column=1, sticky='w')
        tkima.grid_config(legendotherframe, clist=[[1, 'minsize', 10]])
        '''
        legendの行数(self.legendsettingwidgets[n+3])
        '''
        tkima.Label(legendotherframe, text="ncol", row=0, column=0, sticky='w')
        tkima.Entry(legendotherframe, width=5, init=str(self.legendsettings[self.cp-1][3]), row=0, column=2, list=self.legendsettingwidgets)
        '''
        点の大きさ(self.legendsettingwidgets[n+4])
        '''
        tkima.Label(legendotherframe, text="markerscale", row=1, column=0, sticky='w')
        tkima.Spinbox(legendotherframe, width=5, from_=1, to=50, increment=1, init=str(self.legendsettings[self.cp-1][4]), row=1, column=2, list=self.legendsettingwidgets)

        '''
        font
        '''
        self.fontsettingwidgets = []
        tkima.Label(self.viewsettingwindow, text="font", row=6, column=0, columnspan=2, sticky='w')
        fontframe = tkima.Frame(self.viewsettingwindow, borderwidth=1, relief="solid", row=7, column=1, sticky='w')
        tkima.grid_config(fontframe, clist=[[1, 'minsize', 10]])
        '''
        fontsize(label文字)(self.fontsettingwidgets[0])
        '''
        tkima.Label(fontframe, text='size(label)', row=0, column=0, sticky='w')
        tkima.Spinbox(fontframe, width=5, from_=1, to=100, increment=1, init=str(self.fontsettings[self.cp-1][0]), row=0, column=2, list=self.fontsettingwidgets)
        '''
        fontsize(凡例)(self.fontsettingwidgets[1])
        '''
        tkima.Label(fontframe, text='size(legend)', row=1, column=0, sticky='w')
        tkima.Spinbox(fontframe, width=5, from_=1, to=100, increment=1, init=str(self.fontsettings[self.cp-1][1]), row=1, column=2, list=self.fontsettingwidgets)
        '''
        fontsize(凡例)(self.fontsettingwidgets[1])
        '''
        tkima.Label(fontframe, text='size(tick)', row=2, column=0, sticky='w')
        tkima.Spinbox(fontframe, width=5, from_=1, to=100, increment=1, init=str(self.fontsettings[self.cp-1][2]), row=2, column=2, list=self.fontsettingwidgets)

    def viewsettingwindow_okbutton_pushed(self):
        '''
        view設定ウインドウを閉じた時の動作
        Entry系を更新して各設定listに保存する
        '''
        if self.multidata_flags[self.cp-1] == False:
            self.scattersettings[self.cp-1][1] = self.scattersettingwidgets[1].get()
            self.scattersettings[self.cp-1][2] = int(self.scattersettingwidgets[2].get())
            self.scattersettings[self.cp-1][3] = self.scattersettingwidgets[3].get()
            self.scattersettings[self.cp-1][4] = int(self.scattersettingwidgets[4].get())
            if self.fittingsettingwidgets[0]["text"] == '(same)':
                self.fittingsettings[self.cp-1][0] = self.scattersettings[self.cp-1][0]
            self.fittingsettings[self.cp-1][1] = self.fittingsettingwidgets[1].get()
            self.fittingsettings[self.cp-1][2] = int(self.fittingsettingwidgets[2].get())
            self.fontsettings[self.cp-1][0] = int(self.fontsettingwidgets[0].get())
            self.fontsettings[self.cp-1][2] = int(self.fontsettingwidgets[1].get())
        if self.multidata_flags[self.cp-1]:
            n = len(self.usepage[self.cp-1])
            for i in range(n):
                self.titles[self.usepage[self.cp-1][i]] = self.legendsettingwidgets[i].get()
            self.legendsettings[self.cp-1][1] = self.legendsettingwidgets[n].get()
            if self.legendsettingwidgets[n+1].get() == '' or self.legendsettingwidgets[n+2].get() == '' or self.legendsettings[self.cp-1][1] == 'best':
                self.legendsettings[self.cp-1][2] = ''
            else:
                self.legendsettings[self.cp-1][2] = (float(self.legendsettingwidgets[n+1].get()), float(self.legendsettingwidgets[n+2].get()))
            self.legendsettings[self.cp-1][3] = int(self.legendsettingwidgets[n+3].get())
            self.legendsettings[self.cp-1][4] = int(self.legendsettingwidgets[n+4].get())
            self.fontsettings[self.cp-1][0] = int(self.fontsettingwidgets[0].get())
            self.fontsettings[self.cp-1][1] = int(self.fontsettingwidgets[1].get())
            self.fontsettings[self.cp-1][2] = int(self.fontsettingwidgets[2].get())
        self.viewsettingwindow.destroy()

    def changecolor(self, type):
        '''
        self.viewsettings()で使用
        self.scattersettings[page][]とself.fittingsettings[page][]のうち、色の設定を変える
        色サンプルのラベルをクリックした時に呼び出される

        引数
            type:'scatter'か'fitting'のどちらか

        note
            self.colormapwindow:専用のウインドウ
            self.colorlistbox:色の選択肢を表示するやつ
        '''
        def x(event):
            if self.popup_flags[3]:
                print('\npopup window already exist')
                return
            self.popup_flags[3] = True

            self.colormapwindow = tkima.Toplevel(title='select color', func_when_destroy=self.popup_flags_setFalse([3]))
            colorframe = tkima.Frame(self.colormapwindow, row=0, column=0)
            self.colorlistbox = tkima.Listbox(colorframe, height=10, selectmode='single', row=0, column=0)
            for color in COLORS:
                self.colorlistbox.iteminsert(text=color, bg=COLORdict[color])
            tkima.Button(colorframe, text='OK', command=self.changecolor_okbutton_pushed(type), row=1, column=0)
        return x

    def changecolor_okbutton_pushed(self, type):
        '''
        self.changecolor()で使用
        色を決定したボタンをおした時に呼び出される
        self.scattersettings[page][]とself.fittingsettings[page][]を実際に更新する関数
        さらに設定変更ウインドウも更新
        '''
        def x():
            if len(self.colorlistbox.curselection()) == 0:
                return
            index = self.colorlistbox.curselection()[0]
            if type == 'scatter':
                self.scattersettings[self.cp-1][0] = COLORS[index]
                self.scattersettingwidgets[0].config(bg=COLORdict[COLORS[index]], text=COLORS[index])
            if type == 'fitting':
                self.fittingsettings[self.cp-1][0] = COLORS[index]
                self.fittingsettingwidgets[0].config(bg=COLORdict[COLORS[index]], text=COLORS[index])
            tkima.frameclear(self.colormapwindow)
            self.colormapwindow.destroy()
        return x

    def changefunccombo(self, index=None):
        '''
        関数選択Comboboxを変更した時に呼び出される
        数式の表示を更新
        index is page number
        多項式関数なら、次数を指定する奴も表示
        初期値入力欄も更新
        '''
        def x(event):
            self.clearinitparams()
            self.cleardegreeframe()
            k = FUNC_NAMES.index(self.funccomboxes[index].get())
            self.cf[index] = k
            self.func_fomula_strings[index].set(FUNC_FOMULA[k])
            if k == 4:
                tkima.Label(self.degreeframes[index], text="N", row=0, column=0)
                self.degreecombo = tkima.Combobox(self.degreeframes[index], value=('1', '2', '3', '4', '5', '6'), width=3, init=str(self.degrees[index]), row=0, column=1)
                self.degreecombo.bind("<<ComboboxSelected>>", self.changedegreecombo)
            '''if you add a function（何か特別なことあれば）
            elif k == ###関数ナンバー###:
                hogehoge
            '''
            self.initparam_entries()
        return x

    def initparam_entries(self):
        '''
        self.changefunccombo()で使用
        指定した関数に必要な数だけ初期値入力欄を作成
        ある関数で使用した初期値のセットは、同じ関数ならば別のページの初期値として使われる
        '''
        k = self.cp-1
        if len(self.initparamentries[k]) != 0:
            for i in range(len(self.initparamentries[k])):
                self.initparamentries[k][i].destroy()
        tkima.frameclear(self.initparamframes[k])

        dummy = []
        if self.cf[k] == 4:
            num = self.degrees[k] + 1
        else:
            num = len(self.initparams[self.cf[k]])
        dummy = [tkima.Entry(self.initparamframes[k], grid=False, width=5, init=self.initparams[self.cf[k]][i]) for i in range(num)]
        self.initparamentries[k] = dummy

        if self.funccomboxes[k].get() == '(No fitting)':
            return
        for i in range(num):
            self.grid_multirow(index=i, threshold=3, startcolumn=0, startrow=0, children=[tk.Label(self.initparamframes[k], text=WHATPARAM[i]), self.initparamentries[k][i]])

    def changedegreecombo(self, event):
        '''
        self.changefunccombo()で使用
        多項式関数の次数を変更した時に呼び出される
        次数を控えて、初期値入力欄の数を更新する
        '''
        self.degrees[self.cp-1] = int(self.degreecombo.get())
        self.initparam_entries()

    def clearinitparams(self):
        '''
        self.changefunccombo()で使用
        初期値入力欄の更新のために一旦消す
        '''
        tkima.frameclear(self.initparamframes[self.cp-1])
        self.initparamentries[self.cp-1] = []

    def cleardegreeframe(self):
        '''
        self.changefunccombo()で使用
        多項式関数の次数入力欄を一旦消す
        '''
        tkima.frameforget(self.degreeframes[self.cp-1])

    '''--------------------fittingやmatplotlibに関する関数--------------------'''

    def fitting(self, flag=False):
        '''
        メインとなる部分
        OPENボタンを押したら開始する

        引数
            flag:reloadするかしないか
        '''
        k = self.cp-1
        self.funccomboxes[k].config(state='readonly')

        if flag == False:
            self.getpath()
            if self.files[k] == '':
                return
            if len(self.datas[k][0]) > 2:
                self.fitting_multicolumns()
                return
            self.multidata_flags[k] = False
            self.usepage[k] = []
            self.titlestrs[k].set(self.files[k])
            self.delete_blank_row()
            self.ranges[k] = self.deciderange()

        #GUIからレンジなどを取得
        self.get_range()
        #初期値
        self.get_initparams()
        #描画したいページにグラフがすでにあれば消す
        self.delete_graph_if_exists()

        #フィッティング
        self.popts[k], self.pcovs[k], self.perrs[k] = self.execute_fitting()
        #誤差計算
        self.sqrt_of_MSE = cal.calcurate_sqrt_of_MSE(self.cf[k], self.datas[k], self.degrees[k], self.popts[k])

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        graph.set_axissettings(ax, self.fontsettings[k], self.xlabel, self.ylabel, self.xunit, self.yunit, self.xstart, self.ystart, self.xend, self.yend)
        #データを描画
        graph.plot_scatterdata(ax, self.datas[k], self.scattersettings[k], self.titles[k])
        #フィッティング結果を描画
        ydata = self.cal_ydata(k)
        if self.cf[k] != 5:
            graph.plot_fittingresult(ax, np.linspace(self.xstart, self.xend, 100), ydata, self.fittingsettings[k])
        #表示
        self.print_results()
        #グラフをGUIに表示
        self.set_canvases(fig)
        #結果表示
        self.show_fittingresults_onGUI()

    def multidata_start(self):
        '''
        複数のグラフを合わせて表示するボタンを押したら呼び出される
        ここではどのページのグラフを合わせるかを選択する
        この関数を用いて表示されたグラフは選択対象に入らない

        note
            self.whichpagewindow:専用ウインドウ
            self.graphchkbuttons[]:どのグラフを合わせるかを選択するCheckbutton
        '''
        if True in self.popup_flags:
            print("please close popup window")
            return

        pages = []
        for i in range(self.pagenum):
            if self.multidata_flags[i] == False and i != (self.cp-1) and self.graph_flags[i] == True:
                pages.append(i)
        if pages == []:
            print('there is no graph')
            return

        self.popup_flags[1] = True
        self.whichpagewindow = tkima.Toplevel(title='which graphs ?', func_when_destroy=self.popup_flags_setFalse([1]))
        self.graphchkbuttons = []
        r = 0
        for i in pages:
            txt = "page " + str(i+1) +" ( " + self.titles[i] + " )"
            tkima.Checkbutton(self.whichpagewindow, text=txt, variable=self.graphbooleanvars[i], list=self.graphchkbuttons, row=r, column=0)
            r += 1
        tkima.Button(self.whichpagewindow, text='OK', command=self.multidata(pages), row=self.pagenum)

    def multidata(self, pages):
        '''
        note
            self.usepage[]:どのページを用いるかのインデックスが入る(0から始まるので注意)
        '''
        def x():
            self.multidata_flags[self.cp-1] = True

            u = []
            for i in pages:
                if self.graphbooleanvars[i].get() == True:
                    u.append(i)
            self.usepage[self.cp-1] = u
            self.whichpagewindow.destroy()
            if u == []:
                print("no page is selected")
                return

            self.multidata_main(flag=False)
        return x

    def multidata_main(self, flag):
        '''
        self.multidata()で使用
        選んだページのデータ・表示設定などを反映して合わせて表示する
        x,yの範囲はその中での最大範囲を取らせる(あとで変更可)
        flagは、reloadの時True

        note
            self.usepage[]:どのページを用いるかのインデックスが入る(0から始まるので注意)
        '''
        k = self.cp-1
        self.funccomboxes[k].current(5)
        self.funccomboxes[k].config(state='disabled')
        tkima.frameclear(self.degreeframes[k])
        #GUIからレンジなどを取得
        if flag == False:
            xstarts = []
            xends = []
            ystarts = []
            yends = []
            for i in self.usepage[k]:
                xstarts.append(float(self.rangeentries[i][0].get()))
                xends.append(float(self.rangeentries[i][1].get()))
                ystarts.append(float(self.rangeentries[i][2].get()))
                yends.append(float(self.rangeentries[i][3].get()))
            self.xstart = min(xstarts)
            self.xend = max(xends)
            self.ystart = min(ystarts)
            self.yend = max(yends)
            self.rangeentries[k][0].overwrite(str(self.xstart))
            self.rangeentries[k][1].overwrite(str(self.xend))
            self.rangeentries[k][2].overwrite(str(self.ystart))
            self.rangeentries[k][3].overwrite(str(self.yend))
            self.xunit = self.xunitentries[self.usepage[k][0]].get()
            self.yunit = self.yunitentries[self.usepage[k][0]].get()
            self.xlabel = self.xlabelentries[self.usepage[k][0]].get()
            self.ylabel = self.ylabelentries[self.usepage[k][0]].get()
        elif flag:
            self.get_range()

        #描画したいページにグラフがすでにあれば消す
        self.delete_graph_if_exists()

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        graph.set_axissettings(ax, self.fontsettings[k], self.xlabel, self.ylabel, self.xunit, self.yunit, self.xstart, self.ystart, self.xend, self.yend)

        for i in self.usepage[k]:
            #データを描画
            graph.plot_scatterdata(ax, self.datas[i], self.scattersettings[i], self.titles[i])
            #フィッティング結果を描画
            ydata = self.cal_ydata(i)
            if self.cf[i] != 5:
                graph.plot_fittingresult(ax, np.linspace(self.xstart, self.xend, 100), ydata, self.fittingsettings[i])

        #凡例の描画
        graph.plot_legend(ax, self.legendsettings[k], self.fontsettings[k])
        #グラフをGUIに表示
        self.set_canvases(fig)
        #表示
        self.print_results()

    def fitting_multicolumns(self):
        '''
        複数列あるデータの時
        分解して現在のページ、その次のページ...に個別に出す
        '''
        original_page = self.cp-1
        original_data = self.datas[original_page]
        original_file = self.files[original_page]
        original_title = self.titles[original_page]
        num = len(self.datas[original_page][0]) - 1
        u = []
        for i in range(num):
            if i != 0:
                self._add()
            k = self.cp-1
            u.append(k)
            self.files[k] = original_file + ' (' + str(i+1) + ')'
            self.titles[k] = original_title + '(' + str(i+1) + ')'
            self.dirs[k] = self.dirs[original_page]

            dummy = original_data
            for j in reversed(range(num+1)):
                if j != (i+1) and j != 0:
                    dummy = np.delete(dummy, j, axis=1)
            self.datas[k] = dummy
            self.delete_blank_row()
            self.multidata_flags[k] = False
            self.titlestrs[k].set(self.files[k])
            self.ranges[k] = self.deciderange()

            #GUIからレンジなどを取得
            self.get_range()
            #初期値
            self.get_initparams()
            #描画したいページにグラフがすでにあれば消す
            self.delete_graph_if_exists()

            #フィッティング
            self.popts[k], self.pcovs[k], self.perrs[k] = self.execute_fitting()
            #誤差計算
            self.sqrt_of_MSE = cal.calcurate_sqrt_of_MSE(self.cf[k], self.datas[k], self.degrees[k], self.popts[k])

            fig = plt.Figure()
            ax = fig.add_subplot(111)
            graph.set_axissettings(ax, self.fontsettings[k], self.xlabel, self.ylabel, self.xunit, self.yunit, self.xstart, self.ystart, self.xend, self.yend)
            #データを描画
            graph.plot_scatterdata(ax, self.datas[k], self.scattersettings[k], self.titles[k])
            #フィッティング結果を描画
            ydata = self.cal_ydata(k)
            if self.cf[k] != 5:
                graph.plot_fittingresult(ax, np.linspace(self.xstart, self.xend, 100), ydata, self.fittingsettings[k])
            #表示
            self.print_results()
            #グラフをGUIに表示
            self.set_canvases(fig)
            #結果表示
            self.show_fittingresults_onGUI()

        self._add()
        self.multidata_flags[self.cp-1] = True
        self.usepage[self.cp-1] = u
        self.files[self.cp-1] = original_file
        self.titles[self.cp-1] = original_title
        self.dirs[self.cp-1] = self.dirs[original_page]
        self.titlestrs[self.cp-1].set(original_file)

        self.multidata_main(flag=False)

    def reload(self):
        '''
        RELOADボタンを押したら実行される関数
        flag=Trueでfittingなどを実行するだけ
        '''
        if self.graph_flags[self.cp-1] == False:
            print("can't reload because NO DATA")
            return
        if self.multidata_flags[self.cp-1] == False:
            self.fitting(flag=True)
        elif self.multidata_flags[self.cp-1]:
            self.multidata_main(flag=True)

    def execute_fitting(self):
        k = self.cp-1
        fnc = self.cf[k]
        if fnc == 5:
            popt, pcov, perr = None, None, None
        elif fnc == 4:
            self.degrees[self.cp-1] = int(self.degreecombo.get())
            popt, pcov, perr = cal.CurveFitting(cal.Ndegree(self.degrees[k]), self.initparams[fnc][:(self.degrees[k]+1)], self.datas[k])
        else:
            popt, pcov, perr = cal.CurveFitting(FUNC[fnc], self.initparams[fnc], self.datas[k])

        '''if you add a function（elseでカバーできない時(引数の数が変わる時)）
        elif fnc == ###関数ナンバー###:
            popt, pcov, perr = cal.CurveFitting(cal.###関数###, self.initparams[fnc], self.datas[k])
        '''

        return popt, pcov, perr

    def set_canvases(self, fig):
        k = self.cp-1
        #グラフをGUIに表示
        canvas = FigureCanvasTkAgg(fig, master=self.graphframes[k])
        self.canvases[k] = canvas
        self.canvases[k].draw()
        self.canvases[k].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #ツールも表示
        toolbar = NavigationToolbar2Tk(canvas, self.graphframes[k])
        self.toolbars[k] = toolbar
        self.toolbars[k].update()
        self.canvases[k].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def get_initparams(self):
        '''
        fittingの初期値を取得
        '''
        for i in range(len(self.initparamentries[self.cp-1])):
            self.initparams[self.cf[self.cp-1]][i] = float(self.initparamentries[self.cp-1][i].get())

    def get_range(self):
        '''
        グラフのレンジを取得
        '''
        k = self.cp-1
        self.xstart = float(self.rangeentries[k][0].get())
        self.xend = float(self.rangeentries[k][1].get())
        self.ystart = float(self.rangeentries[k][2].get())
        self.yend = float(self.rangeentries[k][3].get())
        self.xunit = self.xunitentries[k].get()
        self.yunit = self.yunitentries[k].get()
        self.xlabel = self.xlabelentries[k].get()
        self.ylabel = self.ylabelentries[k].get()

    def delete_graph_if_exists(self):
        '''
        描画したいページにグラフがすでにあれば消す
        '''
        if self.graph_flags[self.cp-1]:
            tkima.frameclear(self.graphframes[self.cp-1])
            tkima.frameclear(self.resultframes[self.cp-1])
        else:
            self.graph_flags[self.cp-1] = True

    def show_fittingresults_onGUI(self):
        '''
        fitting結果をGUI上のEntryに示す
        '''
        k = self.cp-1
        if self.funccomboxes[k].get() == '(No fitting)':
            return

        tkima.grid_config(self.pageframes[k], rlist=[[13, 'minsize', 10]])
        self.resultframes[k].grid(row=14, column=0)

        tkima.Label(self.resultframes[k], text="sqrt of MSE", bg='DarkSeaGreen1', row=0, column=0)
        tkima.Entry(self.resultframes[k], width=8, init=str(self.sqrt_of_MSE), row=0, column=1)
        tkima.grid_config(self.resultframes[k], clist=[[2, 'minsize', 20]])

        n = len(self.initparamentries[k])
        tkima.Label(self.resultframes[k], text="opt params", bg='DarkSeaGreen1', row=0, column=3)
        for i in range(n):
            label = tk.Label(self.resultframes[k], text=WHATPARAM[i])
            entry_p = tkima.Entry(self.resultframes[k], grid=False, width=8, init=str(self.popts[k][i]))
            self.grid_multirow(index=i, threshold=4, startcolumn=4, startrow=0, children=[label, entry_p])

    def print_results(self):
        k = self.cp-1
        if self.multidata_flags[k] == False:
            print('\n-- page '+str(k+1)+'\n    '+self.files[k])
            if self.funccomboxes[k].get() != '(No fitting)':
                print('    ----fit results--------')
                print('    func = '+FUNC_NAMES[self.cf[k]]+'\n\t( '+FUNC_FOMULA[self.cf[k]]+' )')
                for i in range(len(self.initparamentries[k])):
                    print('    '+WHATPARAM[i]+str(self.popts[k][i])+' (error:'+str(self.perrs[k][i])+')')
                print('    sqrt of mean squared error = '+str(self.sqrt_of_MSE))

            if self.funccomboxes[k].get() == 'Gaussian':
                print('    a^2:'+str(self.popts[k][0]**2))
                print('    (a^2=variance, b=average)')
            '''if you add a function（関数によって何かprintしたいものがあれば）
            if self.funccomboxes[k].get() == '###関数名###':
                print('    hogehoge')
            '''
            if self.funccomboxes[k].get() != '(No fitting)':
                print('    -----------------------')
        elif self.multidata_flags[k]:
            print('\n-- page '+str(k+1)+' = SUMMARISE')
            print('    consists of')
            for i in self.usepage[k]:
                print('    page'+str(i+1)+'('+self.titles[i]+')')

    def deciderange(self):
        '''
        得たデータからx,yの最小値を取得する関数
        '''
        k = self.cp-1
        self.ranges[k] = [min(self.datas[k][:, 0]), max(self.datas[k][:, 0]), min(self.datas[k][:, 1]), max(self.datas[k][:, 1])]
        for i in range(4):
            self.rangeentries[k][i].overwrite(self.ranges[k][i])

    def grid_multirow(self, index, threshold, startcolumn, startrow, children):
        '''
        threshold個ごとに改行してgridしてくれる関数
        for文で繰り返してる中で使う

        引数:
            index:for文のindex
            threshold:同じ列に何セット置くか
            startcolumn:何列目から始めるか
            startrow:何行目から始めるか
            children:実際に置くもの(複数のwidgetをlist化して入れると、それらで1セットに)
        '''
        row, column = divmod(int(index), int(threshold))
        n = len(children)
        for i in range(n):
            children[i].grid(row=int(row+startrow), column=int(n*column+startcolumn+i))

    def popup_flags_setFalse(self, list):
        '''
        ポップアップウィンドウが亡くなった時にself.popup_flagsの該当箇所をFalseにする
        '''
        def x(event):
            for i in list:
                self.popup_flags[i] = False
        return x

    def delete_blank_row(self):
        '''
        空白行を消す
        '''
        for i in reversed(range(len(self.datas[self.cp-1]))):
            if np.isnan(self.datas[self.cp-1][i][1]):
                self.datas[self.cp-1] = np.delete(self.datas[self.cp-1], i, axis=0)

    def cal_ydata(self, i):
        if self.cf[i] == 5:
            return []
        elif self.cf[i] == 4:
            return cal.Ndegree(self.degrees[i])(np.linspace(self.xstart, self.xend, 100), *self.popts[i])
        else:
            return FUNC[self.cf[i]](np.linspace(self.xstart, self.xend, 100) ,*self.popts[i])
        '''if you add a function（elseでカバーできない時(引数の数が変わる時)）
        elif self.cf[i] == ###関数ナンバー###:
            return cal.###関数###(np.linspace(self.xstart, self.xend, 100) ,*self.popts[i])
        '''

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
