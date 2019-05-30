from PyQt5 import QtWidgets
import sys
from ballscroll import BallScroll


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = BallScroll()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
