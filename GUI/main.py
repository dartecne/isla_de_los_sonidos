
import GUI
import wx
import logging



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = GUI.MyFrame( None )
    frame.Show(True)     # Show the frame.
    frame.m_textCtrl_inputs.AppendText( 'INIT' );
    app.MainLoop()

