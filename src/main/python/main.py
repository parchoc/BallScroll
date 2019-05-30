import sys

from fbs_runtime.application_context import ApplicationContext

from ballscroll import BallScroll


def main():
    appctxt = ApplicationContext()
    window = BallScroll()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
