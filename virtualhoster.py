#!/usr/bin/env python

import os
from time import sleep

name = raw_input('Enter the FQDN eg : ("www.google.com") and hit [ENTER]: ')
path_to_vhost = "/etc/apache2/sites-available/scripted-vhosts.conf"

if name in open(path_to_vhost).read():
        print 'vhost already exists. Please choose a different name.'
else:
        docRoot = '/var/www/'+name
        #if the directory does NOT exist, create it
        if not os.path.isdir(docRoot):
                os.mkdir(docRoot)
                #make an html file
                os.chdir(docRoot)
                with open('index.html', 'wb') as index:
                        index.write('It works!')

        #add the stuff to the scripted vhosts file
        vhosts = open(path_to_vhost, 'a')
        vhosts.write('<VirtualHost *:80>\n')
        vhosts.write("                DocumentRoot "+docRoot+'\n')
        vhosts.write("                ServerName "+name+'\n')
        vhosts.write("</VirtualHost>\n")
        vhosts.close()

        print 'Successfully wrote the config file , Enabling the Config ....'

        # Running system commands to reload the config file
        
        os.system('a2dissite scripted-vhosts.conf')
        os.system('service apache2 reload')
        os.system('a2ensite scripted-vhosts.conf')
        os.system('service apache2 reload')
        
	#Chown the created directory so that ftp user can access and upload and setting necessary permissions

	os.system('chown -R ftpuser:ftpuser '+docRoot)
	os.system('chmod -R 775 '+docRoot)
        
        #wait for apache to restart
        sleep(5)
        #To-Do : Write some tests here to check if all is well !
        print 'Script Successfully Completed !'

