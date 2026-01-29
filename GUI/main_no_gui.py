
#import GUI
#import wx
import logging
import controler_no_gui


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
    controler = controler_no_gui.Controler(1, "control_thread")
    controler.start()

#   app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
 #   frame = GUI.MyFrame( None )
 #   frame.Show(True)     # Show the frame.
 #   frame.m_textCtrl_inputs.AppendText( 'INIT' );
 #   app.MainLoop()

