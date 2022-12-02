from smb.SMBConnection import SMBConnection
import time
import argparse

def ShareFile(userID, password, client_machine_name, server_name, domain_name, remote_file, local_file):

    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                     is_direct_tcp=True)
    conn.connect(server_ip, 445)

    shares = conn.listShares()

    for share in shares:
      if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL']:
          sharedfiles = conn.listPath(share.name, '/')
          for sharedfile in sharedfiles:
              print(sharedfile.filename)
              if sharedfile.filename == remote_file:
                  fileObj = open(remote_file,'wb')
                  conn.retrieveFile(share.name,sharedfile.filename,fileObj)
                  fileObj.close() 
                  print(sharedfile.filename+" is downloaded in the current local directory")
                  fileObj2 = open(local_file,'rb')
                  file = local_file
                  conn.storeFile(share.name,'/'+file,fileObj2)
                  print(file+" is uploaded in remote shared directory") 
    conn.close()

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description = \
                                       "Arguments for program")

  parser.add_argument('-u', type=str, \
                      help='Remote Windows user account')

  parser.add_argument('-p', type=str, \
                      help='Remote Windows user password')

  parser.add_argument('-c', type=str, \
                      help='Local SMB cLient name')

  parser.add_argument('-s', type=str, \
                      help='Remote Windows hostname')

  parser.add_argument('-i', type=str, \
                      help='Remote Windows IP address')

  parser.add_argument('-d', type=str, \
                      help='Remote Windows domain name')

  parser.add_argument('-r', type=str, \
                      help='Remote file in Windows machine')

  parser.add_argument('-l', type=str, \
                      help='Local file in this bot')

  args = parser.parse_args()

  server_ip = args.i



while True:
     ShareFile(userID = args.u,
                     password = args.p,
                     client_machine_name = args.c,
                     server_name = args.s,
                     domain_name = args.d,
                     remote_file = args.r,
                     local_file = args.l
               )
     time.sleep(5)
