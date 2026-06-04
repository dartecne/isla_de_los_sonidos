
import sys
import os
import GUI
import wx
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

import controler

def setup_logging():
    log_folder = '../logs'
    os.makedirs(log_folder, exist_ok=True)
    filename = datetime.now().strftime("lisa_events_%Y%m%d_%H%M%S.log")
    log_file = os.path.join(log_folder, filename)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(threadName)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

if __name__ == '__main__':
    args = sys.argv[1:]
    setup_logging()
    logging.info("fichero logging creado")
    if len(args) == 1 and args[0] == '-gui':
        app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
        frame = GUI.MyFrame( None )
        frame.Show(True)     # Show the frame.
        frame.m_textCtrl_inputs.AppendText( 'INIT' );
        app.MainLoop()
    try:
        controler = controler.Controler(1, "control_thread", 0)
        controler.start()

    except KeyboardInterrupt:
        print("\n\nCerrando...")
        controler.close()

        print("Adios!")