# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import controler

###############################################111############################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"SONORON: Isla de los Sonidos", pos = wx.DefaultPosition, size = wx.Size( 805,567 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		panelSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		self.panel.SetBackgroundColour( wx.Colour( 171, 233, 233 ) )
		
		elementosSizer = wx.BoxSizer( wx.VERTICAL )
		
		cuadroSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText_seres = wx.StaticText( self.panel, wx.ID_ANY, u"Seres de la Isla", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_seres.Wrap( -1 )
		self.m_staticText_seres.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer16.Add( self.m_staticText_seres, 0, wx.ALL, 5 )
		
		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_radioBtn_ser1 = wx.RadioButton( self.panel, wx.ID_ANY, u"ser 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_radioBtn_ser1, 0, wx.ALL, 5 )
		
		self.m_radioBtn_ser2 = wx.RadioButton( self.panel, wx.ID_ANY, u"ser 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_radioBtn_ser2, 0, wx.ALL, 5 )
		
		self.m_radioBtn_ser3 = wx.RadioButton( self.panel, wx.ID_ANY, u"ser 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_radioBtn_ser3, 0, wx.ALL, 5 )
		
		self.m_radioBtn_ser4 = wx.RadioButton( self.panel, wx.ID_ANY, u"ser 4", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_radioBtn_ser4, 0, wx.ALL, 5 )
		
		self.m_radioBtn_ser5 = wx.RadioButton( self.panel, wx.ID_ANY, u"ser 5", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_radioBtn_ser5, 0, wx.ALL, 5 )
		
		self.m_radioBtn_ser6 = wx.RadioButton( self.panel, wx.ID_ANY, u"ser 6", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_radioBtn_ser6, 0, wx.ALL, 5 )
		
		
		bSizer16.Add( gSizer5, 1, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		bSizer172 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox_arpegiator = wx.CheckBox( self.panel, wx.ID_ANY, u"arpegiator", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer172.Add( self.m_checkBox_arpegiator, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_checkBox_seres_rec = wx.CheckBox( self.panel, wx.ID_ANY, u"REC", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer172.Add( self.m_checkBox_seres_rec, 1, wx.ALIGN_CENTER|wx.ALIGN_RIGHT|wx.ALL, 0 )
		
		
		bSizer16.Add( bSizer172, 0, wx.ALL|wx.EXPAND, 5 )
		
		seresSizer = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText51 = wx.StaticText( self.panel, wx.ID_ANY, u"Slide Ribbon", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		seresSizer.Add( self.m_staticText51, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_textCtrl_slide_1 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		seresSizer.Add( self.m_textCtrl_slide_1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText52 = wx.StaticText( self.panel, wx.ID_ANY, u"Slide Ribbon", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )
		seresSizer.Add( self.m_staticText52, 0, wx.ALIGN_CENTER|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_textCtrl_slide_2 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		seresSizer.Add( self.m_textCtrl_slide_2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer16.Add( seresSizer, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		cuadroSizer.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		self.m_staticline8 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		cuadroSizer.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )
		
		ambienteSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText491 = wx.StaticText( self.panel, wx.ID_ANY, u"Ambiente de la Isla", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText491.Wrap( -1 )
		self.m_staticText491.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		ambienteSizer.Add( self.m_staticText491, 0, wx.ALL, 5 )
		
		gSizer6 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_radioBtn_ambiente_1 = wx.RadioButton( self.panel, wx.ID_ANY, u"ambiente 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_radioBtn_ambiente_1, 1, wx.ALL, 5 )
		
		self.m_radioBtn_ambiente_2 = wx.RadioButton( self.panel, wx.ID_ANY, u"ambiente 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_radioBtn_ambiente_2, 0, wx.ALL, 5 )
		
		self.m_radioBtn_ambiente_3 = wx.RadioButton( self.panel, wx.ID_ANY, u"ambiente 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_radioBtn_ambiente_3, 0, wx.ALL, 5 )
		
		self.m_radioBtn_ambiente_4 = wx.RadioButton( self.panel, wx.ID_ANY, u"ambiente 4", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_radioBtn_ambiente_4, 0, wx.ALL, 5 )
		
		
		ambienteSizer.Add( gSizer6, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText531 = wx.StaticText( self.panel, wx.ID_ANY, u"One Shot", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText531.Wrap( -1 )
		ambienteSizer.Add( self.m_staticText531, 0, wx.ALL, 5 )
		
		bSizer171 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox_one_shot_1 = wx.CheckBox( self.panel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_checkBox_one_shot_1, 0, wx.ALL, 5 )
		
		self.m_checkBox_one_shot_2 = wx.CheckBox( self.panel, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_checkBox_one_shot_2, 0, wx.ALL, 5 )
		
		self.m_checkBox_one_shot_3 = wx.CheckBox( self.panel, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_checkBox_one_shot_3, 0, wx.ALL, 5 )
		
		self.m_checkBox_one_shot_4 = wx.CheckBox( self.panel, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_checkBox_one_shot_4, 0, wx.ALL, 5 )
		
		self.m_checkBox_one_shot_5 = wx.CheckBox( self.panel, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_checkBox_one_shot_5, 0, wx.ALL, 5 )
		
		self.m_checkBox_one_shot_6 = wx.CheckBox( self.panel, wx.ID_ANY, u"6", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_checkBox_one_shot_6, 0, wx.ALL, 5 )
		
		
		ambienteSizer.Add( bSizer171, 1, wx.ALL|wx.EXPAND, 5 )
		
		gSizer111 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText541 = wx.StaticText( self.panel, wx.ID_ANY, u"Joystick X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText541.Wrap( -1 )
		gSizer111.Add( self.m_staticText541, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_textCtrl_joy_x = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer111.Add( self.m_textCtrl_joy_x, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText551 = wx.StaticText( self.panel, wx.ID_ANY, u"Joystick Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText551.Wrap( -1 )
		gSizer111.Add( self.m_staticText551, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_textCtrl_joy_y = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer111.Add( self.m_textCtrl_joy_y, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		ambienteSizer.Add( gSizer111, 1, wx.EXPAND, 5 )
		
		
		cuadroSizer.Add( ambienteSizer, 1, wx.EXPAND, 5 )
		
		self.m_staticline9 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		cuadroSizer.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )
		
		cuevaSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText49 = wx.StaticText( self.panel, wx.ID_ANY, u"Cueva de los Ruidos", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )
		self.m_staticText49.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		cuevaSizer.Add( self.m_staticText49, 0, wx.ALL, 5 )
		
		gSizer61 = wx.GridSizer( 0, 3, 0, 0 )
		
		self.m_radioBtn_cueva_1 = wx.RadioButton( self.panel, wx.ID_ANY, u"banco 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer61.Add( self.m_radioBtn_cueva_1, 1, wx.ALL, 5 )
		
		self.m_radioBtn_cueva_2 = wx.RadioButton( self.panel, wx.ID_ANY, u"banco 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer61.Add( self.m_radioBtn_cueva_2, 0, wx.ALL, 5 )
		
		self.m_radioBtn_cueva_3 = wx.RadioButton( self.panel, wx.ID_ANY, u"banco 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer61.Add( self.m_radioBtn_cueva_3, 0, wx.ALL, 5 )
		
		
		cuevaSizer.Add( gSizer61, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText53 = wx.StaticText( self.panel, wx.ID_ANY, u"Secuenciador", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText53.Wrap( -1 )
		cuevaSizer.Add( self.m_staticText53, 0, wx.ALL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox_seq_1 = wx.CheckBox( self.panel, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_checkBox_seq_1, 0, wx.ALL, 5 )
		
		self.m_checkBox_seq_2 = wx.CheckBox( self.panel, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_checkBox_seq_2, 0, wx.ALL, 5 )
		
		self.m_checkBox_seq_3 = wx.CheckBox( self.panel, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_checkBox_seq_3, 0, wx.ALL, 5 )
		
		self.m_checkBox_seq_4 = wx.CheckBox( self.panel, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_checkBox_seq_4, 0, wx.ALL, 5 )
		
		self.m_checkBox_seq_5 = wx.CheckBox( self.panel, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_checkBox_seq_5, 0, wx.ALL, 5 )
		
		self.m_checkBox_seq_6 = wx.CheckBox( self.panel, wx.ID_ANY, u"6", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_checkBox_seq_6, 0, wx.ALL, 5 )
		
		
		cuevaSizer.Add( bSizer17, 1, wx.ALL|wx.EXPAND, 5 )
		
		gSizer11 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText54 = wx.StaticText( self.panel, wx.ID_ANY, u"Potenciometro 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )
		gSizer11.Add( self.m_staticText54, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_textCtrl_pot_1 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer11.Add( self.m_textCtrl_pot_1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText55 = wx.StaticText( self.panel, wx.ID_ANY, u"Potenciometro 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText55.Wrap( -1 )
		gSizer11.Add( self.m_staticText55, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_textCtrl_pot_2 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer11.Add( self.m_textCtrl_pot_2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		cuevaSizer.Add( gSizer11, 1, wx.EXPAND, 5 )
		
		
		cuadroSizer.Add( cuevaSizer, 1, wx.EXPAND, 5 )
		
		
		elementosSizer.Add( cuadroSizer, 3, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticline6 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		elementosSizer.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
		
		externosSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		puenteSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.Puente = wx.StaticText( self.panel, wx.ID_ANY, u"Puente", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Puente.Wrap( -1 )
		self.Puente.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		puenteSizer.Add( self.Puente, 0, wx.ALL, 5 )
		
		gSizer14 = wx.GridSizer( 0, 3, 0, 0 )
		
		self.m_textCtrl_puente_1 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer14.Add( self.m_textCtrl_puente_1, 0, wx.ALL, 5 )
		
		self.m_textCtrl_puente_2 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer14.Add( self.m_textCtrl_puente_2, 0, wx.ALL, 5 )
		
		self.m_textCtrl_puente_3 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer14.Add( self.m_textCtrl_puente_3, 0, wx.ALL, 5 )
		
		self.m_textCtrl_puente_4 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer14.Add( self.m_textCtrl_puente_4, 0, wx.ALL, 5 )
		
		self.m_textCtrl_puente_5 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer14.Add( self.m_textCtrl_puente_5, 0, wx.ALL, 5 )
		
		self.m_textCtrl_puente_6 = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer14.Add( self.m_textCtrl_puente_6, 0, wx.ALL, 5 )
		
		
		puenteSizer.Add( gSizer14, 1, wx.EXPAND, 5 )
		
		
		externosSizer.Add( puenteSizer, 1, wx.EXPAND, 5 )
		
		self.m_staticline10 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		externosSizer.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )
		
		lorolocoSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText66 = wx.StaticText( self.panel, wx.ID_ANY, u"LoroLoco", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText66.Wrap( -1 )
		self.m_staticText66.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		lorolocoSizer.Add( self.m_staticText66, 0, wx.ALL, 5 )
		
		self.m_checkBox_loro_rec = wx.CheckBox( self.panel, wx.ID_ANY, u"REC", wx.DefaultPosition, wx.DefaultSize, 0 )
		lorolocoSizer.Add( self.m_checkBox_loro_rec, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		externosSizer.Add( lorolocoSizer, 2, wx.EXPAND, 5 )
		
		self.m_staticline11 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		externosSizer.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )
		
		tunelSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.Tunel = wx.StaticText( self.panel, wx.ID_ANY, u"Tunel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Tunel.Wrap( -1 )
		self.Tunel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		tunelSizer.Add( self.Tunel, 0, wx.ALL, 5 )
		
		self.m_textCtrl_tunel_sonar = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		tunelSizer.Add( self.m_textCtrl_tunel_sonar, 0, wx.ALL, 5 )
		
		
		externosSizer.Add( tunelSizer, 1, wx.EXPAND, 5 )
		
		self.m_staticline81 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		externosSizer.Add( self.m_staticline81, 0, wx.EXPAND |wx.ALL, 5 )
		
		timonSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.Timon = wx.StaticText( self.panel, wx.ID_ANY, u"Timon", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Timon.Wrap( -1 )
		self.Timon.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		timonSizer.Add( self.Timon, 0, wx.ALL, 5 )
		
		self.m_textCtrl_timon = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		timonSizer.Add( self.m_textCtrl_timon, 0, wx.ALL, 5 )
		
		
		externosSizer.Add( timonSizer, 1, wx.EXPAND, 5 )
		
		
		elementosSizer.Add( externosSizer, 1, wx.EXPAND, 5 )
		
		self.m_staticline7 = wx.StaticLine( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		elementosSizer.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )
		
		logSizer = wx.BoxSizer( wx.VERTICAL )
		
		headerSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText47 = wx.StaticText( self.panel, wx.ID_ANY, u"Entradas", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		self.m_staticText47.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		headerSizer.Add( self.m_staticText47, 1, wx.ALL, 5 )
		
		self.m_staticText46 = wx.StaticText( self.panel, wx.ID_ANY, u"Salidas", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )
		self.m_staticText46.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		headerSizer.Add( self.m_staticText46, 1, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		logSizer.Add( headerSizer, 0, wx.EXPAND, 0 )
		
		comSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		m_comboBox_puerto_serieChoices = []
		self.m_comboBox_puerto_serie = wx.ComboBox( self.panel, wx.ID_ANY, u"Puertos Serie", wx.DefaultPosition, wx.DefaultSize, m_comboBox_puerto_serieChoices, 0 )
		comSizer.Add( self.m_comboBox_puerto_serie, 3, wx.ALL, 5 )
		
		self.m_button_puerto_serie = wx.Button( self.panel, wx.ID_ANY, u"Conectar", wx.DefaultPosition, wx.DefaultSize, 0 )
		comSizer.Add( self.m_button_puerto_serie, 0, wx.ALL, 5 )
		
		m_comboBox_puerto_midiChoices = []
		self.m_comboBox_puerto_midi = wx.ComboBox( self.panel, wx.ID_ANY, u"Puertos MIDI", wx.DefaultPosition, wx.DefaultSize, m_comboBox_puerto_midiChoices, 0 )
		comSizer.Add( self.m_comboBox_puerto_midi, 3, wx.ALL, 5 )
		
		self.m_button_puerto_midi = wx.Button( self.panel, wx.ID_ANY, u"Conectar", wx.DefaultPosition, wx.DefaultSize, 0 )
		comSizer.Add( self.m_button_puerto_midi, 0, wx.ALL, 5 )
		
		
		logSizer.Add( comSizer, 1, wx.EXPAND, 5 )
		
		logTextSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl_inputs = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		logTextSizer.Add( self.m_textCtrl_inputs, 3, wx.ALL|wx.EXPAND, 0 )
		
		self.m_textCtrl_outputs = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		logTextSizer.Add( self.m_textCtrl_outputs, 3, wx.EXPAND, 5 )
		
		
		logSizer.Add( logTextSizer, 3, wx.EXPAND, 5 )
		
		
		elementosSizer.Add( logSizer, 1, wx.EXPAND, 5 )
		
		
		self.panel.SetSizer( elementosSizer )
		self.panel.Layout()
		elementosSizer.Fit( self.panel )
		panelSizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.SetSizer( panelSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button_puerto_serie.Bind( wx.EVT_BUTTON, self.OnConnect )
		self.m_button_puerto_midi.Bind( wx.EVT_BUTTON, self.OnMIDIConnect )
	
		self.controler = controler.Controler(1, "control_thread", self)
		self.m_textCtrl_inputs.AppendText( 'Conectando.../n' )
		self.controler.start()

	def __del__( self ):
		pass
	
	def OnConnect( self, event ):
		self.m_textCtrl_inputs.AppendText( 'Conectando.../n' )
		self.controler.start()

	def OnMIDIConnect( self, event ):
		self.m_textCtrl_outputs.AppendText( 'Conectado a puerto MIDI' )


