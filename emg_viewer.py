import sys, csv, time
from collections import deque
from datetime import datetime
import numpy as np
import serial
from serial.tools import list_ports
from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg

class Viewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Grove EMG | ESP32 即時量測')
        self.resize(1150, 850)
        self.ser = None
        self.t = deque(maxlen=30000)
        self.v = deque(maxlen=30000)
        self.base = None
        self.env = 0.0
        self.envelopes = deque(maxlen=30000)
        self.file = None
        self.writer = None
        self.first_us = None
        self.last_us = None
        self.elapsed_us = 0
        self.pending = bytearray()
        self.bad_lines = 0
        self.total = 0
        self.window = QtWidgets.QComboBox(); self.window.addItems(['5','10','30','60']); self.window.setCurrentText('10')
        self.ports = QtWidgets.QComboBox()
        self.refresh = QtWidgets.QPushButton('重新掃描'); self.refresh.clicked.connect(self.scan)
        self.connect_btn = QtWidgets.QPushButton('連線'); self.connect_btn.clicked.connect(self.toggle)
        self.record_btn = QtWidgets.QPushButton('開始記錄 CSV'); self.record_btn.clicked.connect(self.toggle_record)
        self.record_btn.setEnabled(False)
        self.zero_btn = QtWidgets.QPushButton('重設基準'); self.zero_btn.clicked.connect(self.reset_base)
        self.status = QtWidgets.QLabel('尚未連線')
        bar = QtWidgets.QHBoxLayout()
        for w in [QtWidgets.QLabel('COM:'),self.ports,self.refresh,self.connect_btn,QtWidgets.QLabel('視窗(秒):'),self.window,self.zero_btn,self.record_btn]: bar.addWidget(w)
        bar.addStretch()
        layout = QtWidgets.QVBoxLayout(self); layout.addLayout(bar); layout.addWidget(self.status)
        pg.setConfigOptions(antialias=False)
        self.plots = []
        for title, ylabel in [('原始輸出','V'),('扣除基準','mV'),('整流 + 平滑 (活動指標)','mV')]:
            p=pg.PlotWidget(title=title)
            p.setLabel('left',ylabel);p.setLabel('bottom','時間','s');p.showGrid(x=True,y=True,alpha=0.25)
            layout.addWidget(p)
            self.plots.append(p)
        self.curves=[self.plots[0].plot(pen=pg.mkPen('#35a6e8',width=1.5)),self.plots[1].plot(pen=pg.mkPen('#e0a341',width=1.5)),self.plots[2].plot(pen=pg.mkPen('#42c59c',width=2))]
        self.timer=QtCore.QTimer(self);self.timer.timeout.connect(self.tick);self.timer.start(30)
        self.scan()
    def scan(self):
        old=self.ports.currentText(); self.ports.clear()
        self.ports.addItems([p.device for p in list_ports.comports()])
        if old in [self.ports.itemText(i) for i in range(self.ports.count())]: self.ports.setCurrentText(old)
    def reset_base(self):
        if self.v: self.base=float(np.median(list(self.v)[-min(500,len(self.v)):]))
        self.env=0
    def toggle(self):
        if self.ser:
            self.close_serial();return
        try:
            self.ser=serial.Serial(self.ports.currentText(),230400,timeout=0)
            self.ser.reset_input_buffer()
            self.t.clear();self.v.clear();self.envelopes.clear();self.first_us=None;self.last_us=None;self.elapsed_us=0;self.pending.clear();self.bad_lines=0;self.total=0;self.base=None;self.env=0
            self.connect_btn.setText('中斷連線');self.record_btn.setEnabled(True)
        except Exception as e: QtWidgets.QMessageBox.critical(self,'連線失敗',str(e))
    def close_serial(self):
        if self.file:self.toggle_record()
        if self.ser:self.ser.close();self.ser=None
        self.connect_btn.setText('連線');self.record_btn.setEnabled(False);self.status.setText('已中斷連線（保留最後波形）')
    def toggle_record(self):
        if self.file:
            self.file.close();self.file=None;self.writer=None;self.record_btn.setText('開始記錄 CSV');return
        name='emg_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.csv'
        path,_=QtWidgets.QFileDialog.getSaveFileName(self,'儲存量測資料',name,'CSV (*.csv)')
        if not path:return
        self.file=open(path,'w',newline='',encoding='utf-8-sig');self.writer=csv.writer(self.file)
        self.writer.writerow(['esp32_us','time_s','voltage_mV','baseline_mV','delta_mV','envelope_mV'])
        self.record_btn.setText('停止記錄 CSV')
    def tick(self):
        if not self.ser:return
        try:
            # Read complete lines only. Partial serial packets remain buffered.
            chunk = self.ser.read(min(self.ser.in_waiting, 32768))
            if chunk:
                self.pending.extend(chunk)
            if len(self.pending) > 131072:
                self.pending.clear()
                self.bad_lines += 1
            n = 0
            while b'\n' in self.pending and n < 3000:
                line, _, remainder = self.pending.partition(b'\n')
                self.pending = bytearray(remainder)
                try:
                    a, b = line.decode('ascii').strip().split(',')
                    raw_us = int(a)
                    mv = float(b)
                    if not (0 <= raw_us < 2**32 and 0 <= mv <= 3300):
                        raise ValueError('invalid range')
                except (ValueError, UnicodeDecodeError):
                    self.bad_lines += 1
                    continue
                if self.last_us is None:
                    self.elapsed_us = 0
                else:
                    step = (raw_us - self.last_us) & 0xFFFFFFFF
                    # Accept real 32-bit micros() rollover, but reject reboot,
                    # delayed/out-of-order packets and implausible time jumps.
                    if step == 0 or step > 2_000_000:
                        self.bad_lines += 1
                        if raw_us < 5_000_000:
                            self.t.clear(); self.v.clear(); self.envelopes.clear()
                            self.base = None; self.env = 0.0
                            self.elapsed_us = 0
                            self.last_us = raw_us
                        continue
                    self.elapsed_us += step
                self.last_us = raw_us
                ts = self.elapsed_us / 1e6
                if self.base is None: self.base = mv
                delta = mv - self.base
                alpha = 1 - np.exp(-0.002 / 0.1)
                self.env += alpha * (abs(delta) - self.env)
                self.t.append(ts); self.v.append(mv)
                self.envelopes.append(self.env); self.total += 1
                if self.writer:
                    self.writer.writerow([raw_us, f'{ts:.6f}', mv,
                                          f'{self.base:.2f}', f'{delta:.2f}',
                                          f'{self.env:.2f}'])
                n += 1
            if not self.t:return
            t=np.asarray(self.t);v=np.asarray(self.v);e=np.asarray(self.envelopes)
            duration = float(self.window.currentText())
            mask = t >= t[-1] - duration
            # Always plot relative to the newest sample: -window ... 0 seconds.
            x = t[mask] - t[-1]
            self.curves[0].setData(x, v[mask] / 1000)
            self.curves[1].setData(x, v[mask] - self.base)
            self.curves[2].setData(x, e[mask])
            for p in self.plots:
                p.setXRange(-duration, 0, padding=0)
            d=np.diff(t[-min(len(t),1001):]);rate=1/np.median(d[d>0]) if np.any(d>0) else 0
            self.status.setText(f'連線中 | 取樣率約 {rate:.0f} Hz | 樣本數 {self.total} | 基準 {self.base:.1f} mV | 最新 {v[-1]:.1f} mV | 無效封包 {self.bad_lines}')
        except (serial.SerialException,OSError) as e:
            self.close_serial();QtWidgets.QMessageBox.warning(self,'連線中斷',str(e))
    def closeEvent(self,event):
        self.close_serial();super().closeEvent(event)

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    w=Viewer();w.show();sys.exit(app.exec())
