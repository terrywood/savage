#-*- encoding: gb2312 -*-
import os, sys, string
import poplib

# pop3��������ַ
host = "pop3.163.com"
# �û���
username = "qq3532619@163.com"
# ����
password = "abcabc123123"
# ����һ��pop3�������ʱ��ʵ�����Ѿ������Ϸ�������
pp = poplib.POP3(host)
# ���õ���ģʽ�����Կ�����������Ľ�����Ϣ
pp.set_debuglevel(1)
# ������������û���
pp.user(username)
# ���������������
pp.pass_(password)
# ��ȡ���������ż���Ϣ��������һ���б���һ����һ���ж��Ϸ��ʼ����ڶ����ǹ��ж����ֽ�
ret = pp.stat()
print (ret)
# ��Ҫȡ�������ż���ͷ�����ż�id�Ǵ�1��ʼ�ġ�
for i in range(1, ret[0]+1):
    # ȡ���ż�ͷ����ע�⣺topָ�������������ż�ͷΪ�����ģ�Ҳ����˵��ȡ0�У�
    # ��ʵ�Ƿ���ͷ����Ϣ��ȡ1����ʵ�Ƿ���ͷ����Ϣ֮���ٶ�1�С�
    mlist = pp.top(i, 0)
    print ('line: ', len(mlist[1]))
# �г����������ʼ���Ϣ��������ÿһ���ʼ������id�ʹ�С������stat��������ܵ�ͳ����Ϣ
ret = pp.list()
print (ret)
# ȡ��һ���ʼ�������Ϣ���ڷ���ֵ��ǰ��д洢��down[1]���б���ġ�down[0]�Ƿ��ص�״̬��Ϣ
down = pp.retr(1)
print ('lines:', len(down))
# ����ʼ�
for line in down[1]:
    print (line)
# �˳�
pp.quit()