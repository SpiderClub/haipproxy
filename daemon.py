# import sys, os, time, atexit
# from signal import SIGTERM
#
#
# class Daemon:
#     def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
#         # 需要获取调试信息，改为stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr'，以root身份运行。
#         self.stdin = stdin
#         self.stdout = stdout
#         self.stderr = stderr
#         self.pidfile = pidfile
#
#     def _daemonize(self):
#         try:
#             pid = os.fork()  # 第一次fork，生成子进程，脱离父进程
#             if pid > 0:
#                 sys.exit(0)  # 退出主进程
#         except OSError as e:
#             sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
#             sys.exit(1)
#
#         os.chdir("/")  # 修改工作目录
#         os.setsid()  # 设置新的会话连接
#         os.umask(0)  # 重新设置文件创建权限
#
#         try:
#             pid = os.fork()  # 第二次fork，禁止进程打开终端
#             if pid > 0:
#                 sys.exit(0)
#         except OSError as e:
#             sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
#             sys.exit(1)
#
#             # 重定向文件描述符
#         sys.stdout.flush()
#         sys.stderr.flush()
#         si = open(self.stdin, 'r', 1)
#         so = open(self.stdout, 'a+', 1)
#         se = open(self.stderr, 'a+', 1)
#         os.dup2(si.fileno(), sys.stdin.fileno())
#         os.dup2(so.fileno(), sys.stdout.fileno())
#         os.dup2(se.fileno(), sys.stderr.fileno())
#
#         # 注册退出函数，根据文件pid判断是否存在进程
#         atexit.register(self.delpid)
#         pid = str(os.getpid())
#         open(self.pidfile, 'w+').write('%s\n' % pid)
#
#     def delpid(self):
#         os.remove(self.pidfile)
#
#     def start(self):
#         # 检查pid文件是否存在以探测是否存在进程
#         try:
#             pf = open(self.pidfile, 'r')
#             pid = int(pf.read().strip())
#             pf.close()
#         except IOError:
#             pid = None
#
#         if pid:
#             message = 'pidfile %s already exist. Daemon already running!\n'
#             sys.stderr.write(message % self.pidfile)
#             sys.exit(1)
#
#             # 启动监控
#         self._daemonize()
#         self._run()
#
#     def stop(self):
#         # 从pid文件中获取pid
#         try:
#             pf = open(self.pidfile, 'r')
#             pid = int(pf.read().strip())
#             pf.close()
#         except IOError:
#             pid = None
#
#         if not pid:  # 重启不报错
#             message = 'pidfile %s does not exist. Daemon not running!\n'
#             sys.stderr.write(message % self.pidfile)
#             return
#
#             # 杀进程
#         try:
#             while 1:
#                 os.kill(pid, SIGTERM)
#                 time.sleep(0.1)
#                 # os.system('hadoop-daemon.sh stop datanode')
#                 # os.system('hadoop-daemon.sh stop tasktracker')
#                 # os.remove(self.pidfile)
#         except OSError as err:
#             err = str(err)
#             if err.find('No such process') > 0:
#                 if os.path.exists(self.pidfile):
#                     os.remove(self.pidfile)
#             else:
#                 print(str(err))
#                 print(sys.exit(1))
#
#     def restart(self):
#         self.stop()
#         self.start()
#
#     def _run(self):
#         """ run your fun"""
#         while True:
#             # fp=open('/tmp/result','a+')
#             # fp.write('Hello World\n')
#             sys.stdout.write('%s:hello world\n' % (time.ctime(),))
#             sys.stdout.flush()
#             time.sleep(2)
#
#     def speak_out(self):
#         while True:
#             print('aaa')
#             time.sleep(1)
#             print('aaaa')
#
#
# if __name__ == '__main__':
#     daemon = Daemon('/tmp/watch_process.pid', stdout='/tmp/watch_stdout.log')
#     if len(sys.argv) == 2:
#         if 'start' == sys.argv[1]:
#             daemon.start()
#         elif 'stop' == sys.argv[1]:
#             daemon.stop()
#         elif 'restart' == sys.argv[1]:
#             daemon.restart()
#         else:
#             print('unknown command')
#             sys.exit(2)
#         sys.exit(0)
#     else:
#         print('usage: %s start|stop|restart' % sys.argv[0])
#         sys.exit(2)
class Base(object):
    def __init__(self):
        print("enter Base")
        print("leave Base")

class A(Base):
    def __init__(self):
        print("enter A")
        super().__init__()
        print("leave A")

class B(Base):
    def __init__(self):
        print("enter B")
        super().__init__()
        print("leave B")

class C(A, B):
    def __init__(self):
        print("enter C")
        super().__init__()
        print("leave C")

if __name__ == '__main__':
    ins = C()